"""Chuyển phiếu AI đề xuất (nhãn điền thẳng vào cột duyệt) -> ai_labels.jsonl có cột *_AI + cờ soát lại. Chạy từ gốc repo."""
import json, re
from collections import defaultdict
from openpyxl import load_workbook
B='data/golden_test/v1/'
wb=load_workbook(B+'phieu_duyet_A_AI_de_xuat.xlsx',data_only=True)
def rows(s):
    ws=wb[s];h=[c.value for c in ws[1]];return [dict(zip(h,r)) for r in ws.iter_rows(min_row=2,values_only=True) if any(v not in(None,'') for v in r)]
cand={r['id']:r for r in map(json.loads,open(B+'candidates.jsonl',encoding='utf-8'))}
out={i:{"id":i,"entities":{},"relations":{},"additions":[],"flags":[]} for i in cand}
def reason(x):
    x=(x or '').replace('[AI đề xuất]','').strip(); return x or None
for r in rows('DOAN'):
    n=(r.get('GHI_CHU') or '').replace('[AI]','').strip()
    if n and n!='không có điểm nghi ngờ': out[r['ma_doan']]['note']=n
E={}
for r in rows('THUC_THE'):
    E[(r['ma_doan'],r['ma_tt'])]=r
    out[r['ma_doan']]['entities'][r['ma_tt']]={"verdict":r['KET_LUAN'],"label":r.get('NHAN_DUNG'),"phrase":r.get('CUM_TU_DUNG'),"reason":reason(r.get('GHI_CHU'))}
for r in rows('THEM_THUC_THE'):
    if r.get('CUM_TU'): out[r['ma_doan']]['additions'].append({"phrase":r['CUM_TU'],"nth":r.get('LAN_XUAT_HIEN'),"label":r['NHAN'],"reason":reason(r.get('GHI_CHU'))})
for r in rows('QUAN_HE'):
    out[r['ma_doan']]['relations'][r['ma_cap']]={"label":r['NHAN'],"reason":reason(r.get('GHI_CHU'))}
    h,t=E[(r['ma_doan'],r['head'])],E[(r['ma_doan'],r['tail'])]
    if r['NHAN'] not in('NO_RELATION','CHUA_RO') and 'XOA' in(h['KET_LUAN'],t['KET_LUAN']):
        out[r['ma_doan']]['flags'].append({"id":r['ma_doan'],"ref":r['ma_cap'],"kind":"mâu thuẫn",
          "issue":f"Quan hệ {r['NHAN']} ({h['cum_tu']} → {t['cum_tu']}) gán dương nhưng một đầu bị XOA. Khi import, cặp này sẽ biến mất.",
          "suggest":"Nếu giữ thực thể (bỏ XOA) thì giữ quan hệ; nếu xóa thì không cần làm gì."})
F=[("GT-138","E4","sai ranh giới","'huyết' bị XOA nhưng câu là 'hình thành huyết khối' — không còn thực thể nào cho bệnh này.","SAI_RANH_GIOI → 'huyết khối', NHAN_DUNG = CONDITION"),
   ("GT-145","E1","sai ranh giới","'huyết' bị XOA trong 'bệnh lý huyết khối' — mất bệnh.","SAI_RANH_GIOI → 'huyết khối', NHAN_DUNG = CONDITION"),
   ("GT-129","E3","trái hướng dẫn","'virus' bị XOA; hướng dẫn ghi rõ 'nhiễm virus' là tình trạng bệnh.","SAI_RANH_GIOI → 'nhiễm virus' (CONDITION)"),
   ("GT-062","E4","mất bệnh","'ruột' bị XOA trong 'hội chứng ruột kích…' (câu bị cắt) — không có CONDITION nào cho hội chứng ruột kích thích.","Thêm CONDITION 'hội chứng ruột kích' hoặc ghi chú CHUA_RO"),
   ("GT-117","E5","có thể giữ","'viêm gan' (lần 2, câu cắt 'viêm gan siêu…') bị XOA; vẫn là một bệnh được nhắc.","Cân nhắc DUNG"),
   ("GT-080","E1","có thể sửa thay vì xóa","'tiêm vắc xin' (DRUG) bị XOA; vắc-xin thuộc DRUG theo schema (PREVENTIVEMED).","SAI_RANH_GIOI → 'vắc xin' nếu không trùng E4"),
   ("GT-082","E2","có thể giữ","'tiêm ngừa' (DRUG) bị XOA; theo schema PREVENTIVEMED → DRUG.","Cân nhắc DUNG hoặc SAI_NHAN → PROCEDURE"),
   ("GT-086","E1","không nhất quán","GT-086 gộp 'bị tiêu' → 'tiêu xương' (một CONDITION), nhưng GT-091/092/093/097/099/100 giữ 'bị tiêu' + located_at → 'xương'.","Chọn một quy ước cho cả 7 đoạn"),
   ("GT-122","E2","trái hướng dẫn","'cao' → 'liều cao' gán DOSAGE và has_dosage; hướng dẫn: mức độ không phải liều (không có hàm lượng/số lượng).","Cân nhắc XOA và NO_RELATION (cả GT-123, GT-124)"),
   ("GT-026","R1","nghi ngờ","has_dosage 'thuốc ngừa thai' → 'hai mươi mốt viên' là số viên trong vỉ, không phải liều dùng (tương tự GT-027 'bảy viên').","Cân nhắc NO_RELATION"),
   ("GT-061","R2","trùng lặp","located_at 'viêm đại tràng' → 'đại tràng': bộ phận đã nằm trong tên bệnh (hướng dẫn: không tạo located_at nội bộ). Tương tự GT-137 R3.","Cân nhắc NO_RELATION"),
   ("GT-021","E1","định dạng","SAI_RANH_GIOI nhưng có điền NHAN_DUNG = TEST — import vẫn áp dụng cả hai.","Xác nhận ý đổi cả ranh giới và nhãn")]
for i,ref,k,iss,sug in F: out[i]['flags'].append({"id":i,"ref":ref,"kind":k,"issue":iss,"suggest":sug})
with open(B+'ai_labels.jsonl','w',encoding='utf-8') as f:
    for i in cand: f.write(json.dumps(out[i],ensure_ascii=False)+'\n')
print('flags',sum(len(o['flags']) for o in out.values()))

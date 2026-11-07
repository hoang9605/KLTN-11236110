"""Explicit, auditable second-pass review; never marks AI output physician approved."""
import copy,json,re,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).parent
SOURCE=ROOT/'outputs/vietmed_600_RE_review/annotations_draft.jsonl'
rows=[json.loads(x) for x in SOURCE.read_text(encoding='utf-8').splitlines()]
changes=[]
def log(n,action,before,after,reason):
 changes.append(dict(sample_id=f'VM600-{n:03}',action=action,before=before,after=after,reason=reason))
# Exact surface matches below were inspected in all six batches. These are not
# general-purpose clinical inference rules.
REMOVE={
 'DOSAGE': 'rất nhiều|cao|một vài thông số|cái thứ hai|cái ngưỡng mức|tính dung nạp|năm mươi|phân tử|mức độ|thứ nhất|cường độ|một người|một trăm phần trăm|hai nhóm|cái tỷ lệ|ba bước|tỷ lệ|những bệnh nhân|đường huyết|một phần|hai bộ phận|phần thứ hai|các chỉ số|hba1c|hai mươi phần trăm|tám mươi phần trăm|ba mươi phần trăm|trung bình|từ năm đến mười phần|nhịp tim|nhịp thở|phần lớn|phần trăm|chiếm đa số|trăm nghìn tỷ|một ca|một trăm phần tử|một trong những cái hướng|ba giai đoạn|giai đoạn|kcal|hiệu quả cao nhất|lưu lượng máu',
 'DRUG':'ức chế|kéo dài tuổi thọ|phòng ngừa|tuân thủ|kiểm soát|khuyến cáo|điều chỉnh|ngăn ngừa|chốt chặn|chỉ định|loại bỏ|phòng tránh|nguy cơ lây chéo|kiểm nghiệm',
 'TEST':'quá trình lão hóa|nghiên cứu|sức đề kháng|hấp thu|chuyển hóa|thích nghi',
 'PROCEDURE':'chiết xuất|cải thiện|hỗ trợ|dự đoán|quá trình sáng|chế biến|truyền miệng|nuôi dưỡng|tăng cường lưu thông máu|nuôi tim|phân tích',
 'CONDITION':'vi khuẩn|mầm bệnh|virus|bị|quan hệ|bẩm sinh|bị trẻ hóa|lây lan',
}
REASONS={
 'DOSAGE':'Không phải liều dùng thuốc trong ngữ cảnh: số thứ tự, mức độ, chỉ số sinh lý, tỷ lệ hoặc lượng thực phẩm.',
 'DRUG':'Đây là hành động/khái niệm, không phải tên thuốc hoặc dược chất.',
 'TEST':'Đây là quá trình sinh lý/nghiên cứu hoặc khái niệm sức khỏe, không phải xét nghiệm/thăm khám.',
 'PROCEDURE':'Đây là quá trình, kết quả hoặc động từ chung; không xác định thủ thuật/điều trị.',
 'CONDITION':'Không phải bệnh/triệu chứng: tác nhân sinh học, từ ngữ chức năng hoặc khái niệm ngoài schema.'}
REMOVE={k:set(v.split('|')) for k,v in REMOVE.items()}
# Per-record edits: old entity IDs remain stable for traceability; additions get
# new IDs, and all offsets and BIO tags are rebuilt from the unchanged text.
# D deletes, S changes surface/type (occurrence is 1-based), A adds a mention.
EDITS={
 1:[('S','E2','bệnh','CONDITION',1)],
 2:[('D','E1')],
 3:[('A','tẩy trắng','PROCEDURE'),('A','dưỡng sáng','PROCEDURE')],
 9:[('S','E2','thuốc nền','DRUG')],
 13:[('A','chiết xuất từ hoa lan','DRUG'),('D','E2')],
 19:[],20:[],24:[],27:[('D','E2')],
 28:[('S','E5','thuốc','DRUG')],
 31:[('S','E1','xét nghiệm sarscov2','TEST'),('D','E2'),('D','E3')],
 36:[('S','E2','thuốc','DRUG',2)],
 37:[('S','E3','kích thích não','PROCEDURE',2)],
 39:[('A','dại','CONDITION')],
 45:[('S','E2','xơ vữa mạch','CONDITION'),('S','E3','thành mạch','BODY_PART')],
 50:[('S','E1','thuốc','DRUG')],
 52:[('D','E1'),('S','E6','vai gáy','BODY_PART'),('D','E7')],
 64:[('S','E3','hệ nội tiết','BODY_PART')],
 65:[('A','căng','CONDITION')],
 72:[],74:[],77:[('S','E1','bệnh','CONDITION')],
 86:[('S','E2','dại','CONDITION')],
 91:[('D','E1'),('A','nhiễm bệnh','CONDITION')],
 94:[('D','E3')],96:[('D','E2')],98:[('A','thận','BODY_PART')],
 99:[('S','E2','huyết áp đang tăng cao','CONDITION')],
 105:[('D','E3')],
 106:[('D','E2'),('A','chiết xuất từ hoa thủy tiên biển','DRUG')],
 111:[('A','bệnh lý','CONDITION',2)],
 116:[('D','E1')],
 122:[('S','E1','tế bào thần kinh','BODY_PART'),('D','E2'),('D','E3'),('A','chất dẫn truyền thần kinh','DRUG')],
 141:[('S','E1','thuốc','DRUG')],
 142:[('S','E4','khớp','BODY_PART'),('D','E3')],
 147:[('S','E2','mạch vành','BODY_PART')],
 149:[('S','E2','thuốc','DRUG')],
 152:[('D','E1'),('S','E2','huyết áp cao','CONDITION'),('S','E4','mỡ máu cao','CONDITION')],
 153:[('S','E1','huyết áp cao','CONDITION'),('S','E3','mỡ máu cao','CONDITION')],
 154:[('D','E1')],
 157:[('A','cơ quan','BODY_PART')],
 159:[('D','E3'),('A','vitamina a','DRUG')],
 160:[('S','E3','l-carnitine fumarate','DRUG'),('D','E4')],
 165:[('S','E4','mạch vành','BODY_PART')],
 171:[('S','E1','mạch vành','BODY_PART'),('S','E2','huyết áp cao','CONDITION')],
 173:[('S','E1','huyết áp nó tăng cao','CONDITION'),('S','E3','huyết áp tăng cao','CONDITION')],
 174:[('S','E2','điều trị giảm cân','PROCEDURE')],
 177:[('S','E2','sọ não','BODY_PART'),('D','E3')],
 179:[('S','E1','mảng vữa xơ','CONDITION',1),('S','E2','mảng vữa xơ','CONDITION',2)],
 186:[('S','E2','huyết áp cao','CONDITION'),('A','bệnh lý','CONDITION')],
 194:[('D','E2')],
 195:[('S','E2','bàn chân','BODY_PART'),('A','tức','CONDITION'),('A','chân','BODY_PART',1),('A','chân','BODY_PART',2),('A','lạnh','CONDITION'),('A','chân','BODY_PART',3),('A','nề','CONDITION')],
 196:[('D','E1')],
 200:[('S','E1','viêm cột sống dính khớp','CONDITION')],
 202:[('D','E1')],
 204:[('S','E4','cột sống thắt lưng','BODY_PART',2),('D','E5')],
 207:[('D','E1')],
 212:[('D','E2'),('D','E3')],
 217:[('S','E1','can thiệp nội mạch','PROCEDURE'),('D','E2')],
 223:[('S','E1','chụp vai gáy','TEST')],
 224:[('D','E4'),('A','đập nó quá nhanh','CONDITION')],
 226:[('S','E1','chân','BODY_PART')],
 228:[('A','chủng ngừa','PROCEDURE')],
 231:[('A','bệnh','CONDITION',1)],
 232:[('S','E1','khám bệnh','TEST'),('S','E2','đánh giá','TEST')],
 234:[('S','E1','huyết áp cao','CONDITION'),('S','E3','mỡ máu cao','CONDITION')],
 238:[('D','E6')],240:[('D','E4')],
 242:[('S','E1','dại','CONDITION')],
 243:[('D','E1'),('D','E2')],
 244:[('S','E1','huyết áp cao','CONDITION'),('S','E3','mỡ máu cao','CONDITION')],
 248:[('D','E1')],
 249:[('S','E3','đánh giá','TEST')],
 250:[('D','E1'),('A','đập hồi hộp','CONDITION')],
 255:[('D','E1')],
 260:[('A','bài tập','PROCEDURE')],
 261:[('S','E1','can thiệp','PROCEDURE'),('S','E2','luồn cái dụng cụ','PROCEDURE')],
 266:[('A','tập luyện','PROCEDURE')],
 267:[('A','thèm đường','CONDITION')],
 268:[('S','E1','tế bào miễn dịch','BODY_PART')],
 271:[('S','E1','lấy mẫu','TEST')],
 272:[('A','nhiễm chéo','CONDITION')],
 273:[('S','E3','xơ vữa động mạch','CONDITION')],
 279:[('S','E2','đánh giá','TEST',1),('S','E5','đánh giá','TEST',3)],
 291:[('S','E1','cắt amidan','PROCEDURE')],
 292:[('S','E1','điều trị tâm lý','PROCEDURE')],
 293:[('D','E1')],
 298:[('S','E2','yếu tay chân','CONDITION')],
 301:[('S','E5','rối loạn tự miễn','CONDITION')],
 303:[('D','E2')],
 306:[('D','E1')],
 308:[('S','E1','thâm sau mụn','CONDITION'),('D','E2')],
 309:[('S','E1','kích thích não sau','PROCEDURE')],
 311:[('S','E1','hệ miễn dịch','BODY_PART')],
 312:[('D','E1')],
 313:[('S','E1','bài thuốc','DRUG')],
 316:[('D','E1')],
 319:[('S','E2','khớp','BODY_PART')],
 320:[('S','E2','kháng vitamin k','DRUG')],
 325:[('D','E1')],
 328:[('D','E1'),('D','E3'),('D','E4'),('D','E5')],
 329:[('S','E4','huyết áp cao','CONDITION')],
 331:[('S','E1','kiểm tra ngay huyết áp','TEST'),('D','E2'),('S','E3','thuốc','DRUG',1),('D','E5'),('D','E7')],
 333:[('D','E1'),('A','hba1c','TEST')],
 340:[('D','E1'),('A','ốm yếu','CONDITION')],
 341:[('D','E2'),('S','E3','khảo sát','TEST')],
 342:[('S','E1','cột sống cổ','BODY_PART'),('D','E2')],
 345:[('D','E2')],
 346:[('D','E1')],
 348:[('D','E1')],
 349:[('S','E1','rối loạn về cái hành vi ăn uống','CONDITION')],
 351:[('D','E1')],
 360:[('S','E1','thay đổi hành vi','PROCEDURE'),('A','vận động thể lực','PROCEDURE')],
 363:[('S','E1','đánh giá','TEST'),('A','thăm dò','TEST')],
 364:[('A','chức năng gan bị giảm','CONDITION'),('D','E4')],
 375:[('A','lỗ chân lông','BODY_PART')],
 376:[('S','E2','sản phẩm đông y','DRUG')],
 377:[('S','E2','nghiệm pháp kích thích','TEST')],
 384:[('S','E1','viêm tắc','CONDITION')],
 387:[('S','E2','khảo sát','TEST'),('A','thăm dò','TEST')],
 389:[('S','E1','hoạt chất tẩy rửa bề mặt','DRUG')],
 390:[('D','E1')],
 395:[('S','E1','thăm khám','TEST')],
 396:[('S','E2','thuốc ức chế miễn dịch','DRUG'),('D','E3')],
 398:[('D','E6')],
 401:[('D','E1'),('S','E2','triệu chứng ngoài vận động','CONDITION'),('A','mất ổn định','CONDITION')],
 406:[('A','mặt','BODY_PART',2)],
 407:[('D','E3')],
 410:[('D','E2')],411:[('D','E1')],
 414:[('D','E4')],
 415:[('A','khô','CONDITION')],
 419:[('A','bệnh','CONDITION',2)],
 420:[('A','mặt','BODY_PART'),('A','nhiều dầu','CONDITION')],
 425:[('S','E2','bệnh','CONDITION',2)],
 434:[('S','E2','thuốc','DRUG')],
 436:[('A','vành','BODY_PART')],
 441:[('D','E1'),('S','E2','adenosine','DRUG',1),('S','E3','polysaccharide','DRUG'),('A','cordycepin','DRUG'),('A','adenosine','DRUG',2)],
 442:[('S','E2','vitamin nhóm b','DRUG'),('D','E3')],
 444:[('D','E1'),('D','E2')],
 446:[('S','E1','lấy mẫu','TEST')],
 449:[('D','E1')],
 455:[('A','hẹp tắc','CONDITION')],
 458:[('S','E3','can thiệp','PROCEDURE')],
 461:[('S','E2','hệ tim','BODY_PART'),('A','hệ hô hấp','BODY_PART')],
 470:[('D','E1')],
 472:[('A','nhiễm virus','CONDITION')],
 475:[('S','E1','đai thắt lưng','PROCEDURE')],
 485:[('S','E1','thanh lọc cơ thể','PROCEDURE'),('D','E2')],
 486:[('S','E1','huyết áp cao','CONDITION')],
 489:[('A','probiotic','DRUG')],
 491:[('D','E3')],
 498:[('S','E1','lấy mẫu','TEST')],
 500:[('A','tập thể dục','PROCEDURE')],
 501:[('S','E4','cơ tim','BODY_PART'),('D','E5')],
 503:[('D','E4'),('A','bệnh lý','CONDITION')],
 504:[('S','E1','hệ vi sinh vật','BODY_PART'),('D','E2')],
 508:[('S','E3','đẳng sâm việt nam','DRUG')],
 509:[('S','E3','cơ tim','BODY_PART'),('D','E4')],
 511:[('A','má','BODY_PART')],
 521:[('A','lở loét','CONDITION',1),('A','lở loét','CONDITION',2)],
 523:[('S','E2','hệ thần kinh','BODY_PART')],
 527:[('D','E3')],
 530:[('S','E3','ý định tự tử','CONDITION'),('A','bồn chồn','CONDITION')],
 531:[('D','E1')],
 533:[('S','E4','nhân tế bào','BODY_PART')],
 535:[('A','nhiễm virus','CONDITION')],
 537:[('A','tập luyện','PROCEDURE')],
 538:[('S','E2','đai thắt lưng','PROCEDURE')],
 539:[('S','E2','nhồi máu','CONDITION'),('S','E3','cơ tim','BODY_PART'),('D','E4')],
 542:[('A','đo','TEST')],
 545:[('S','E1','tái khám','TEST')],
 548:[('S','E1','đậu mùa bò','CONDITION'),('A','nhiễm virus','CONDITION')],
 550:[('A','mặt','BODY_PART')],
 554:[('A','tim','BODY_PART')],
 557:[('D','E3')],
 559:[('A','tập thể dục','PROCEDURE',1),('A','tập thể dục','PROCEDURE',2)],
 561:[('S','E3','5k','PROCEDURE')],
 562:[('A','lây chéo','CONDITION')],
 564:[('S','E1','điều trị','PROCEDURE'),('A','mụn ẩn','CONDITION',1)],
 567:[('A','gầy đi','CONDITION')],
 569:[('S','E3','bệnh','CONDITION',1),('A','bệnh','CONDITION',2)],
 571:[('S','E1','màng xơ vữa','CONDITION')],
 572:[('S','E3','cơ tim','BODY_PART'),('D','E4')],
 574:[('D','E1')],
 575:[('S','E1','run','CONDITION',1)],
 579:[('S','E1','khám trên lâm sàng','TEST')],
 580:[('S','E1','thăm khám','TEST')],
 582:[('D','E1')],
 584:[('D','E1')],585:[('D','E1')],
 593:[('D','E1')],
 596:[('A','dưỡng ẩm','PROCEDURE')],
 597:[('A','khó nắm','CONDITION')],
}

# Unresolved linguistic/ontology decisions are explicit and exclude the whole
# sample from the provisional resolved subset. They are never gold negatives.
FLAGS={}
def flag(ns,reason):
 for n in ns:FLAGS.setdefault(n,[]).append(reason)
flag([1,35,49,63,70,77,92,149,188,189,327,359,388,418,425,428,450,460,483,520,539,543,549,569,599,600], 'GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.')
flag([3,13,32,51,56,65,78,87,106,110,139,150,159,160,162,164,181,196,215,219,229,245,247,262,267,282,285,290,306,310,317,323,326,333,346,372,376,385,389,393,409,417,420,441,442,457,466,489,504,508,519,565,577,586,598], 'ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.')
flag([28,37,39,45,52,57,68,79,80,86,98,105,110,126,127,128,131,135,141,142,149,153,165,167,170,171,183,186,190,192,195,202,203,204,212,223,224,242,245,246,247,249,250,256,261,265,273,275,279,286,291,297,298,300,307,309,311,312,321,331,333,338,341,343,349,350,351,358,363,367,376,377,382,384,401,406,408,410,415,419,420,421,423,424,426,435,436,441,448,450,455,458,462,464,470,475,480,485,488,502,503,505,509,511,513,517,518,520,521,522,527,532,534,536,539,541,542,547,550,553,554,555,556,557,558,564,567,570,571,572,579,585,586,592,593,597], 'CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.')
flag([5,11,19,28,30,40,45,52,66,100,111,119,132,147,157,165,167,169,171,173,177,179,186,195,199,200,204,224,231,238,240,250,265,298,319,329,342,357,364,375,384,398,406,414,419,435,436,447,455,459,471,483,484,486,501,506,509,514,517,521,539,540,548,549,556,558,572,581,600], 'SPAN_POLICY: cần chốt nhất quán thực thể bệnh/triệu chứng chứa bộ phận cơ thể (span phẳng hay tách); bản này giữ cách tách nguồn trừ lỗi ranh giới rõ ràng, không tạo thực thể lồng nhau.')
flag([64,145,253,340,453,490,530,594], 'SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.')
flag([246], 'DOSAGE_CONTEXT: có hai lần/hai viên nhưng thuốc và đơn vị thời gian bị thiếu; không tạo has_dosage từ suy đoán.')
flag([18,26,59,108,114,122,156,206,217,221,228,260,266,293,304,320,344,360,366,387,412,434,446,472,498,500,519,524,535,548,559,561,574,578,580,583,596], 'SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.')

# Source pairs have been read independently; only explicit links below survive
# as proposed positives. IDs refer to preserved original IDs or added surfaces.
POS={7:[('E2','E1')],10:[('E2','E1')],11:[('E1','E2')],19:[('E3','E4')],28:[('E2','E1')],35:[('E5','E3')],
52:[('E2','E3'),('E5','E6')],66:[('E2','E3')],70:[('E1','E2')],90:[('E2','E1')],100:[('E1','E2')],
111:[('bệnh lý','E2')],115:[('E2','E1')],132:[('E2','E3'),('E4','E5'),('E6','E7')],137:[('E1','E3')],
157:[('E3','cơ quan')],169:[('E1','E2')],174:[('E1','E2')],186:[('bệnh lý','E1')],188:[('E2','E3')],189:[('E1','E2')],
195:[('tức','chân#1'),('E1','chân#2'),('lạnh','chân#3'),('nề','E2')],199:[('E3','E2'),('E4','E2')],
204:[('E1','E2'),('E3','E4')],224:[('E1','E2'),('đập nó quá nhanh','E2')],231:[('bệnh','E1')],250:[('đập hồi hộp','E5')],
265:[('E2','E1')],286:[('E1','E2')],319:[('E3','E2')],329:[('E1','E2')],357:[('E2','E3')],
375:[('E3','E2')],384:[('E2','E3')],391:[('E2','E1')],408:[('E2','E1')],410:[('E1','E3')],414:[('E1','E2')],
419:[('bệnh','E3')],420:[('nhiều dầu','mặt')],436:[('E1','vành')],447:[('E1','E2')],471:[('E2','E3')],483:[('E1','E2')],
491:[('E2','E1')],505:[('E2','E1')],509:[('E2','E3')],514:[('E1','E2')],
521:[('lở loét#1','E1'),('lở loét#2','E2')],534:[('E2','E1')],537:[('E1','E2'),('E1','E3'),('E1','E4'),('E1','tập luyện')],
539:[('E2','E3')],540:[('E1','E2')],544:[('E2','E1')],549:[('E1','E2'),('E1','E3')],556:[('E2','E1')],558:[('E5','E3')],
564:[('mụn ẩn#1','E1')],572:[('E2','E3')]}
UNC={11:[('E1','E3')],28:[('E2','E5'),('E4','E5')],57:[('E4','E1')],66:[('E2','E1'),('E2','E4'),('E2','E5')],
68:[('E2','E1')],78:[('E1','E3'),('E2','E3')],86:[('E2','E1')],100:[('E3','E2')],
135:[('E1','E2')],137:[('E1','E2')],147:[('E3','E2')],149:[('E1','E2')],170:[('E1','E3')],188:[('E1','E3')],
192:[('E1','E2')],203:[('E2','E1')],223:[('E2','E1'),('E2','E3')],249:[('E1','E2'),('E1','E3')],279:[('E1','E2'),('E1','E4'),('E1','E5')],
300:[('E3','E1')],307:[('E1','E2'),('E1','E3')],319:[('E3','E1')],341:[('E1','E3')],
375:[('E3','E1')],376:[('E3','E1'),('E3','E2')],377:[('E1','E2')],384:[('E1','E3'),('E4','E3'),('E5','E3')],
415:[('E2','E1'),('E3','E1'),('E4','E1'),('khô','E1')],435:[('E2','E3')],450:[('E1','E2')],458:[('E2','E3')],464:[('E1','E2')],
509:[('E2','E1'),('E5','E1'),('E5','E3')],517:[('E4','E2'),('E4','E3')],534:[('E4','E1')],
541:[('E2','E1'),('E2','E3')],547:[('E1','E2')],556:[('E2','E3')],557:[('E1','E5'),('E2','E5')],558:[('E2','E3')],
564:[('E2','E1')],572:[('E2','E1'),('E5','E1'),('E5','E3')],579:[('E3','E1'),('E3','E2')],586:[('E1','E2')]}
SCHEMA={('CONDITION','BODY_PART'):'located_at',('CONDITION','DRUG'):'treated_by',('CONDITION','PROCEDURE'):'treated_by_procedure',('CONDITION','TEST'):'diagnosed_by',('DRUG','DOSAGE'):'has_dosage'}
GENERIC_PROC={'điều trị','trị liệu','chữa trị','phác đồ','can thiệp','phục hồi','đánh giá','chẩn đoán','chuẩn đoán','khảo sát','đo'}

# User adjudication 2026-10-15: retain the complete condition/symptom phrase.
# A separately stated location ("ở", "trong", or a separate clause) remains
# eligible for located_at. Embedded anatomy never becomes a nested entity.
MERGES={
 52:[('E2',['E3'],'đau nhức xương khớp',1),('E5',['E6'],'đau vai gáy',1)],
 66:[('E2',['E3'],'tổn thương tế bào',1)],
 111:[('bệnh lý',['E2'],'bệnh lý về tim mạch',1)],
 132:[('E4',['E5'],'chảy máu dạ dày',1),('E6',['E7'],'viêm loét dạ dày',1)],
 186:[('bệnh lý',['E1'],'bệnh lý tim mạch',1)],
 188:[('E2',['E3'],'bệnh lý khớp',1)],
 195:[('tức',['chân#1'],'tức chân',1),('E1',['chân#2'],'đau chân',1),('lạnh',['chân#3'],'lạnh chân',1),('nề',['E2'],'nề bàn chân',1)],
 204:[('E1',['E2'],'thoái hóa cột sống thắt lưng',1),('E3',['E4'],'đau cột sống thắt lưng',1)],
 224:[('đập nó quá nhanh',['E2'],'tim đập nó quá nhanh',1)],
 231:[('bệnh',['E1'],'bệnh tim mạch',1)],
 250:[('đập hồi hộp',['E5'],'tim đập hồi hộp',1)],
 329:[('E1',['E2'],'đau khớp',1)],
 357:[('E2',['E3'],'tổn thương mô',1)],
 384:[('E2',['E3'],'viêm tĩnh mạch',1)],
 414:[('E1',['E2'],'viêm loét đại tràng',1)],
 419:[('bệnh',['E3'],'bệnh tim mạch',1)],
 435:[('E2',['E3'],'nghẽn mạch máu não',1)],
 447:[('E1',['E2'],'tê bì chân tay',1)],
 471:[('E2',['E3'],'đau cả hai đầu gối',1)],
 509:[('E2',['E3'],'thiếu máu cơ tim',1)],
 521:[('lở loét#1',['E1'],'lở loét miệng',1),('lở loét#2',['E2'],'lở loét miệng',2)],
 540:[('E1',['E2'],'đau khớp',1)],
 572:[('E2',['E3'],'thiếu máu cơ tim',1)],
}

def locate(text,surface,occ=1):
 hits=[m.start() for m in re.finditer(re.escape(surface),text)]
 assert len(hits)>=occ,(surface,occ,text)
 a=hits[occ-1];return a,a+len(surface)
def ref(es,key):
 if re.fullmatch(r'E\d+',key):
  match=[e for e in es if e['id']==key]
 else:
  s,_,idx=key.partition('#');match=[e for e in es if e['text']==s];match=match[int(idx or 1)-1:int(idx or 1)]
 assert len(match)==1,(key,es)
 return match[0]['id']

result=[]
for n,old in enumerate(rows,1):
 r=copy.deepcopy(old);es=r['entities'];original=copy.deepcopy(es)
 explicit={op[1] for op in EDITS.get(n,[]) if op[0] in ('D','S')}
 for e in list(es):
  if e['id'] not in explicit and e['text'] in REMOVE.get(e['label'],set()):
   es.remove(e);log(n,'remove_entity',e,None,REASONS[e['label']])
 next_id=max([int(e['id'][1:]) for e in original]+[0])+1
 for op in EDITS.get(n,[]):
  if op[0]=='D':
   e=next(e for e in es if e['id']==op[1]);es.remove(e)
   log(n,'remove_entity',e,None,'Rà soát ngữ cảnh: nhãn sai nghĩa, từ nằm trong cụm khác hoặc được gộp vào span đầy đủ.')
  else:
   if op[0]=='S':
    e=next(e for e in es if e['id']==op[1]);before=copy.deepcopy(e);surface,label=op[2:4];occ=op[4] if len(op)>4 else 1
   else:
    e={'id':f'E{next_id}'};next_id+=1;es.append(e);before=None;surface,label=op[1:3];occ=op[3] if len(op)>3 else 1
   a,b=locate(r['text'],surface,occ);e.update(start=a,end=b,text=surface,label=label)
   log(n,'edit_entity' if before else 'add_entity',before,copy.deepcopy(e),'Sửa loại/ranh giới hoặc bổ sung thực thể được nêu trong chính văn bản; không sửa câu nguồn.')
 es.sort(key=lambda e:e['start'])
 # Resolve relation references before merging so removed body mentions can be
 # discarded explicitly rather than retargeted to a different occurrence.
 pos={(ref(es,h),ref(es,t)) for h,t in POS.get(n,[])}
 unc={(ref(es,h),ref(es,t)) for h,t in UNC.get(n,[])}
 merge_plan=[(ref(es,h),[ref(es,t) for t in tails],surface,occ) for h,tails,surface,occ in MERGES.get(n,[])]
 for head,removed,surface,occ in merge_plan:
  e=next(e for e in es if e['id']==head);before=copy.deepcopy(e)
  a,b=locate(r['text'],surface,occ)
  e.update(start=a,end=b,text=surface,label='CONDITION')
  log(n,'edit_entity',before,copy.deepcopy(e),'Theo quyết định của người dùng: giữ toàn bộ cụm bệnh/triệu chứng trong một CONDITION, không tách bộ phận bên trong.')
  for tail in removed:
   t=next(t for t in es if t['id']==tail);es.remove(t)
   log(n,'remove_entity',t,None,'Bộ phận đã nằm trong CONDITION đầy đủ; không tạo span lồng nhau hoặc located_at nội bộ.')
  pos={pair for pair in pos if not set(pair)&set(removed)}
  unc={pair for pair in unc if not set(pair)&set(removed)}
 es.sort(key=lambda e:e['start'])
 for a,b in zip(es,es[1:]):assert a['end']<=b['start'],(n,a,b)
 offsets=[];cursor=0
 for w in r['words']:
  a=r['text'].find(w,cursor);assert a>=0;offsets.append((a,a+len(w)));cursor=a+len(w)
 r['labels']=['O']*len(offsets)
 for e in es:
  indices=[i for i,(a,b) in enumerate(offsets) if a>=e['start'] and b<=e['end']]
  assert indices and offsets[indices[0]][0]==e['start'] and offsets[indices[-1]][1]==e['end'],(n,e)
  e['token_start']=indices[0];e['token_end']=indices[-1]+1
  for j,i in enumerate(indices):r['labels'][i]=('B-' if j==0 else 'I-')+e['label']
  e['review_status']='AI_REVIEWED_PENDING_HUMAN'
 flags=[f for f in FLAGS.get(n,[]) if not f.startswith('SPAN_POLICY:')]
 if any(e['text'] in GENERIC_PROC for e in es):flags.append('GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.')
 if any(e['text'] in ('huyết áp','mỡ máu') and e['label']=='CONDITION' for e in es):flags.append('PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.')
 if n in (169,505):
  unc|=pos;pos=set()
 assert not pos&unc,n
 pairs=[]
 for h in es:
  for t in es:
   allowed=SCHEMA.get((h['label'],t['label']))
   if not allowed:continue
   key=(h['id'],t['id']);label=allowed if key in pos else 'CHUA_RO' if key in unc else 'NO_RELATION'
   a=min(h['start'],t['start']);b=max(h['end'],t['end'])
   reason=('Liên kết được nêu trong đoạn; chỉ áp dụng cho hai lần nhắc đã chỉ định.' if key in pos else
    'Thiếu ngữ cảnh hoặc quy ước về phủ định/câu hỏi/tham chiếu; không dùng làm nhãn âm.' if key in unc else
    'Đã xét cặp cụ thể: đoạn không xác lập quan hệ thuộc 5 loại; đồng xuất hiện/nhân quả/phòng ngừa không đủ để gán điều trị.')
   pairs.append(dict(id=f'R{len(pairs)+1}',head=h['id'],tail=t['id'],allowed_relation=allowed,label=label,
    review_status='AI_REVIEWED_PENDING_HUMAN',evidence=dict(start=a,end=b,text=r['text'][a:b]),rationale=reason))
 actual={(p['head'],p['tail']) for p in pairs}
 assert pos|unc <= actual,(n,(pos|unc)-actual)
 if unc:flags.append('UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.')
 oldpairs={(p['head'],p['tail']):p for p in old['relations']}
 newpairs={(p['head'],p['tail']):p for p in pairs}
 for key in oldpairs.keys()|newpairs.keys():
  b=oldpairs.get(key);a=newpairs.get(key)
  if b is None or a is None or b['label']!=a['label'] or b['allowed_relation']!=a['allowed_relation'] or b['evidence']!=a['evidence']:
   log(n,'relation_change',b,a,'Tạo lại cặp hợp lệ sau sửa NER và đọc lại liên kết trong đoạn. ID R chỉ có ý nghĩa trong bản này.')
 r.update(entities=es,relations=pairs,annotation_status='AI_SECOND_PASS_PENDING_ADJUDICATION' if flags else 'AI_SECOND_PASS_RESOLVED_PROVISIONAL',
  reviewer='AI_second_pass',reviewed_at='2026-10-15',human_verified=False,training_eligible=False,
  review_flags=sorted(set(flags)),review_note='; '.join(sorted(set(flags))),
  re_scope='Five directed relation types within unchanged original utterance; no external medical inference',
  original_annotation_sha256=hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True).encode()).hexdigest())
 result.append(r)

def jsonl(name,data):
 (OUT/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8')
jsonl('annotations_reviewed_600.jsonl',result)
for c in changes:
 if c['action'].endswith('entity'):
  for side in ('before','after'):
   if c[side]:c[side]={k:v for k,v in c[side].items() if k in ('id','text','label','start','end')}
jsonl('changes.jsonl',changes)
jsonl('needs_adjudication.jsonl',[r for r in result if r['review_flags']])
jsonl('resolved_provisional.jsonl',[r for r in result if not r['review_flags']])
stats=dict(samples=len(result),entities_before=sum(len(r['entities']) for r in rows),entities_after=sum(len(r['entities']) for r in result),
 changed_samples=len({c['sample_id'] for c in changes}),change_events=dict(collections.Counter(c['action'] for c in changes)),
 relation_labels_before=dict(collections.Counter(p['label'] for r in rows for p in r['relations'])),
 relation_labels_after=dict(collections.Counter(p['label'] for r in result for p in r['relations'])),
 pending_samples=sum(bool(r['review_flags']) for r in result),resolved_provisional_samples=sum(not r['review_flags'] for r in result),
 human_verified_samples=0,training_eligible_samples=0)
(OUT/'stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))

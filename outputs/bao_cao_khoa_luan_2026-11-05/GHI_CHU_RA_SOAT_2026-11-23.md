# Ghi chú rà soát báo cáo (đêm 22–23/11/2026)

Bản được rà: `KHOA_LUAN_TOT_NGHIEP_NguyenHaiHoang-11236110_v33` (101 trang).
Bản đã sửa: `KHOA_LUAN_TOT_NGHIEP_NguyenHaiHoang-11236110_v34.docx/.pdf` (101 trang).
v33 vẫn giữ nguyên. Mã dựng v33 được lưu tạm để có thể quay lại.

Mình đã đọc toàn bộ chữ của 101 trang và xem ảnh thu nhỏ của từng trang để kiểm tra bố cục.
Bố cục trang ổn: bìa, mục lục, đánh số trang, chú thích bảng/hình đúng mẫu, không có bảng hay hình bị tràn lề.

## 1. Đã sửa trong v34

| Chỗ | Lỗi | Đã sửa thành |
|---|---|---|
| Danh mục từ viết tắt | "(entity ký hiệu đánh dấu)", do bộ thay thuật ngữ thay nhầm | "(marker)" |
| 2.3.2 | "dùng ký hiệu đánh dấu kèm loại, tức là ký hiệu đánh dấu có kèm loại thực thể" (lặp ý) | "dùng ký hiệu đánh dấu có kèm loại thực thể" |
| 2.3.3 | "tập huấn luyện RE của khóa luận có 436 cặp dương", trong khi nay tập huấn luyện có thêm dữ liệu sinh | "dữ liệu huấn luyện thật của RE trong khóa luận chỉ có 436 cặp dương" |
| 2.3.4 | "micro-F1 trên lớp dương tính trên các nhãn dương" (lặp) | "micro-F1 tính trên các nhãn dương" |
| 2.4.3 | "một mã mã định danh khái niệm thuốc" (lặp "mã") | bỏ một chữ "mã" |
| 3.3.3.6 | Hai mức dữ liệu sinh 1.169/3.509 cặp dễ nhầm với hai mức đã kiểm tra ở 3.3.3.7 | ghi rõ "kho sinh ban đầu", "hai mức chưa kiểm tra" |
| 3.3.3.7 | Nhắc RxNorm, BioText, ADE nhưng không trích dẫn | thêm [16], [25], [26] |
| 3.3.4, 4.2.1 | "tập nhãn chuẩn mã riêng" (câu gượng, do đổi chữ "gold") | "tập đánh giá riêng", "tập đánh giá chuẩn hóa riêng" |
| 3.4.6.4 | Câu quá dài, nối "như Hình 4.5 cho thấy, mỗi ứng viên có…" | tách thành hai câu |
| Bảng 3.8 | Dòng RE ghi tập kiểm tra "chấm một lần", nhưng thực tế đã chấm x1 trước khi thêm v1/vall | "chỉ để báo cáo" |
| 4.1.2, Bảng 4.1 | Trộn "strict/relaxed", "Strict P" với "khớp chặt" | dùng thống nhất "khớp chặt", "khớp nới lỏng" |
| 4.7.3 | "cấu hình được chọn trên tập kiểm định trước khi chấm tập kiểm tra", không còn đúng hẳn | thêm vế: v1 và vall được thêm sau khi tập kiểm tra đã được chấm một lần |
| Kết luận, mục RE | Chưa nói kết quả của dữ liệu sinh đã kiểm tra | thêm câu: hỗ trợ đủ năm quan hệ nhưng chưa cải thiện có ý nghĩa so với chỉ dữ liệu thật |
| Kết luận, Hạn chế | Quá ngắn (một câu) | thêm: tập kiểm định nhỏ, khoảng 1/10 dữ liệu sinh chỉ qua kiểm tra tự động có thể sai, nhãn tập đánh giá chuẩn hóa do LLM gán chưa được xác nhận |
| 3.4.9, 4.4, Kết luận, Phụ lục F | Kết quả kiểm thử cũ (107 ca, 16/11) | chạy lại ngày 23/11: **114/114 ca đạt**; thêm tệp `test_relation_pipeline.py` vào Bảng F.1 |
| Phụ lục A | Lệnh dựng đồ thị đầu tiên thiếu `--re-mode fallback`, chạy ra đồ thị union khác với báo cáo; còn chữ "tập gold", "Knowledge graph trên split test" | thêm cờ, sửa chữ |
| Phụ lục A | Lệnh pytest chạy cả 9 ca của thư mục thử nghiệm `re_v3` (không thuộc khóa luận) | thêm `--ignore` cho hai tệp đó |
| Phụ lục B | Thiếu đồ thị 21/11, trong khi mục 4.5 có so sánh với đồ thị này | thêm dòng `outputs/kg_test_2026-11-21/` |
| Phụ lục C | "đoạn khoảng 26 từ", trong khi mục 3.3.1 ghi 22 đến 24 từ | "khoảng 22 đến 24 từ" |

## 2. Cần bạn làm hoặc quyết định

1. **Lời cảm ơn đang trống** (trang vi chỉ có tiêu đề). Bạn cần tự viết.
2. **Lời cam đoan**: ngày tháng và chữ ký để trống, bạn ghi tay khi in.
3. ~~Giao diện web và câu ví dụ đang chạy mô hình ∪ luật~~ **Đã sửa (v35, 23/11):**
   - `web/app.py` và `scripts/demo/make_samples.py` chuyển sang `mode="fallback"`, tức mô hình đứng một mình. `scripts/build_kg.py` cũng đổi mặc định sang chế độ này.
   - Đã chạy lại `web/samples.json`: mọi quan hệ có nguồn là mô hình.
   - Đã sửa dòng tiêu đề giao diện và chụp lại Hình 3.6.
   - Đã cập nhật `docs/HUONG_DAN_HE_THONG.md`, `knowledge_graph/README.md` và README của mô hình.
4. **Ngưỡng fuzzy matching ghi theo hai thang**: chữ ghi "0,85", "0,6", "0,87" (thang 0–1), còn Mã giả 3.3 ghi "s ≥ 85" và mục 2.6 nói token_set_ratio có thang 0–100. Nên thống nhất một thang, đề xuất 0–100 (85, 60, 87) cho khớp mã nguồn.
5. **Mục 4.3.3**: con số 0,633 là của mô hình hiện tại (vall), nhưng "12 cặp người gán soát lại" là các cặp mà mô hình trước đó (x1) bỏ sót. Kết luận của đoạn không đổi. Nếu muốn chặt chẽ, có thể thêm "của mô hình trước đó" vào câu về 12 cặp.
6. **Chưa có tài liệu tham khảo cho MED-RT, WHO, NIH** (mục 3.3.3.7). Nếu thầy yêu cầu trích dẫn đủ, cần thêm 2–3 mục vào danh sách tài liệu tham khảo.
7. **"Danh mục các từ viết tắt"** có cả thuật ngữ không phải viết tắt (Âm tiết, Subword, Embedding, Dropout…). Nếu mẫu của Khoa cho phép, nên đổi tên thành "Danh mục từ viết tắt và thuật ngữ".
8. **Đoạn mở đầu Chương 2** có câu "Đáng chú ý, token_set_ratio đạt điểm tối đa…". Câu này đi sâu vào chi tiết, hơi lạc chỗ trong đoạn giới thiệu chương, nên cân nhắc bỏ (nội dung đã có ở mục 2.6).
9. **Trang iv của mục lục** chỉ có một dòng ("Phụ lục F"). Chỉ là vấn đề thẩm mỹ, không cần sửa.
10. **Trang Turnitin** ở cuối vẫn là trang giữ chỗ, bạn in kết quả Turnitin và đóng vào.

## 3. Những điểm nội dung đã đúng, không cần sửa

- Mọi con số RE, đồ thị và chuẩn hóa trong chữ khớp với tệp kết quả, vì báo cáo đọc thẳng từ JSON.
- Các ví dụ lỗi ở mục 4.6.3 đã được đối chiếu lại với mô hình hiện tại.
- Nguồn nhãn được ghi trung thực ở mọi chỗ: nhãn LLM, người duyệt, người có chuyên môn y khoa.

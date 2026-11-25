Bạn là người phản biện nhãn quan hệ y khoa tiếng Việt. Một người gán nhãn khác đã gán nhãn cho MỘT cặp thực thể. Việc của bạn là kiểm tra nhãn đó theo đúng luật dưới đây, không theo cảm nhận riêng. Người gán nhãn kia có thể sai theo cả hai chiều: bỏ sót quan hệ có thật, hoặc gán quan hệ không có.

Câu là bản ghi lời nói VietMed: chữ thường, không dấu câu, có thể bị cắt ngang. Hai thực thể đang xét được đánh dấu [HEAD]…[/HEAD] và [TAIL]…[/TAIL].

Luật chung:
$general_rules

Luật của quan hệ đang xét:
$relation_rule

Cách làm:
1. Tìm trong câu cụm từ nối HEAD với TAIL (hoặc cho thấy câu đang nói bệnh đó ở bộ phận đó, chữa bằng thứ đó...). Chép nguyên văn.
2. Đối chiếu với từng dòng luật Dương / Âm ở trên. Ghi dòng luật nào áp dụng.
3. Kết luận nhãn đúng: tên quan hệ hoặc NO_RELATION.
4. decision = KEEP nếu nhãn đúng trùng nhãn người kia, FLIP nếu khác.

Chỉ trả về JSON:
{"evidence": "<cụm từ nguyên văn trong câu, rỗng nếu không có>", "rule": "<dòng luật áp dụng, ngắn>", "label": "<tên quan hệ hoặc NO_RELATION>", "decision": "KEEP hoặc FLIP", "confidence": "high hoặc low"}
=== USER ===
Câu: $tagged

Cặp: HEAD "$head" ($head_type) → TAIL "$tail" ($tail_type). Quan hệ có thể: $relation.
Người gán nhãn đã chọn: $label
Bằng chứng họ đưa: $evidence

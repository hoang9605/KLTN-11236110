from pathlib import Path

root = Path(__file__).resolve().parents[3]
base = root / 'outputs' / 're_report_2026-10-02' / '.build' / 'build_report.py'
source = base.read_text(encoding='utf-8')
source = source.replace('BAO_CAO_RE_2026-10-02.md', 'BAO_CAO_RE_GUI_GVHD_2026-10-02.md')
source = source.replace('BAO_CAO_RE_2026-10-02.pdf', 'BAO_CAO_RE_GUI_GVHD_2026-10-02.pdf')
source = source.replace('Báo cáo kế hoạch và kỹ thuật RE', 'Báo cáo phương án triển khai RE')
source = source.replace('AI KLTN  |  Hiện trạng và đề xuất  |  Chưa có kết quả RE', 'Khóa luận trích xuất thông tin y tế tiếng Việt  |  Phương án triển khai RE')
source = source.replace("if 'Điểm công bố' in rows[0]: weights = [0.40, 0.20, 0.40]", "if 'Điểm công bố' in rows[0]: weights = [0.40, 0.20, 0.40]\n        if rows[0][0] == 'Tập dữ liệu': weights = [0.17, 0.20, 0.63]")
exec(compile(source, str(base), 'exec'), {'__file__': __file__, '__name__': '__main__'})

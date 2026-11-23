# Dựng khóa luận theo mẫu Trường Công nghệ (NEU): nội dung -> ghép bìa -> Word cập nhật mục lục -> PDF.
#   pwsh -File outputs/bao_cao_khoa_luan_2026-11-05/build_all.ps1
# Cần: NODE_PATH trỏ tới thư mục node_modules có gói docx; PYTEST_SUMMARY (đoạn tóm tắt kết quả pytest).
# Thông tin bìa (tên, mã sinh viên, GVHD...) sửa trong thong_tin_bia.json.
#   -Name đặt tên tệp khác (ví dụ khi bản cũ đang mở trong Word).
param([string]$Name = "KHOA_LUAN_TOT_NGHIEP_2026-11-08")
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path "$PSScriptRoot\..\..").Path
$Dir = $PSScriptRoot
$Body = Join-Path $env:TEMP "$Name.body.docx"
Push-Location $Root
try {
    node "$Dir\build_report.js" . $Body eval/results_2026-11-05
    if ($LASTEXITCODE) { throw "build_report.js failed" }
    & "$Root\.venv\Scripts\python.exe" -X utf8 "$Dir\apply_template.py" "$Dir\Mau_bao_cao_NEU.docx" $Body "$Dir\thong_tin_bia.json" "$Dir\$Name.docx"
    if ($LASTEXITCODE) { throw "apply_template.py failed" }
    & "$Dir\update_fields.ps1" -Docx "$Dir\$Name.docx" -Pdf "$Dir\$Name.pdf"
} finally {
    Pop-Location
    Remove-Item $Body -ErrorAction SilentlyContinue
}

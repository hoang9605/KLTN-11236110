# Mở báo cáo bằng Word để cập nhật mục lục, danh mục bảng/hình và số trang, lưu lại và xuất PDF.
# Chạy bằng PowerShell 7 (pwsh); Windows PowerShell 5 không nạp được thư viện COM của Word trên máy này.
#   pwsh -File outputs/bao_cao_khoa_luan_2026-11-05/update_fields.ps1 -Docx <docx> [-Pdf <pdf>]
param([Parameter(Mandatory = $true)][string]$Docx, [string]$Pdf)
$Docx = (Resolve-Path $Docx).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx, $false, $false)
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    # Đoạn chứa dấu kết thúc của mỗi danh mục là một dòng trống; khi danh mục vừa kín trang, dòng này
    # tràn sang trang mới và để lại một trang trắng trước tiêu đề kế tiếp. Thu nó về cao 1pt.
    foreach ($toc in $doc.TablesOfContents) {
        $p = $doc.Range($toc.Range.End, $toc.Range.End).Paragraphs(1)
        if ($p.Range.Text.Trim().Length -eq 0) {
            $p.Range.Font.Size = 1
            $p.SpaceBefore = 0; $p.SpaceAfter = 0
            $p.LineSpacingRule = 4; $p.LineSpacing = 1
        }
    }
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) { $toc.UpdatePageNumbers() }
    $doc.Save()
    "pages: " + $doc.ComputeStatistics(2)
    if ($Pdf) { $doc.ExportAsFixedFormat($Pdf, 17); "pdf: $Pdf" }
    $doc.Close($false)
} finally {
    $word.Quit()
}

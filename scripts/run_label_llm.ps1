<#
Gán nhãn RE cho câu VietMed thật bằng OpenAI API (re_v3/label_llm.py), từng bước, có trần chi phí.

Khóa API: đặt $env:OPENAI_API_KEY, hoặc ghi một dòng OPENAI_API_KEY=sk-... vào file .env ở gốc repo
(.env đã có trong .gitignore). Nếu chưa có, script hỏi khóa và chỉ giữ trong phiên PowerShell này.

Thứ tự khuyến nghị:
  1. .\scripts\run_label_llm.ps1 -Step check          # 1 câu: kiểm tra khóa + ước tính chi phí pilot
  2. .\scripts\run_label_llm.ps1 -Step pilot -MaxUsd 3 # 300 câu train -> Excel cho chuyên gia
  3. (chuyên gia chấm 1/0 trong file Excel)  .\scripts\run_label_llm.ps1 -Step score
  4. sửa prompt nếu cần (tạo verify_v2.md, đổi PROMPT_VERSION), chạy lại pilot với -Name pilot_label_v2
  5. .\scripts\run_label_llm.ps1 -Step dev  -MaxUsd 3  # 177 câu dev, chuyên gia duyệt 100%
  6. .\scripts\run_label_llm.ps1 -Step test -MaxUsd 3  # 177 câu test, chuyên gia duyệt 100%
  7. .\scripts\run_label_llm.ps1 -Step train -MaxUsd 15 # 1407 câu train, chuyên gia duyệt tầng B + 20% tầng A
Chạm trần thì script dừng gọi API; chạy lại cùng lệnh với -MaxUsd lớn hơn, phần đã gán lấy từ cache.
#>
param(
    [ValidateSet("check", "pilot", "score", "dev", "test", "train")]
    [string]$Step = "check",
    [double]$MaxUsd = 3,
    [string]$Model = "gpt-4o-2024-08-06",
    [string]$Name = "",
    [int]$PilotSize = 300
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$py = Join-Path $root ".venv\Scripts\python.exe"

function Confirm-ApiKey {
    if ($env:OPENAI_API_KEY) { return }
    $envFile = Join-Path $root ".env"
    if ((Test-Path $envFile) -and (Select-String -Path $envFile -Pattern "^OPENAI_API_KEY=\S+" -Quiet)) { return }
    $secure = Read-Host "Nhập OPENAI_API_KEY (chỉ giữ trong phiên này)" -AsSecureString
    $env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new("", $secure).Password
}

$names = @{ check = "pilot_label_v1"; pilot = "pilot_label_v1"; score = "pilot_label_v1";
            dev = "dev_label_v1"; test = "test_label_v1"; train = "train_label_v1" }
if (-not $Name) { $Name = $names[$Step] }

switch ($Step) {
    "check" {
        Confirm-ApiKey
        & $py -X utf8 -m re_v3.label_llm --split train --limit $PilotSize --name $Name --model $Model --check --max-usd 0.05
    }
    "pilot" {
        Confirm-ApiKey
        & $py -X utf8 -m re_v3.label_llm --split train --limit $PilotSize --name $Name --model $Model --max-usd $MaxUsd --a-fraction 1.0
    }
    "score" {
        $xlsx = Join-Path $root "re_v3\data\silver\$Name\${Name}_expert_review.xlsx"
        if (-not (Test-Path $xlsx)) { throw "Không thấy $xlsx" }
        & $py -X utf8 -m re_v3.expert_review $xlsx
    }
    { $_ -in "dev", "test" } {
        Confirm-ApiKey
        & $py -X utf8 -m re_v3.label_llm --split $Step --name $Name --model $Model --max-usd $MaxUsd --a-fraction 1.0
    }
    "train" {
        Confirm-ApiKey
        & $py -X utf8 -m re_v3.label_llm --split train --name $Name --model $Model --max-usd $MaxUsd --a-fraction 0.2
    }
}
if ($Step -ne "score" -and $Step -ne "check") {
    Write-Host ""
    Write-Host "Excel cho chuyên gia: re_v3\data\silver\$Name\${Name}_expert_review.xlsx"
    Write-Host "Chuyên gia ghi tên + ngày ở sheet Hướng dẫn, chấm 1/0, lưu file, rồi chạy: .\scripts\run_label_llm.ps1 -Step score -Name $Name"
}

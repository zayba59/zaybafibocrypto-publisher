$ErrorActionPreference = "Stop"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "Python bulunamadı. Python 3.11+ kurup tekrar çalıştırın."
}

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
  Copy-Item ".env.example" ".env"
  Write-Host ".env oluşturuldu. Telegram bilgilerini bu dosyaya yazın."
} else {
  Write-Host ".env zaten mevcut; üzerine yazılmadı."
}

Write-Host ""
Write-Host "Kurulum tamamlandı."
Write-Host "Çalıştırmak için: .\baslat.ps1"

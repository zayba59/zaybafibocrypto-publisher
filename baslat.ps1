$ErrorActionPreference = "Stop"

if (-not (Test-Path ".env")) {
  throw ".env bulunamadı. Önce .\kurulum.ps1 çalıştırın ve .env dosyasını doldurun."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
  throw ".venv bulunamadı. Önce .\kurulum.ps1 çalıştırın."
}

Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "& '.\.venv\Scripts\python.exe' 'src\publisher.py'" 
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "& '.\.venv\Scripts\python.exe' 'src\dashboard.py'" 

Start-Process "http://127.0.0.1:8081"
Write-Host "Publisher ve ana ekran başlatıldı."

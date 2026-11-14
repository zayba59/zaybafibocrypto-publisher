# zaybafibocrypto-publisher
Telegram’da yalnızca sizin admin hesabınızdan gelen paylaşımları hedef kanala/gruba gönderen bağımsız yayın botu ve ana ekran.
## Kurulum
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```
`.env` içine şunları yazın:
- `TELEGRAM_BOT_TOKEN`: BotFather tokenı
- `TELEGRAM_ADMIN_CHAT_ID`: yalnızca sizin Telegram chat ID’niz
- `TELEGRAM_TARGET_CHAT_ID`: yayınların gideceği kanal/grup ID’si
İki terminalde çalıştırın:
```powershell
python src\publisher.py
python src\dashboard.py
```
Ana ekran: `http://127.0.0.1:8081`
Telegram komutları:
- `/publish BTCUSDT için takip mesajı`
- `/signal 0.618 seviyesi: 65000, kapanış bekleniyor`
- `/status`
- `/help`
Admin chat ID dışındaki tüm kullanıcılar yok sayılır. Bot emir açmaz ve Binance hesabına erişmez; mevcut sinyal botundan bağımsızdır. GitHub’a yüklendikten sonra başka bilgisayarda `git clone`, güncellemede `git pull` kullanılabilir.

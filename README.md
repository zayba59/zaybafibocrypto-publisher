# zaybafibocrypto-publisher

Telegram’da yalnızca sizin admin hesabınızdan gelen paylaşımları hedef kanala/gruba gönderen bağımsız yayın botu ve 20 kontrollü inceleme ajanından oluşan ana yayın sistemi.

## Windows kurulumu

```powershell
cd "$env:USERPROFILE\Desktop"
git clone https://github.com/zayba59/zaybafibocrypto-publisher.git
cd zaybafibocrypto-publisher
powershell -ExecutionPolicy Bypass -File .\kurulum.ps1
```

`.env` dosyasına BotFather tokenı, sizin Telegram chat ID’niz ve hedef kanal ID’sini yazın:

- `TELEGRAM_BOT_TOKEN`: BotFather tokenı
- `TELEGRAM_ADMIN_CHAT_ID`: yalnızca sizin Telegram chat ID’niz
- `TELEGRAM_TARGET_CHAT_ID`: yayınların gideceği kanal/grup ID’si

Başlatmak için:

```powershell
.\baslat.ps1
```

Ana ekran: `http://127.0.0.1:8081`

## Telegram komutları

- `/publish BTCUSDT için takip mesajı`
- `/signal 0.618 seviyesi: 65000, kapanış bekleniyor`
- `/review BTCUSDT fiyat 65000 RSI 55 stop 64000`
- `/status`
- `/help`

`/review` komutu 20 alt kontrolü çalıştırır ve eksik alanları `needs_data` olarak raporlar. Bu ajanlar emir açmaz, Binance hesabına erişmez ve otomatik yatırım kararı vermez. Yayın yetkisi yalnızca `TELEGRAM_ADMIN_CHAT_ID` ile eşleşen hesaptadır. Mevcut çalışan sinyal botundan bağımsızdır.

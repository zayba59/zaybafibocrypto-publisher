# zaybafibocrypto-publisher

Telegram’da yalnızca sizin admin hesabınızdan gelen paylaşımları hedef kanala/gruba gönderen, Binance Fibonacci taraması yapan ve 20 kontrollü inceleme ajanından oluşan ana yayın sistemi.

## Windows kurulumu

```powershell
cd "C:\Users\SEKAR\Desktop\Zayba Bot\zaybafibocrypto-publisher"
git -c http.sslBackend=openssl pull --ff-only
powershell -ExecutionPolicy Bypass -File .\kurulum.ps1
```

`.env` dosyasına BotFather tokenı, sizin Telegram chat ID’niz ve hedef kanal ID’sini yazın. Binance taraması için `BINANCE_SYMBOLS`, `INTERVAL`, `LOOKBACK` ve `ALERT_TOLERANCE` ayarları da kullanılır.

Başlatmak için:

```powershell
.\baslat.ps1
```

Kontrol merkezi: `http://127.0.0.1:8081`

Kontrol merkezinden GitHub güncellemesi, kurulum/onarım, botu başlatma-durdurma ve işlem günlüğü görüntüleme yapılabilir.

## Telegram komutları

- `/publish BTCUSDT için takip mesajı`
- `/signal 0.618 seviyesi: 65000, kapanış bekleniyor`
- `/review BTCUSDT fiyat 65000 RSI 55 stop 64000`
- `/status`
- `/help`

`/review` komutu 20 alt kontrolü çalıştırır. Bot emir açmaz, Binance hesabına erişmez ve yalnızca sinyal yayınlar. Yayın yetkisi yalnızca `TELEGRAM_ADMIN_CHAT_ID` ile eşleşen hesaptadır. Mevcut çalışan sinyal botundan bağımsızdır.

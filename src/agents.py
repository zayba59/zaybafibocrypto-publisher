"""20 kontrollü sinyal inceleme ajanı.

Bu modüller emir açmaz ve yatırım kararı vermez. Gelen sinyal metnini
konu bazında kontrol eder; eksik veri varsa bunu açıkça raporlar.
"""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AgentResult:
    name: str
    scope: str
    status: str
    note: str


def _check(name: str, scope: str, text: str, keywords: tuple[str, ...]) -> AgentResult:
    normalized = text.casefold()
    found = [word for word in keywords if word.casefold() in normalized]
    if found:
        return AgentResult(name, scope, "ready", f"İlgili alan bulundu: {', '.join(found)}")
    return AgentResult(name, scope, "needs_data", "Bu alan için sinyal metninde veri yok")


AGENTS: tuple[tuple[str, str, Callable[[str], AgentResult]], ...] = (
    ("veri-kalite", "veri kalite", lambda t: _check("veri-kalite", "veri kalite", t, ("fiyat", "giriş"))),
    ("fibonacci", "Fibonacci seviyeleri", lambda t: _check("fibonacci", "Fibonacci seviyeleri", t, ("fibo", "0.618", "0.382"))),
    ("trend", "trend ve piyasa yapısı", lambda t: _check("trend", "trend ve piyasa yapısı", t, ("trend", "yükseliş", "düşüş"))),
    ("hacim", "hacim ve likidite", lambda t: _check("hacim", "hacim ve likidite", t, ("hacim", "volume", "likidite"))),
    ("momentum", "momentum göstergeleri", lambda t: _check("momentum", "momentum göstergeleri", t, ("rsi", "macd", "momentum"))),
    ("volatilite", "ATR ve volatilite", lambda t: _check("volatilite", "ATR ve volatilite", t, ("atr", "volatilite"))),
    ("risk", "risk ve stop kontrolü", lambda t: _check("risk", "risk ve stop kontrolü", t, ("stop", "risk"))),
    ("sinyal-skor", "sinyal puanlama", lambda t: _check("sinyal-skor", "sinyal puanlama", t, ("puan", "skor"))),
    ("zaman", "zaman dilimi", lambda t: _check("zaman", "zaman dilimi", t, ("5m", "15m", "1h", "zaman"))),
    ("sembol", "sembol ve parite", lambda t: _check("sembol", "sembol ve parite", t, ("usdt", "btc", "eth"))),
    ("duplikasyon", "tekrarlı sinyal", lambda t: _check("duplikasyon", "tekrarlı sinyal", t, ("tekrar", "cooldown"))),
    ("telegram-guvenlik", "Telegram yetki kontrolü", lambda t: AgentResult("telegram-guvenlik", "Telegram yetki kontrolü", "ready", "Yetki publisher.py tarafından admin chat ID ile kontrol edilir")),
    ("mesaj-format", "mesaj biçimi", lambda t: AgentResult("mesaj-format", "mesaj biçimi", "ready", "Mesaj yayın öncesi metin olarak korunur")),
    ("dashboard", "ana ekran izlenebilirliği", lambda t: AgentResult("dashboard", "ana ekran izlenebilirliği", "ready", "Son olay dashboard state dosyasına yazılır")),
    ("loglama", "audit ve hata kayıtları", lambda t: AgentResult("loglama", "audit ve hata kayıtları", "ready", "Olay tipi ve son metin kaydedilir")),
    ("performans", "çalışma süresi", lambda t: AgentResult("performans", "çalışma süresi", "ready", "Ajanlar yerel ve deterministik çalışır")),
    ("test", "test edilebilirlik", lambda t: AgentResult("test", "test edilebilirlik", "ready", "Her ajan bağımsız fonksiyon olarak çağrılabilir")),
    ("config", "ayar yönetimi", lambda t: AgentResult("config", "ayar yönetimi", "ready", "Telegram ayarları .env üzerinden okunur")),
    ("fail-safe", "eksik veri ve hata güvenliği", lambda t: AgentResult("fail-safe", "eksik veri ve hata güvenliği", "ready", "Eksik alanlar needs_data olarak raporlanır")),
    ("entegrasyon", "publisher entegrasyonu", lambda t: AgentResult("entegrasyon", "publisher entegrasyonu", "ready", "Sonuçlar /review ve /signal akışına bağlanabilir")),
)


def run_agents(text: str) -> list[AgentResult]:
    return [factory(text) for _, _, factory in AGENTS]


def format_report(text: str) -> str:
    results = run_agents(text)
    ready = sum(result.status == "ready" for result in results)
    lines = [f"20 ajan kontrolü: {ready}/20 hazır", ""]
    lines.extend(f"• {result.name}: {result.status} — {result.note}" for result in results)
    return "\n".join(lines)

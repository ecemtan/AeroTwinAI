# Geliştirme Ortamı Kurulumu (Windows · PowerShell · VS Code)

Bu adımlar temiz bir klon üzerinde doğrulanmıştır (bkz. "Doğrulama kaydı").

## 1. Ön koşullar

| Araç | Sürüm | Kontrol |
|---|---|---|
| Git | 2.40+ | `git --version` |
| Python | **3.12 önerilir** (3.11+ desteklenir) | `py -3.12 --version` |
| Node.js | 20.19+ veya 22.12+ (Vite 8 gereksinimi) | `node --version` |
| VS Code | güncel | Python, Pylance ve ESLint/oxlint eklentileri önerilir |
| OpenVSP | **isteğe bağlı** — yalnızca aerodinamik çalışması için | bkz. bölüm 5 |

JSBSim ayrıca kurulmaz: `pip` paketi `c172p` uçak modeliyle birlikte gelir.

## 2. Depoyu alın

```powershell
git clone https://github.com/ecemtan/AeroTwinAI.git
cd AeroTwinAI
git switch main
git pull
```

## 3. Python ortamı

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Sanal ortamı etkinleştirmek isterseniz: `.\.venv\Scripts\Activate.ps1`.
PowerShell betik çalıştırmayı engelliyorsa etkinleştirmeden devam edin; bu
dokümandaki komutlar `.\.venv\Scripts\python.exe` ile doğrudan çalışır.
VS Code'da `Ctrl+Shift+P → Python: Select Interpreter → .venv` seçin.

Eski Jet Drone betikleri için (isteğe bağlı): `.\.venv\Scripts\python.exe -m pip install -e ".[dev,legacy]"`

## 4. Doğrulama komutları

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m simulation check
.\.venv\Scripts\python.exe -m simulation run --duration 10
.\.venv\Scripts\python.exe -m validation.jsbsim_reference_check
.\.venv\Scripts\python.exe -m aerodynamics check
```

Beklenen sonuçlar:

- `pytest`: tüm testler geçer (JSBSim kuruluysa atlanan test olmaz).
- `simulation check`: `"available": true`, `"c172p": true`.
- `simulation run`: trimlenmiş seyir uçuşu; başlangıç ve bitiş irtifası/hızı neredeyse aynı.
- `jsbsim_reference_check`: `18/18 checks passed`.
- `aerodynamics check`: OpenVSP kurulu değilse **çıkış kodu 1** ve
  "NOT ready" mesajı verir. Bu beklenen durumdur; Cessna OpenVSP geometrisi henüz yoktur.

## 5. Backend ve frontend'i çalıştırma

Terminal 1 — backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000
```

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs (Swagger arayüzü)

Terminal 2 — frontend:

```powershell
cd frontend
npm ci
npm run dev
```

- http://localhost:5173 — Vite, `/api` ve `/health` isteklerini 8000 portuna iletir.

Frontend kontrolleri: `npm run lint` ve `npm run build`.

## 6. OpenVSP / VSPAERO (yalnızca aerodinamik geliştirme)

OpenVSP pip ile kurulmaz. https://openvsp.org adresinden Windows sürümünü indirip
bir klasöre açın, ardından `.env` dosyasına ekleyin:

```text
OPENVSP_ROOT=C:\Tools\OpenVSP-3.x-win64
```

Kontrol: `.\.venv\Scripts\python.exe -m aerodynamics check` artık VSPAERO yolunu göstermelidir.
OpenVSP'nin Python API'si (`openvsp` modülü) belirli bir Python sürümüne bağlıdır;
gerekmedikçe kurmayın. İlk aşamada VSPAERO komut satırından çalıştırılacaktır.

## 7. Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| Frontend'de "Backend erişilemiyor" | Terminal 1'de uvicorn çalışıyor mu? Port 8000 boş mu? |
| `Port 5173 is already in use` | Diğer Vite sürecini kapatın (`strictPort` açık). |
| `ModuleNotFoundError: core` | `pip install -e ".[dev]"` komutunu depo kökünde çalıştırın. |
| `Activate.ps1 cannot be loaded` | Etkinleştirmeden `.\.venv\Scripts\python.exe` kullanın. |
| JSBSim başlangıç yazıları (`JSBSim startup beginning`) | Normaldir; JSBSim'in kendi çıktısıdır. |

## Doğrulama kaydı

16 Ekim 2026: Windows 11 · Python 3.12.10 · Node 24.15.0 · npm 11.12.1. Temiz bir
klonda yukarıdaki komutlar çalıştırıldı (sonuçlar commit mesajında ve PR açıklamasında).

# Ekip Görevleri — İlk Demo (15 Kasım 2026)

## Roller

| Kişi | Alan | Sahip olduğu klasörler |
|---|---|---|
| Proje lideri | Mimari, Cessna geometrisi, OpenVSP/VSPAERO, doğrulama, entegrasyon kararları | `core/`, `aircraft/`, `aerodynamics/`, `validation/`, `docs/` |
| Öğrenci 1 | Backend (FastAPI, Pydantic, servisler, sonuç yönetimi) | `backend/` |
| Öğrenci 2 | Frontend (React, TS, Three.js, grafikler, göstergeler) | `frontend/` |
| Öğrenci 3 | Uçuş simülasyonu (JSBSim, senaryolar, telemetri) | `simulation/` |

Kendi klasörünüz dışındaki bir dosyayı değiştirmeniz gerekirse PR'da sahibini gözden geçiren olarak ekleyin.
`core/` şemalarındaki değişiklikler proje liderinin onayını gerektirir.

## Takvim

| Hafta | Tarih | Hedef (hafta sonu kontrol noktası) |
|---|---|---|
| 1 | 19–25 Eki | Her modül kendi başına çalışıyor; simülasyon REST endpoint'i hazır; arayüz gerçek bir simülasyon sonucunu çiziyor |
| 2 | 26 Eki–1 Kas | Senaryolar; Cessna OpenVSP modeli ve ilk VSPAERO α taraması; 3B model sahnede |
| 3 | 2–8 Kas | Telemetriyle hareket eden 3B model; aero grafikleri; doğrulama karşılaştırması |
| 4 | 9–15 Kas | Entegrasyon, test, demo provası. **12 Kas: özellik dondurma.** 15 Kas: demo |

Demo akışı (`README.md` ile aynı): uygulama açılır → Cessna 172 seçilir → 3B model →
senaryo seçimi → JSBSim hesaplar → hız/irtifa/yönelim gösterilir → 3B model hareket
eder → VSPAERO grafikleri → sonuçlar incelenir.

## Pazartesi (19 Eki) ilk saat — herkes

1. `docs/SETUP.md` adımlarını uygulayın; `pytest` ve frontend `npm run build` başarılı olsun.
2. `docs/ARCHITECTURE.md` ve `docs/API_CONTRACT.md` dosyalarını okuyun.
3. Kendi dalınızı açın: `git switch -c feature/<alan>-<kısa-konu>` (bkz. `CONTRIBUTING.md`).
4. Sorun yaşarsanız ekran çıktısı ve komutla birlikte ekip kanalına yazın.

---

## 1. hafta görevleri ve kabul kriterleri

### Öğrenci 1 — Backend

**G1.1 `POST /api/simulation/runs`** (Öğrenci 3 ile birlikte)
- `simulation.runner.run_simulation` fonksiyonunu çağırır; şemalar `simulation/schemas.py`'den gelir.
- JSBSim çalışması CPU'yu bloklar: `def` endpoint (thread pool) veya `run_in_threadpool` kullanın.
- Hata eşlemesi `docs/API_CONTRACT.md` tablosuna uygun (422 / 503 / 500).

**G1.2 Sonuç kaydı**
- Her başarılı koşu `data/runs/<run_id>/result.json` olarak yazılır.
- `GET /api/simulation/runs/{run_id}` kaydı döndürür, `data_origin` değeri `"replay"` olur.

**G1.3 Testler**
- `tests/test_api_simulation.py`: başarılı koşu, geçersiz istek (422), JSBSim yokken 503 (`monkeypatch` ile `JSBSIM_ROOT`).

Kabul kriterleri:
- [ ] `pytest` tamamı geçiyor; yeni endpoint'lerin her biri en az bir testle kapsanıyor.
- [ ] `/docs` sayfasında istek/yanıt şemaları görünüyor.
- [ ] 10 s / 10 Hz bir koşu 2 saniyenin altında yanıt veriyor (ölçüp PR'a yazın).
- [ ] `API_CONTRACT.md` içindeki durum 🟡 → ✅ olarak güncellendi.

### Öğrenci 2 — Frontend

**G2.1 Simülasyon ekranı**
- `SimulationPanel`: başlangıç koşulu formu (irtifa ft/m, hız kt, yön derece → API'ye SI/rad gönderilir).
- G1.1 hazır olunca "Çalıştır" düğmesi; yanıttaki `samples` dizisinden irtifa, hız ve yönelim grafikleri.
- Grafik kütüphanesi seçimi (öneri: Plotly veya uPlot) PR açıklamasında gerekçelendirilir.

**G2.2 Veri kökeni gösterimi**
- `data_origin` değeri her grafikte görünür; `replay` için belirgin bir "Tekrar oynatma" etiketi.
- Backend kapalıyken ve 503 döndüğünde anlaşılır mesaj (sahte veri yok).

**G2.3 Three.js**
- `AircraftViewer` içinde örnek bir `TelemetrySample` ile yönelim uygulayan fonksiyon
  (`BODY_TO_THREE`, `docs/ARCHITECTURE.md` §4). Model yoksa eksen/ok nesnesi döner.

Kabul kriterleri:
- [ ] `npm run lint` ve `npm run build` hatasız.
- [ ] Gerçek bir JSBSim koşusu ekranda çiziliyor; birimler eksenlerde yazılı.
- [ ] Hiçbir bileşen sabit kodlanmış "örnek" sonuç göstermiyor.
- [ ] Ekran görüntüsü PR'a eklendi.

### Öğrenci 3 — Uçuş simülasyonu

**G3.1 Senaryolar**
- `simulation/scenarios.py`: en az üç senaryo (düz seyir, sabit gazla tırmanış, koordineli viraj),
  her biri `SimulationRequest` üretir. Viraj için kontrol girişleri zamanla değişebilmeli
  (runner'a `ControlSchedule` benzeri bir yapı ekleyin; şema değişikliğini proje lideriyle konuşun).

**G3.2 Telemetri doğrulama testleri**
- Trimli seyirde 60 s boyunca irtifa ve hız sapması sınırları (sınırları ölçün, gerekçelendirin).
- Viraj senaryosunda yön açısının beklenen yönde değiştiği.
- Birim kontrolü: JSBSim `ft` değeri ile `altitude_m` tutarlı.

**G3.3 Performans**
- 60 s simülasyon süresini ölçün; gerçek zamandan hızlı mı? Sonucu `simulation/README.md`'ye yazın.

Kabul kriterleri:
- [ ] `python -m simulation run` her senaryo için çalışıyor (`--scenario` parametresi).
- [ ] `pytest -m jsbsim` geçiyor; testler rastgelelik içermiyor.
- [ ] JSBSim özelliklerinin (property) adları ve birimleri `simulation/README.md` içinde listelendi.

### Proje lideri — Aerodinamik, geometri, doğrulama

**GL.1 Cessna OpenVSP modeli**
- Varyant seçimi (172P ya da 172S) ve kaynakları; `aircraft/c172/geometry/c172.vsp3`.
- `aircraft_config.json:geometry_model` güncellemesi; varyant farkları `aircraft/c172/README.md`'ye.

**GL.2 VSPAERO ortamı**
- OpenVSP kurulumu, `python -m aerodynamics check` → ready. Komut satırıyla tek bir α noktası koşusu.

**GL.3 Referans veri**
- POH değerlerinin (MTOW, Vs, Vy vb.) birincil kaynaktan kontrolü; `unverified` → `verified` geçişleri PR ile.

Kabul kriterleri:
- [ ] `.vsp3` dosyası depoda; parametreleri kaynaklı.
- [ ] VSPAERO çıktısı (tek nokta) elde edildi; referans alan, açıklık ve kord kayıtlı.
- [ ] `jsbsim_reference_check` geçiyor; `verified` işaretli her değerin birincil kaynağı var.

---

## Kural hatırlatmaları

- Eksik mühendislik verisi uydurulmaz; `missing` olarak kalır.
- Önceden kaydedilmiş veri `replay` olarak işaretlenir.
- VSPAERO ve JSBSim sonuçları aynı fizik modelinin parçası değildir.
- Jet Drone dosyalarına dokunulmaz.

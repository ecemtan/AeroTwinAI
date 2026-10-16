# AeroTwin AI — Mimari (v0.1, Cessna 172)

Bu doküman `docs/SYSTEM_ARCHITECTURE.md` (Jet Drone dönemi) dosyasının yerini alır.
Oradaki mühendislik kuralları geçerliliğini korur ve aşağıda yer alır.

## 1. Modüller ve sorumluluklar

| Klasör | Sorumlu | Görev | Durum (16 Eki 2026) |
|---|---|---|---|
| `core/` | Proje lideri | Ortak veri modelleri, SI birim katmanı, koordinat çerçeveleri, uçak kayıtları | çalışıyor, testli |
| `aircraft/c172/` | Proje lideri | Kaynaklı uçak parametreleri, ileride OpenVSP geometrisi | yapılandırma var, geometri yok |
| `aerodynamics/` | Proje lideri | OpenVSP/VSPAERO servisi | ortam kontrolü + iskelet; analiz yok |
| `simulation/` | Öğrenci 3 | JSBSim c172p çalıştırıcı, senaryolar, telemetri | başsız (headless) trimli koşu çalışıyor |
| `validation/` | Proje lideri | Referans karşılaştırmaları, hata metrikleri | yapılandırma ↔ JSBSim çapraz kontrolü |
| `backend/` | Öğrenci 1 | FastAPI, Pydantic, REST/WebSocket | `/health`, `/api/aircraft` |
| `frontend/` | Öğrenci 2 | React + TS + Vite, Three.js, grafikler | dashboard iskeleti |
| `tests/` | Herkes | pytest | 39 test |
| `aircraft/jetdrone/`, `aerodynamics/*.py` mesh betikleri | — | Eski Jet Drone çalışması | korunuyor, API'ye bağlı değil |

Bağımlılık yönü (döngü yasak):

```text
frontend ──HTTP──▶ backend ──▶ simulation ─┐
                           ├──▶ aerodynamics ├──▶ core
                           └──▶ validation ──┘
```

`core` hiçbir modüle bağımlı değildir. `simulation` ve `aerodynamics` birbirini
içe aktarmaz; yalnızca `core` şemaları üzerinden konuşurlar.

## 2. Veri akışı (demo hedefi)

```text
Kullanıcı ─▶ React Dashboard ─▶ FastAPI
                                   ├─ GET  /api/aircraft/{id}      → core.aircraft_registry
                                   ├─ POST /api/simulation/runs     → simulation.runner (JSBSim)
                                   ├─ POST /api/aerodynamics/sweeps → aerodynamics.service (VSPAERO)
                                   └─ GET  /api/validation/...      → validation
```

Sözleşmelerin ayrıntısı: `docs/API_CONTRACT.md`. Uygulanmış ve planlanmış endpoint'ler orada ayrı işaretlidir.

## 3. Birimler

Modüller arası tüm değerler **SI**'dır: m, kg, s, N, N·m, Pa, W, rad, rad/s, m/s.

- Dönüşümler yalnızca `core/units.py` ile yapılır (JSBSim: ft, in, lbf, slug).
- Arayüz gösterim için birim değiştirebilir (kt, ft, derece); API asla.
- Alan adları birimi içerir: `altitude_m`, `heading_rad`, `true_airspeed_mps`.

## 4. Koordinat sistemleri

Tanımlar ve dönüşüm matrisleri: `core/frames.py` (testler: `tests/test_frames.py`).

| Çerçeve | Orijin | +X | +Y | +Z | Kullanan |
|---|---|---|---|---|---|
| BODY | Ağırlık merkezi | burun (ileri) | sağ kanat | aşağı | Telemetri, açısal hızlar |
| STRUCTURAL | Model referans noktası | kuyruk (geri) | sağ kanat | yukarı | JSBSim XML konumları (inç) |
| OPENVSP | Model referans noktası | kuyruk (geri) | sağ kanat | yukarı | OpenVSP geometrisi (m) |
| NED | Yerel teğet nokta | kuzey | doğu | aşağı | Konum/hız, Euler açıları |
| THREE | Sahne orijini | doğu | yukarı | güney | Three.js sahnesi |

- Euler açıları: 3-2-1 (yaw–pitch–roll), NED → BODY, radyan.
- Three.js'teki uçak modeli: burun −Z, sağ kanat +X, yukarı +Y (`BODY_TO_THREE`).
  Böylece ψ = 0 (kuzey) için modele ek dönüş gerekmez.
- Jet Drone'un CATIA → OpenVSP dönüşümü `aerodynamics/coordinate_transform.py` içinde ayrıca belgelidir.

## 5. Veri kaynağı ve doğrulama kuralları

1. Her mühendislik parametresi `SourcedValue` olarak tutulur: değer, birim, kaynak, durum.
2. Durumlar: `verified`, `reference_model`, `unverified`, `missing`. Eksik değer `null` kalır; tahminle doldurulmaz.
3. `reference_model` değerleri `python -m validation.jsbsim_reference_check` ile JSBSim dosyalarına karşı otomatik doğrulanır.
4. Simülasyon sonuçları `data_origin` taşır: `live_simulation` veya `replay`. Tekrar oynatma arayüzde açıkça belirtilir.
5. Aerodinamik sonuçlar referans alan/açıklık/kord, geometri dosyası hash'i ve `validation_status` olmadan yayınlanmaz.
6. Gerekli araç yoksa servis **hata verir**; yer tutucu sayı döndürmez.
7. **VSPAERO ve JSBSim farklı fizik modelleridir.** Sonuçları karşılaştırılabilir ama aynı modelin parçası sayılmaz. Tam bağlı aero–uçuş dinamiği ayrı bir çalışmadır.
8. OpenVSP geometrisinin varyantı JSBSim `c172p` (172P) ile aynı varsayılmaz; farklar `aircraft/c172/README.md` dosyasına yazılır.
9. STL mesh alanı kanat referans alanı olarak kullanılmaz; CAD geometrisi tek başına uçuş modeli değildir.

## 6. Kalıcı veri

| Tür | Biçim | Konum |
|---|---|---|
| Uçak yapılandırması | JSON (`core.models.AircraftConfig`) | `aircraft/<id>/config/` |
| Analiz/simülasyon sonuçları | JSON (+ ileride CSV/Parquet zaman serisi) | `data/runs/<run_id>/` (git'e girmez) |
| 3B geometri | `.vsp3`, görüntüleyici için `.glb` | `aircraft/<id>/geometry/` |

## 7. Kapsam dışı (ilk demo)

Gerçek zamanlı kontrol girdisi, PX4/Gazebo, MATLAB/Simulink, AI model eğitimi,
fiziksel sensör bağlantısı, CFD ve tam bağlı aero–uçuş dinamiği.
AI iş paketi demodan sonra ayrı ele alınır (`ai/` klasörü boş bırakıldı).

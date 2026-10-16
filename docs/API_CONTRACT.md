# API Sözleşmesi (v0.1)

- Temel adres (geliştirme): `http://127.0.0.1:8000`. Canlı şema: `/openapi.json`, arayüz: `/docs`.
- Tüm sayısal alanlar SI'dır; açılar radyandır (bkz. `docs/ARCHITECTURE.md`).
- Kaynak gerçekleri: Pydantic modelleri. TypeScript karşılıkları: `frontend/src/api/types.ts`.
  Bir modeli değiştiren PR, iki tarafı ve bu dokümanı birlikte günceller.
- Hata gövdesi FastAPI standardıdır: `{"detail": "..."}`.

Durum etiketleri: ✅ uygulandı ve testli · 🟡 şema hazır, endpoint yok · ⬜ planlandı

## ✅ `GET /health`

API ayaktaysa her zaman 200 döner. `status`, yalnızca tüm modüller kullanılabilirse `ok` olur, aksi halde `degraded`.

```json
{
  "status": "degraded",
  "api_version": "0.1.0",
  "timestamp": "2026-10-16T08:00:00Z",
  "modules": {
    "aircraft_registry": {"available": true, "aircraft_ids": ["c172"], "error": null},
    "jsbsim": {"available": true, "version": "1.3.3", "root_dir": "...", "models": {"c172p": true}, "error": null},
    "openvsp": {"python_api_available": false, "vspaero_path": null, "vspscript_path": null,
                "available": false, "error": "VSPAERO executable not found. ..."}
  }
}
```

Model: `backend/app/routers/health.py::HealthResponse`. Test: `tests/test_api.py`.

## ✅ `GET /api/aircraft`

Etkin uçakların özeti (`core.models.AircraftSummary`):

```json
[{"aircraft_id": "c172", "name": "Cessna 172", "category": "single_engine_fixed_wing",
  "flight_dynamics_model": "c172p", "geometry_model_available": false}]
```

## ✅ `GET /api/aircraft/{aircraft_id}`

Tam yapılandırma (`core.models.AircraftConfig`). Bilinmeyen ya da eski (`jetdrone`) kimlik için **404** döner.
`geometry`, `mass_properties` ve `propulsion` bölümleri `SourcedValue` sözlükleridir:

```json
"wing_area": {"status": "reference_model", "source": "jsbsim_c172p",
              "source_value": 174.0, "source_unit": "ft2",
              "value": 16.16512896, "unit": "m2", "frame": null, "note": "metrics/wingarea"}
```

## 🟡 `POST /api/simulation/runs` (Öğrenci 1 + Öğrenci 3, 1. hafta)

İstek: `simulation.schemas.SimulationRequest`. Yanıt: `simulation.schemas.SimulationResult`.
Çalışan Python fonksiyonu: `simulation.runner.run_simulation`.

```json
{"aircraft_id": "c172",
 "initial_conditions": {"altitude_m": 914.4, "true_airspeed_mps": 51.4, "heading_rad": 0.0,
                        "pitch_rad": 0.0, "roll_rad": 0.0, "latitude_deg": 0.0, "longitude_deg": 0.0},
 "controls": {"throttle": 0.7, "mixture": 1.0, "elevator": 0.0, "aileron": 0.0, "rudder": 0.0, "pitch_trim": 0.0},
 "trim": true, "duration_s": 10.0, "output_rate_hz": 10.0}
```

Yanıtta `metadata.data_origin`, `metadata.applied_controls`, `metadata.warnings` ve
`samples[]` bulunur. Her örnek `TelemetrySample`: `t_s`, `latitude_deg`, `longitude_deg`,
`altitude_m`, `true_airspeed_mps`, `groundspeed_mps`, `vertical_speed_mps`, `roll_rad`,
`pitch_rad`, `heading_rad`, `p_radps`, `q_radps`, `r_radps`, `alpha_rad`, `beta_rad`.

Hata eşlemesi (uyulacak):

| Durum | HTTP |
|---|---|
| Doğrulama hatası (Pydantic) | 422 |
| JSBSim kurulu değil / model yok (`JSBSimUnavailableError`) | 503 |
| Trim veya çalıştırma hatası (`SimulationError`) | 500, `detail` içinde neden |

## 🟡 `POST /api/aerodynamics/sweeps` (Proje lideri, 2. hafta)

İstek: `aerodynamics.schemas.AlphaSweepRequest`. Yanıt: `aerodynamics.schemas.AlphaSweepResult`.
VSPAERO ya da geometri yoksa **503** döner ve `detail` alanında `aerodynamics.service.readiness()` çıktısı yer alır.

## ⬜ Planlananlar

| Endpoint | Amaç | Hafta |
|---|---|---|
| `GET /api/simulation/scenarios` | Hazır senaryo listesi (seyir, tırmanış, viraj…) | 2 |
| `GET /api/simulation/runs/{run_id}` | Kaydedilmiş koşu (`data_origin: replay`) | 2 |
| `WS /ws/simulation/{run_id}` | Telemetri akışı (~30 Hz) | 3 |
| `GET /api/aircraft/{id}/model.glb` | Three.js modeli | 2–3 |
| `GET /api/validation/{id}` | Karşılaştırma ve hata metrikleri | 3 |

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_reports_every_module():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"ok", "degraded"}
    modules = body["modules"]
    assert set(modules) == {"aircraft_registry", "jsbsim", "openvsp"}
    assert modules["aircraft_registry"] == {"available": True, "aircraft_ids": ["c172"], "error": None}
    # 'ok' must never be reported while a module is unavailable.
    all_available = all(m["available"] for m in modules.values())
    assert (body["status"] == "ok") == all_available


def test_aircraft_list():
    response = client.get("/api/aircraft")
    assert response.status_code == 200
    assert response.json() == [
        {
            "aircraft_id": "c172",
            "name": "Cessna 172",
            "category": "single_engine_fixed_wing",
            "flight_dynamics_model": "c172p",
            "geometry_model_available": False,
        }
    ]


def test_aircraft_detail():
    response = client.get("/api/aircraft/c172")
    assert response.status_code == 200
    body = response.json()
    assert body["aircraft_id"] == "c172"
    area = body["geometry"]["wing_area"]
    assert area["unit"] == "m2" and area["status"] == "reference_model" and area["source"] == "jsbsim_c172p"
    assert body["geometry"]["fuselage_length"] == {
        "status": "missing", "source": None, "source_value": None, "source_unit": None,
        "value": None, "unit": None, "frame": None, "note": None,
    }


def test_unknown_and_legacy_aircraft_return_404():
    assert client.get("/api/aircraft/jetdrone").status_code == 404
    assert client.get("/api/aircraft/does-not-exist").status_code == 404


def test_cors_allows_vite_dev_server():
    response = client.get("/health", headers={"Origin": "http://localhost:5173"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"

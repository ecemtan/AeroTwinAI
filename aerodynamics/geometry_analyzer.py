
import json
from pathlib import Path

import trimesh


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STL_PATH = (
    PROJECT_ROOT
    / "aircraft"
    / "jetdrone"
    / "geometry"
    / "original"
    / "jetDron.stl"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "aircraft"
    / "jetdrone"
    / "config"
    / "geometry_analysis.json"
)


def analyze_geometry(stl_path: Path) -> dict:
    if not stl_path.is_file():
        raise FileNotFoundError(f"STL file not found: {stl_path}")

    mesh = trimesh.load_mesh(
        str(stl_path),
        process=False
    )

    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError("Expected a single triangular mesh.")

    result = {
        "aircraft": "Jet Drone",
        "source_file": stl_path.name,
        "coordinate_system": {
            "x": "unverified",
            "y": "unverified",
            "z": "unverified"
        },
        
"source_units": "mm",
"output_units": "m",
"bounding_box_m": {
    axis: round(float(value) / 1000.0, 6)
    for axis, value in zip("xyz", mesh.extents)
},
"mesh_surface_area_m2": round(
    float(mesh.area) / 1_000_000.0, 6
),

        "vertices": int(len(mesh.vertices)),
        "faces": int(len(mesh.faces)),
        "bounding_box": {
            axis: round(float(value), 3)
            for axis, value in zip("xyz", mesh.extents)
        },
        "bounds": {
            axis: {
                "min": round(float(mesh.bounds[0][i]), 3),
                "max": round(float(mesh.bounds[1][i]), 3)
            }
            for i, axis in enumerate("xyz")
        },
        "mesh_surface_area": round(float(mesh.area), 3),
        "watertight": bool(mesh.is_watertight)
    }

    return result


def main():
    print("\n===== AEROTWIN AI =====")
    print("Jet Drone Geometry Analysis")
    print("==========================\n")

    result = analyze_geometry(STL_PATH)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_PATH.write_text(
        json.dumps(result, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(f"\nJSON saved: {OUTPUT_PATH}")
    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()

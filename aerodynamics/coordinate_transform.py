
from pathlib import Path
import json

import numpy as np
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
    / "coordinate_transform.json"
)

# CATIA: X = spanwise, Y = vertical, +Z = nose
# OpenVSP: X = aft, Y = spanwise, Z = vertical
#
# Assumption: CATIA +Y points upward.

# CATIA:
# X = kanat açıklığı
# Y = dikey (+Y yukarı varsayılıyor)
# Z = uzunlamasına (+Z burun)

# Hedef koordinat sistemi:
# X = uçağın arkasına doğru
# Y = kanat açıklığı
# Z = yukarı

TRANSFORM = np.array([
    [0, 0, -1],
    [-1, 0, 0],
    [0, 1, 0]
], dtype=float)


def main():
    if not STL_PATH.is_file():
        raise FileNotFoundError(STL_PATH)

    mesh = trimesh.load_mesh(
        STL_PATH,
        process=False
    )

    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError("Expected a triangular mesh")

    # Convert millimeters to meters
    vertices_m = mesh.vertices / 1000.0

    # Transform coordinates
    transformed = vertices_m @ TRANSFORM.T

    # Calculate transformed bounding box
    bounds_min = transformed.min(axis=0)
    bounds_max = transformed.max(axis=0)
    dimensions = bounds_max - bounds_min

    # Validate rotation matrix
    determinant = np.linalg.det(TRANSFORM)

    result = {
        "source": "CATIA",
        "target": "OpenVSP",
        "source_units": "mm",
        "target_units": "m",
        "transform_matrix": TRANSFORM.tolist(),
        "determinant": float(determinant),
        "translation_applied": False,
        "assumptions": {
            "catia_positive_y_is_up": True,
            "catia_positive_z_is_nose": True
        },
        "bounding_box_m": {
            "x": round(float(dimensions[0]), 6),
            "y": round(float(dimensions[1]), 6),
            "z": round(float(dimensions[2]), 6)
        },
        "bounds_m": {
            axis: {
                "min": round(float(bounds_min[i]), 6),
                "max": round(float(bounds_max[i]), 6)
            }
            for i, axis in enumerate("xyz")
        }
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_PATH.write_text(
        json.dumps(result, indent=4),
        encoding="utf-8"
    )

    print("\n===== AEROTWIN AI =====")
    print("CATIA -> OpenVSP Coordinate Transform")
    print("======================\n")

    print(json.dumps(result, indent=4))
    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

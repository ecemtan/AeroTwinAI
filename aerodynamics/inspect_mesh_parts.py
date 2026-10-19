
from pathlib import Path

import trimesh

ROOT = Path(__file__).resolve().parents[1]

STL_PATH = (
    ROOT / "aircraft" / "jetdrone"
    / "geometry" / "original" / "jetDron.stl"
)

mesh = trimesh.load_mesh(STL_PATH, process=True)

print("\n=== AeroTwin AI - Mesh Inspection ===")
print("Vertices:", len(mesh.vertices))
print("Faces:", len(mesh.faces))
print("Watertight:", mesh.is_watertight)

# Separate disconnected mesh components
parts = mesh.split(only_watertight=False)

print("\nNumber of connected components:", len(parts))

# Sort by surface area
parts = sorted(
    parts,
    key=lambda part: part.area,
    reverse=True
)

print("\nLargest 15 components:\n")

for i, part in enumerate(parts[:15]):
    dimensions = part.extents / 1000.0
    center = part.bounds.mean(axis=0) / 1000.0

    print(
        f"Part {i:02d} | "
        f"Faces: {len(part.faces):6d} | "
        f"Size (m): {dimensions.round(3)} | "
        f"Center (m): {center.round(3)}"
    )

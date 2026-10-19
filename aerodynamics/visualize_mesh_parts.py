
from pathlib import Path

import matplotlib.pyplot as plt
import trimesh

ROOT = Path(__file__).resolve().parents[1]

STL_PATH = (
    ROOT / "aircraft" / "jetdrone"
    / "geometry" / "original" / "jetDron.stl"
)

mesh = trimesh.load_mesh(STL_PATH, process=True)

parts = sorted(
    mesh.split(only_watertight=False),
    key=lambda part: part.area,
    reverse=True
)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for i in range(2):
    part = parts[i]
    vertices = part.vertices / 1000.0

    axes[i].scatter(
        vertices[:, 0],
        vertices[:, 2],
        s=0.5,
        alpha=0.6,
        color="navy"
    )

    axes[i].set_title(f"Part {i:02d} - Top View")
    axes[i].set_xlabel("CATIA X (m)")
    axes[i].set_ylabel("CATIA Z (m)")
    axes[i].set_aspect("equal")
    axes[i].grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

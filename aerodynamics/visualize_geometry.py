
from pathlib import Path

import numpy as np
import trimesh
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

STL_PATH = (
    ROOT / "aircraft" / "jetdrone"
    / "geometry" / "original" / "jetDron.stl"
)

mesh = trimesh.load_mesh(STL_PATH, process=False)

# Mesh'in üçgen yüzeylerinden örnek noktalar al
points = mesh.vertices

# Çok büyük dosyalarda çizimi hızlandır
if len(points) > 20000:
    rng = np.random.default_rng(42)
    indices = rng.choice(
        len(points), size=20000, replace=False
    )
    points = points[indices]

# Milimetreden metreye dönüştür
points = points / 1000.0

fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    points[:, 0],
    points[:, 1],
    points[:, 2],
    s=0.3,
    alpha=0.35,
    color="navy"
)

ax.set_xlabel("X (m) - RED")
ax.set_ylabel("Y (m) - GREEN")
ax.set_zlabel("Z (m) - BLUE")

# Orijinden pozitif eksenleri göster
axis_length = 1.5

ax.quiver(0, 0, 0, axis_length, 0, 0,
          color="red", linewidth=2)
ax.quiver(0, 0, 0, 0, axis_length, 0,
          color="green", linewidth=2)
ax.quiver(0, 0, 0, 0, 0, axis_length,
          color="blue", linewidth=2)

ax.set_box_aspect(np.ptp(points, axis=0))
ax.set_title("AeroTwin AI - Jet Drone Coordinate System")


# Uçağı yandan görüntüle
# X ekseni boyunca bakıyoruz: ekranda Z yatay, Y dikey
ax.view_init(elev=0, azim=-90, vertical_axis="y")
ax.set_title("Jet Drone - Side View (Y Vertical)")
 
# Jet Drone - Top View
# CATIA: X = kanat açıklığı, Z = burun yönü
# Yukarıdan bakış için X-Z düzlemini gösteriyoruz.

ax.view_init(
    elev=90,
    azim=-90,
    vertical_axis="y"
)

ax.set_title("Jet Drone - Top View (X-Z Plane)")
 
plt.tight_layout()
plt.show()

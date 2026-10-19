
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

STL_PATH = (
    ROOT / "aircraft" / "jetdrone"
    / "geometry" / "original" / "jetDron.stl"
)

mesh = trimesh.load_mesh(STL_PATH, process=False)

# CATIA coordinates in meters
vertices = mesh.vertices / 1000.0

# X = spanwise, Z = longitudinal
x = vertices[:, 0]
z = vertices[:, 2]

# Sample points for faster plotting
rng = np.random.default_rng(42)
if len(x) > 60000:
    idx = rng.choice(len(x), 60000, replace=False)
    x = x[idx]
    z = z[idx]

fig, ax = plt.subplots(figsize=(12, 8))

ax.scatter(
    x, z,
    s=0.25,
    alpha=0.25,
    color="navy",
    rasterized=True
)

ax.axhline(0, color="gray", linewidth=0.7)
ax.axvline(0, color="gray", linewidth=0.7)

ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.55, 1.55)
ax.set_ylim(-0.65, 0.65)
ax.set_xlabel("CATIA X - Wingspan (m)")
ax.set_ylabel("CATIA Z - Nose Direction (m)")
ax.set_title("AeroTwin AI - Jet Drone Top View")
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

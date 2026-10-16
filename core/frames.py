"""Coordinate frame definitions shared by all modules.

Every vector that leaves a module must state its frame. The frames below are
the only ones the active (Cessna 172) code paths use. See
docs/ARCHITECTURE.md, section "Koordinat sistemleri", for diagrams.

Frame       Origin                 +X           +Y            +Z        Length unit
---------   --------------------   ----------   -----------   -------   -----------
BODY        aircraft CG            nose (fwd)   right wing    down      m
STRUCTURAL  model reference point  tail (aft)   right wing    up        m (JSBSim: in)
OPENVSP     model reference point  tail (aft)   right wing    up        m
NED         local tangent point    north        east          down      m
THREE       scene origin           east         up            south     m

THREE is the Three.js scene frame (right-handed, +Y up). An aircraft mesh used in
the viewer is authored in BODY orientation converted with BODY_TO_THREE, i.e. the
nose points to -Z and the right wing to +X, so that a level aircraft heading north
(psi = 0) needs no extra rotation in the scene.

Euler angles (phi, theta, psi) follow the aerospace 3-2-1 (yaw-pitch-roll)
sequence from NED to BODY, in radians.
"""

from __future__ import annotations

from enum import Enum

import numpy as np


class Frame(str, Enum):
    BODY = "body"
    STRUCTURAL = "structural"
    OPENVSP = "openvsp"
    NED = "ned"
    THREE = "three"


# Rotation matrices: v_target = R @ v_source (pure orientation, no translation).
OPENVSP_TO_BODY = np.array(
    [
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0],
    ]
)

# STRUCTURAL and OPENVSP share the same axis orientation.
STRUCTURAL_TO_BODY = OPENVSP_TO_BODY

# BODY and NED share the (fwd/north, right/east, down) pattern, so the same
# matrix maps both into the Three.js scene frame.
BODY_TO_THREE = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.0],
    ]
)
NED_TO_THREE = BODY_TO_THREE


def ned_to_body_matrix(phi: float, theta: float, psi: float) -> np.ndarray:
    """Direction cosine matrix C_bn: v_body = C_bn @ v_ned (3-2-1 Euler, rad)."""
    cphi, sphi = np.cos(phi), np.sin(phi)
    cth, sth = np.cos(theta), np.sin(theta)
    cpsi, spsi = np.cos(psi), np.sin(psi)
    return np.array(
        [
            [cth * cpsi, cth * spsi, -sth],
            [sphi * sth * cpsi - cphi * spsi, sphi * sth * spsi + cphi * cpsi, sphi * cth],
            [cphi * sth * cpsi + sphi * spsi, cphi * sth * spsi - sphi * cpsi, cphi * cth],
        ]
    )


def body_to_ned_matrix(phi: float, theta: float, psi: float) -> np.ndarray:
    """C_nb = C_bn^T: v_ned = C_nb @ v_body."""
    return ned_to_body_matrix(phi, theta, psi).T


def structural_point_to_body(
    point_structural_m: np.ndarray, cg_structural_m: np.ndarray
) -> np.ndarray:
    """Convert a point in STRUCTURAL (metres) to BODY coordinates about the CG."""
    return STRUCTURAL_TO_BODY @ (np.asarray(point_structural_m) - np.asarray(cg_structural_m))


def is_proper_rotation(matrix: np.ndarray, tol: float = 1e-12) -> bool:
    """True if ``matrix`` is orthonormal with determinant +1."""
    m = np.asarray(matrix, dtype=float)
    return bool(
        m.shape == (3, 3)
        and np.allclose(m @ m.T, np.eye(3), atol=tol)
        and abs(np.linalg.det(m) - 1.0) < tol
    )

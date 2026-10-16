"""SI-based unit conversion layer.

AeroTwin AI uses SI units internally (m, kg, s, N, N*m, rad, Pa).
External tools use other systems -- most importantly JSBSim, which works in
feet, pounds, slugs and inches. Every value that crosses a module boundary
must be converted here, never with ad-hoc literals elsewhere in the code.

All factors are exact by definition unless noted (international foot/pound).
"""

from __future__ import annotations

import math

# --- Length -----------------------------------------------------------------
M_PER_FT = 0.3048
M_PER_IN = 0.0254
M_PER_NMI = 1852.0
M_PER_MM = 0.001

# --- Mass / force -------------------------------------------------------------
KG_PER_LBM = 0.45359237
STANDARD_GRAVITY = 9.80665  # m/s^2
N_PER_LBF = KG_PER_LBM * STANDARD_GRAVITY
KG_PER_SLUG = N_PER_LBF / M_PER_FT  # 1 slug = 1 lbf*s^2/ft

# --- Velocity ---------------------------------------------------------------
MPS_PER_KT = M_PER_NMI / 3600.0
MPS_PER_FPS = M_PER_FT

# --- Pressure / power ---------------------------------------------------------
PA_PER_PSF = N_PER_LBF / M_PER_FT**2
W_PER_HP = 745.69987158227022  # mechanical horsepower


def ft_to_m(value: float) -> float:
    return value * M_PER_FT


def m_to_ft(value: float) -> float:
    return value / M_PER_FT


def in_to_m(value: float) -> float:
    return value * M_PER_IN


def m_to_in(value: float) -> float:
    return value / M_PER_IN


def ft2_to_m2(value: float) -> float:
    return value * M_PER_FT**2


def lbm_to_kg(value: float) -> float:
    return value * KG_PER_LBM


def kg_to_lbm(value: float) -> float:
    return value / KG_PER_LBM


def lbf_to_n(value: float) -> float:
    return value * N_PER_LBF


def slug_to_kg(value: float) -> float:
    return value * KG_PER_SLUG


def slugft2_to_kgm2(value: float) -> float:
    return value * KG_PER_SLUG * M_PER_FT**2


def kt_to_mps(value: float) -> float:
    return value * MPS_PER_KT


def mps_to_kt(value: float) -> float:
    return value / MPS_PER_KT


def fps_to_mps(value: float) -> float:
    return value * MPS_PER_FPS


def mps_to_fps(value: float) -> float:
    return value / MPS_PER_FPS


def psf_to_pa(value: float) -> float:
    return value * PA_PER_PSF


def hp_to_w(value: float) -> float:
    return value * W_PER_HP


def deg_to_rad(value: float) -> float:
    return math.radians(value)


def rad_to_deg(value: float) -> float:
    return math.degrees(value)


# Unit symbol -> factor to convert a value in that unit to SI.
# Used to normalise sourced values (e.g. JSBSim XML attributes) generically.
TO_SI: dict[str, float] = {
    "m": 1.0,
    "mm": M_PER_MM,
    "in": M_PER_IN,
    "ft": M_PER_FT,
    "m2": 1.0,
    "ft2": M_PER_FT**2,
    "kg": 1.0,
    "lbm": KG_PER_LBM,
    "slug": KG_PER_SLUG,
    "N": 1.0,
    "lbf": N_PER_LBF,
    "kg*m2": 1.0,
    "slug*ft2": KG_PER_SLUG * M_PER_FT**2,
    "m/s": 1.0,
    "kt": MPS_PER_KT,
    "ft/s": MPS_PER_FPS,
    "rad": 1.0,
    "deg": math.pi / 180.0,
    "W": 1.0,
    "hp": W_PER_HP,
    "Pa": 1.0,
    "psf": PA_PER_PSF,
}

SI_UNIT_OF: dict[str, str] = {
    "mm": "m", "in": "m", "ft": "m", "m": "m",
    "ft2": "m2", "m2": "m2",
    "lbm": "kg", "slug": "kg", "kg": "kg",
    "lbf": "N", "N": "N",
    "slug*ft2": "kg*m2", "kg*m2": "kg*m2",
    "kt": "m/s", "ft/s": "m/s", "m/s": "m/s",
    "deg": "rad", "rad": "rad",
    "hp": "W", "W": "W",
    "psf": "Pa", "Pa": "Pa",
}


def to_si(value: float, unit: str) -> tuple[float, str]:
    """Convert ``value`` given in ``unit`` to SI. Returns (value, si_unit)."""
    try:
        return value * TO_SI[unit], SI_UNIT_OF[unit]
    except KeyError as exc:
        raise ValueError(f"Unsupported unit: {unit!r}") from exc

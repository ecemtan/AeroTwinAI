import math

import numpy as np
import pytest

from core import frames


@pytest.mark.parametrize(
    "matrix", [frames.OPENVSP_TO_BODY, frames.STRUCTURAL_TO_BODY, frames.BODY_TO_THREE, frames.NED_TO_THREE]
)
def test_fixed_matrices_are_proper_rotations(matrix):
    assert frames.is_proper_rotation(matrix)


def test_openvsp_aft_up_maps_to_body_fwd_down():
    nose_direction_vsp = np.array([-1.0, 0.0, 0.0])  # OpenVSP +X points aft
    up_vsp = np.array([0.0, 0.0, 1.0])
    assert np.allclose(frames.OPENVSP_TO_BODY @ nose_direction_vsp, [1, 0, 0])
    assert np.allclose(frames.OPENVSP_TO_BODY @ up_vsp, [0, 0, -1])


def test_body_to_three_nose_is_minus_z_and_up_is_plus_y():
    assert np.allclose(frames.BODY_TO_THREE @ [1, 0, 0], [0, 0, -1])  # nose
    assert np.allclose(frames.BODY_TO_THREE @ [0, 1, 0], [1, 0, 0])   # right wing
    assert np.allclose(frames.BODY_TO_THREE @ [0, 0, -1], [0, 1, 0])  # up


def test_euler_identity_and_heading():
    assert np.allclose(frames.ned_to_body_matrix(0, 0, 0), np.eye(3))
    # Heading east (psi = 90 deg): body nose points east in NED.
    c_nb = frames.body_to_ned_matrix(0.0, 0.0, math.pi / 2)
    assert np.allclose(c_nb @ [1, 0, 0], [0, 1, 0], atol=1e-12)


def test_euler_pitch_up_raises_nose():
    c_nb = frames.body_to_ned_matrix(0.0, math.radians(10), 0.0)
    nose_ned = c_nb @ [1, 0, 0]
    assert nose_ned[2] < 0  # negative down == up


@pytest.mark.parametrize("angles", [(0.1, -0.2, 2.5), (-1.0, 0.7, -0.3)])
def test_euler_matrix_is_rotation(angles):
    assert frames.is_proper_rotation(frames.ned_to_body_matrix(*angles), tol=1e-12)


def test_structural_point_to_body_about_cg():
    cg = np.array([1.0, 0.0, 0.9])
    tail = np.array([5.0, 0.0, 1.4])  # aft and above the CG
    body = frames.structural_point_to_body(tail, cg)
    assert np.allclose(body, [-4.0, 0.0, -0.5])

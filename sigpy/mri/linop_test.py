import unittest
import numpy as np
import sigpy as sp
import numpy.testing as npt

from sigpy.mri import linop
from sigpy.linop_test import check_linop_adjoint

if __name__ == '__main__':
    unittest.main()


class TestLinop(unittest.TestCase):

    def test_shepp_logan_sense_model(self):
        img_shape = [16, 16]
        mps_shape = [8, 16, 16]

        img = sp.randn(img_shape, dtype=np.complex)
        mps = sp.randn(mps_shape, dtype=np.complex)

        mask = np.zeros(img_shape)
        mask[::2, ::2] = 1.0

        A = linop.Sense(mps)

        check_linop_adjoint(A, dtype=np.complex)

        npt.assert_allclose(sp.fft(img * mps, axes=[-1, -2]),
                            A * img)

    def test_shepp_logan_sense_model_batch(self):
        img_shape = [16, 16]
        mps_shape = [8, 16, 16]

        img = sp.randn(img_shape, dtype=np.complex)
        mps = sp.randn(mps_shape, dtype=np.complex)

        mask = np.zeros(img_shape, dtype=np.complex)
        mask[::2, ::2] = 1.0

        A = linop.Sense(mps, coil_batch_size=1)
        check_linop_adjoint(A, dtype=np.complex)
        npt.assert_allclose(sp.fft(img * mps, axes=[-1, -2]),
                            A * img)

    def test_shepp_logan_noncart_sense_model(self):
        img_shape = [16, 16]
        mps_shape = [8, 16, 16]

        img = sp.randn(img_shape, dtype=np.complex)
        mps = sp.randn(mps_shape, dtype=np.complex)

        y, x = np.mgrid[:16, :16]
        coord = np.stack([np.ravel(y - 8), np.ravel(x - 8)], axis=1)

        A = linop.Sense(mps, coord=coord)
        check_linop_adjoint(A, dtype=np.complex)
        npt.assert_allclose(sp.fft(img * mps, axes=[-1, -2]).ravel(),
                            (A * img).ravel(), atol=0.1, rtol=0.1)

    def test_shepp_logan_noncart_sense_model_batch(self):
        img_shape = [16, 16]
        mps_shape = [8, 16, 16]

        img = sp.randn(img_shape, dtype=np.complex)
        mps = sp.randn(mps_shape, dtype=np.complex)

        y, x = np.mgrid[:16, :16]
        coord = np.stack([np.ravel(y - 8), np.ravel(x - 8)], axis=1)

        A = linop.Sense(mps, coord=coord, coil_batch_size=1)
        check_linop_adjoint(A, dtype=np.complex)
        npt.assert_allclose(sp.fft(img * mps, axes=[-1, -2]).ravel(),
                            (A * img).ravel(), atol=0.1, rtol=0.1)

from .. import T

from .common import ExponentialFamily

__all__ = ["MatrixNormalInverseWishart", "MNIW"]

class MatrixNormalInverseWishart(ExponentialFamily):

    def expected_value(self):
        raise NotImplementedError()

    def sample(self, num_samples=1):
        raise NotImplementedError()

    @classmethod
    def regular_to_natural(cls, regular_parameters):
        S, M0, V, nu = regular_parameters
        V_inv = T.matrix_inverse(V)
        M0V_1 = T.matmul(V_inv, T.matrix_transpose(M0))
        return [
            S + T.matmul(M0, M0V_1),
            T.matrix_transpose(M0V_1),
            V_inv,
            nu
        ]

    @classmethod
    def natural_to_regular(cls, natural_parameters):
        A, B, V_inv, nu = natural_parameters
        V = T.matrix_inverse(V_inv)
        M0 = T.matmul(B, V)
        S = A - T.matmul(B, T.matrix_transpose(M0))
        return([
            S,
            M0,
            V,
            nu
        ])

    def log_likelihood(self, x):
        pass

    def log_z(self):
        S, M0, V, nu = self.get_parameters('regular')
        shape = T.shape(M0)
        d, s = shape[-2], shape[-1]
        return (nu / 2. * (T.to_float(d) * T.log(2.) - T.logdet(S))
                + T.multigammaln(nu / 2., d)
                + T.to_float(s) / 2. * T.logdet(V))

    def log_h(self, x):
        raise NotImplementedError

    def sufficient_statistics(self, x):
        sigma, A = x
        sigma_inv_A = T.matrix_solve(sigma, A)
        return [
            -0.5 * T.matrix_inverse(sigma),
            sigma_inv_A,
            -0.5 * T.matmul(T.matrix_transpose(A), sigma_inv_A),
            -0.5 * T.logdet(sigma)
        ]

    def expected_sufficient_statistics(self):
        S, M0, V, nu = self.get_parameters('regular')
        S_inv = T.matrix_inverse(S)
        S_inv_M0 = T.matrix_solve(S, M0)
        s = T.shape(V)[-1]
        d = T.shape(S)[-1]
        return [
            -nu / 2. * S_inv,
            nu * S_inv_M0,
            -nu / 2. * T.matmul(T.matrix_transpose(M0), S_inv_M0) - T.to_float(s) / 2. * V,
            0.5 * (T.to_float(d) * T.log(2.) - T.logdet(S))
                + T.reduce_sum(T.digamma((nu[...,None] - T.to_float(T.range(d)[None,...]))/2.), -1)
        ]

MNIW = MatrixNormalInverseWishart

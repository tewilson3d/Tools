"""
Most of this was taken from http://mathlab.github.io/PyGeM/_modules/pygem/radial.html#RBF
"""
######################################
############# IMPORTS ################
######################################
import numpy
from scipy.spatial.distance import cdist


######################################
############# FUNCTIONS ##############
######################################
def get_weight_matrix(sp, tp, rbf, radius):
    """Get the weight matrix x in Ax=B

    :param sp: Source control point array
    :param tp: Target control point aray
    :param rbf: Rbf function from class RBF
    :param radius: Smoothing parameter

    :return: Weight matrix
    """
    identity = numpy.ones((sp.shape[0], 1))
    dist = get_distance_matrix(sp, sp, rbf, radius)
    # Solve x for Ax=B
    dim = 3
    a = numpy.bmat(
        [
            [dist, identity, sp],
            [identity.T, numpy.zeros((1, 1)), numpy.zeros((1, dim))],
            [sp.T, numpy.zeros((dim, 1)), numpy.zeros((dim, dim))],
        ]
    )
    b = numpy.bmat([[tp], [numpy.zeros((1, dim))], [numpy.zeros((dim, dim))]])
    weights = numpy.linalg.solve(a, b)
    return weights

def get_distance_matrix(v1, v2, rbf, radius):
    matrix = cdist(v1, v2, "euclidean")
    if rbf != RBF.linear:
        matrix = rbf(matrix, radius)
    return matrix


######################################
############# CLASSES ################
######################################
class RBF(object):
    """Various RBF kernels"""

    @classmethod
    def linear(cls, matrix, radius):
        return matrix

    @classmethod
    def gaussian(cls, matrix, radius):
        result = numpy.exp(-(matrix * matrix) / (radius * radius))
        return result

    @classmethod
    def thin_plate(cls, matrix, radius):
        result = matrix / radius
        result *= matrix

        numpy.warnings.filterwarnings("ignore")
        result = numpy.where(result > 0, numpy.log(result), result)
        numpy.warnings.filterwarnings("always")

        return result

    @classmethod
    def multi_quadratic_biharmonic(cls, matrix, radius):
        result = numpy.sqrt((matrix * matrix) + (radius * radius))
        return result

    @classmethod
    def inv_multi_quadratic_biharmonic(cls, matrix, radius):
        result = 1.0 / (numpy.sqrt((matrix * matrix) + (radius * radius)))
        return result

    @classmethod
    def beckert_wendland_c2_basis(cls, matrix, radius):
        arg = matrix / radius
        first = numpy.zeros(matrix.shape)
        first = numpy.where(1 - arg > 0, numpy.power(1 - arg, 4), first)
        second = (4 * arg) + 1
        result = first * second
        return result
import numpy as np
from cmath import sqrt

ID = np.matrix([[1, 0], [0, 1]])

CNOT = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

T = np.matrix([[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]])

SWAP = np.matrix([[1, 0, 0, 0], [0, 0, 1, 0],
                  [0, 1, 0, 0], [0, 0, 0, 1]])

HAD = np.matrix([[1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)]])

NOT = np.matrix([[0, 1], [1, 0]])

COEF = (1 + 1j) / 2

# TODO: Fix CV/CVPLUS - ask question on stackexchange or find out elsewhere
CV = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                [0, 0, COEF * 1, COEF * -1j], [0, 0, COEF * - 1j, COEF * 1]])

COEF2 = (1 - 1j) / 2

CVPLUS = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                    [0, 0, COEF2 * 1, COEF2 * 1j],
                    [0, 0, COEF2 * 1j, COEF2 * 1]])

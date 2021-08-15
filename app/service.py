import logging
import numpy as np

class QuantumSimulatorService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def tensor(f1, f2, f3=0, f4=0):
        """
        Tensor product for up to three functions
        """
        if(type(f3) is int):
            return np.kron(f1, f2)
        elif(type(f4) is int):
            u = np.kron(f1, f2)
            return np.kron(u, f3)
        else:
            u = np.kron(f1, f2)
            u = np.kron(u, f3)
            return np.kron(u, f4)

    @staticmethod
    def bArrToDec(ba):
        return int(''.join(map(str, ba)), 2)

    @staticmethod
    def dec_to_bin(x):
        return int(bin(x)[2:])

    @staticmethod
    def fixBinToDec(x, d_length):
        if (len(x) < d_length):
            amountToPad = d_length - len(x)
            for i in range(amountToPad):
                x.insert(0, 0)
            return x
        else:
            return x

    def getBinNum(self, x, d_length=0):
        if (d_length == 0):
            d_length = len(bin(x))
        bin_n = [int(i) for i in str(self.dec_to_bin(x))]
        return self.fixBinToDec(bin_n, d_length)

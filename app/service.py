from typing import Optional
from app.quantum_register import QuantumRegister
from app.quantum_gates import CNOT, HAD, ID
import logging
import numpy as np

class QuantumSimulatorService:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_quantum_entanglement_system(self):
        # computation basis for 2 qubit system ~ |00>, |01>, |10>, |11>
        quantum_register = QuantumRegister(
            number_of_qubits=2,
            binary_one_position=2
        )

        self.logger.info(f"Quantum computational basis at init: {quantum_register.amps.T}")

        self.logger.info(self.tensor(HAD, ID))

        self.logger.info("Apply HADxID")
        quantum_register.applyGate(self.tensor(HAD, ID))
        self.logger.info(f"Quantum computational basis after: {quantum_register.amps.T}")

        self.logger.info("Apply CNOT")
        quantum_register.applyGate(CNOT)

        self.logger.info(f"Quantum computational basis after: {quantum_register.amps.T}")

    @staticmethod
    def tensor(
        A: np.matrix,
        B: np.matrix,
        C: Optional[np.matrix] = None,
        D: Optional[np.matrix] = None
    ):
        if(C == None):
            U = np.kron(A, B)
            return U
        elif(D == None):
            U = np.kron(A, B)
            return np.kron(U, C)
        else:
            U = np.kron(A, B)
            U = np.kron(U, C)
            return np.kron(U, D)

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

import numpy as np

class QuantumRegister:
    def __init__(self, number_of_qubits, binary_one_position=None):
        self.number_of_qubits = number_of_qubits
        self.qubits = [0] * number_of_qubits
        self.number_of_amplitudes = 1 << number_of_qubits
        # in this classical simulation, we use 2^n_qubits complex numbers
        self.amps = [0] * self.number_of_amplitudes
        if (binary_one_position):
            self.amps[binary_one_position] = 1
        else:
            self.amps[len(self.amps) - 1] = 1

        # Now turn it into a row vector.
        self.amps: np.matrix = np.matrix(self.amps).T

    def getState(self, qs):
        return qs.measureMQubits(self.amps)

    def applyGate(self, quantum_gate_matrix: np.matrix):
        self.amps = np.dot(
            quantum_gate_matrix,
            self.amps
        )

    def readState(self):
        print(self.amps.T)  # readable form

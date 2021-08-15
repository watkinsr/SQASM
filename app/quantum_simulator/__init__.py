import logging

import numpy as np

from app.quantum_gates import ID, SWAP, CV, CNOT, CVPLUS, T
from app.service import QuantumSimulatorService
from app.quantum_register import QuantumRegister

import random
import math

class QuantumSimulator:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.service = QuantumSimulatorService()
        self.ONE_LOWER_TOLERANCE = 0.999
        self.ONE_UPPER_TOLERANCE = 1.001

    def NAND(self, a, b, quantum_register: QuantumRegister):
        binNumStr = str(a) + str(b) + str(1)
        binNum = int(binNumStr, 2)
        states = [0] * len(quantum_register.amps)
        states[binNum] = 1
        return np.dot(T, np.matrix(states).T)

    def doPeresGate(self, quantum_register: QuantumRegister):
        quantum_register.applyGate(T)
        quantum_register.applyGate(self.service.tensor(CNOT, ID))
        return quantum_register

    def doMTSGGate(self, quantum_register: QuantumRegister):
        """
        Implementation of quantum circuitry from:
        http://ijarcet.org/wp-content/uploads/IJARCET-VOL-4-ISSUE-4-1382-1386.pdf
        """
        # 1st op: v(b, d)
        quantum_register.applyGate(self.service.tensor(ID, SWAP, ID))
        quantum_register.applyGate(self.service.tensor(ID, ID, CV))
        quantum_register.applyGate(self.service.tensor(ID, SWAP, ID))
        # 2nd op: v(a, d)
        quantum_register.applyGate(self.service.tensor(SWAP, ID, ID))
        quantum_register.applyGate(self.service.tensor(ID, SWAP, ID))
        quantum_register.applyGate(self.service.tensor(ID, ID, CV))
        quantum_register.applyGate(self.service.tensor(ID, SWAP, ID))
        quantum_register.applyGate(self.service.tensor(SWAP, ID, ID))
        # 3rd op: cnot(a, b)
        quantum_register.applyGate(self.service.tensor(CNOT, ID, ID))
        # 4th op:
        quantum_register.applyGate(self.service.tensor(ID, ID, CV))
        self.logger.info('After CV[3]: %s' % quantum_register.amps.T)
        # 5th op:
        quantum_register.applyGate(self.service.tensor(ID, CNOT, ID))
        # 6th op:
        quantum_register.applyGate(self.service.tensor(ID, ID, CVPLUS))
        self.logger.info('After CPLUS: %s' % quantum_register.amps.T)

    def measure(self, r, q):
        oneProb, zeroProb = self.getProbsForQubit(r, q, r.amps[:])
        oneProb = abs(oneProb)
        zeroProb = abs(zeroProb)

        if(oneProb > 0.999):
            return 1
        elif(zeroProb > 0.999):
            return 0
        else:
            print('Undefinite state detected: probabilistic collapse needed')
            zeroProb = math.ceil(zeroProb * 100)
            oneProb = math.ceil(oneProb * 100)
            probs = [0] * int(zeroProb) + [1] * int(oneProb)  # int stops floats
            choice = random.choice(probs)
            return choice

    def measureMQubits(self, r, d_length=0):
        for i in range(len(r.amps)):
            if (r.amps[i].real.item(0) > self.ONE_LOWER_TOLERANCE):
                return self.service.getBinNum(i, d_length)

    # Apply a gate to a register

    def select(self, r, off, n_qubits):
        selection = []
        for i in range(off, n_qubits + 1):
            selection.append(i)
        return selection

    def getProbsForQubit(self, r, q, amps, oneProb=0.0, zeroProb=0.0):
        self.logger.info('Current qubit: %d' % q)
        self.logger.info(r.amps)
        for index in range(0, len(r.amps)):
            bin_n = self.service.getBinNum(index, r.n_qubits)
            bin_n = list(reversed(bin_n))
            self.logger.info('Bin number for index: %s' % bin_n)
            self.logger.info('bin_n[q]: %d' % bin_n[q])
            if bin_n[q] == 1:   # If there is a 1 in column of index & mask
                oneProb += amps[index] * amps[index]
            else:
                zeroProb += amps[index] * amps[index]
        self.logger.info('oneProb: %s, zeroProb: %s, qbit(%d)' % (oneProb, zeroProb, q))
        return (oneProb, zeroProb)

    def getAvgToAddFromOldStates(self, r, q, np_state, pStates=0, carry=0):
        for index in range(0, len(r.amps)):
            bin_n = self.service.getBinNum(index)
            if (bin_n[q] == np_state):
                carry += r.amps[index]
                r.amps[index] = 0
            elif (bin_n[q] != np_state and r.amps[index] != 0):
                pStates = pStates + 1
        avgToAdd = carry / pStates * carry / pStates
        return (avgToAdd, carry, pStates)

    def alterStates(self, r, q, np_state, pStates=0, carry=0):
        avgToAdd, carry, pStates = self.getAvgToAddFromOldStates(r, q, np_state)
        for index in range(0, len(r.amps)):
            bin_n = self.service.getBinNum(index)
            if (bin_n[q] != np_state and r.amps[index] != 0):
                r.amps[index] = r.amps[index] * r.amps[index] + avgToAdd

    def quantumOracle(self, function, r):
        "This is constant time on a quantum computer if f(x) is constant time"
        # We go in steps of 2 as the first qubit is not an input to our function
        for index in range(0, len(r.amps), 2):
            result = function(index // 2)  # Check if f(x) = balanced/constant
            #  print('result for ' + str(index) + ' // 2: ' + str(index // 2))
            if result == 1:
                r.amps[index] = - r.amps[index]
                r.amps[index + 1] = - r.amps[index + 1]

        print('After Uf (quantum oracle) applied: %s ' % r.amps.T)

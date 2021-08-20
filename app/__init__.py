from app.service import QuantumSimulatorService
from app.quantum_register import QuantumRegister

from app.quantum_gates import CNOT, HAD, ID

import numpy as np

# ONE_UPPER_TOLERANCE = 1.001

# DEBUG = False


    # def isOne(self, number):  # evaluates if our number is 1.0
    #     #  isOne = number > self.ONE_LOWER_TOLERANCE and \
    #     #    number < self.ONE_UPPER_TOLERANCE
    #     #  print('eval in isOne(): %s, for number: ' % isOne, number)
    #     return number > ONE_LOWER_TOLERANCE and \
    #         number < ONE_UPPER_TOLERANCE


# def checkProbs(l):
#     """
#     Checks if probabilities add to one in sufficient manner
#     """
#     probs = sum(abs(i)*abs(i) for i in l)
#     probs = probs.item(0)
#     assert probs < ONE_UPPER_TOLERANCE and probs > ONE_LOWER_TOLERANCE


# # Wrapper functions for quantum programming language SQASM
# def MEASURE(r):
#     ''' Measurement on a given register in a given range
#         r[0] = selection, r[1] = reg - Error handling for
#         other situations included '''
#     qs = QSimulator()

#     # Error handling for passing various value types from compiler
#     try:
#         selection = r[0]
#     except AttributeError:
#         selection = [0, r.n_qubits - 1]
#     try:
#         reg = r[1]
#     except AttributeError:
#         reg = r

#     res = []

#     print("Amount of amplitudes in register %s" % len(reg.amps))
#     print('selection range: %s' % selection)
#     begin = selection[0]
#     end = selection[1] + 1

#     for i in range(begin, end):
#         res.append(qs.measure(reg, i))

#     print('RES: %s' % res)  # Reads left to right in order of qubits
#     return res


# def SELECT(r, begin, end):
#     qs = QSimulator()
#     return (qs.select(r, begin, end), r)


# def INITIALIZE(n, pos):
#     return QuantumRegister(int(n), pos)


# def APPLY(gate, qreg):
#     qs = QSimulator()
#     qreg.applyGate(gate)
#     return qreg


# def ADD(a, b):
#     r = QuantumRegister(BIT_ARITHMETIC_AMOUNT)  # 16 bit addition
#     adder = Adder()
#     adder.setAdderBinaryValues(a, b)
#     log('a: %s, b: %s' % (adder.bin_1, adder.bin_2))
#     qs = QSimulator()
#     r, res = adder.rippleCarryAdder(BIT_ARITHMETIC_AMOUNT, qs)
#     log('ADD RESULT: %s + %s = %s' % (a, b, res))
#     assert res == a + b
#     print('SUCCESS: ADD')
#     return r


# def PEEK(r):
#     return r.amps

# # Deutsch's algorithm functions
# def alwaysZero(value):
#     return 0


# def alwaysOne(value):
#     return 1


# def isOdd(value):
#     #  print('value & 1 inside isOdd is: ' + str(value & 1))
#     return (value & 1)


# def isEven(value):
#     #  print('(value ^ 1) & 1 is: ' + str((value ^ 1) & 1))
#     return (value ^ 1) & 1


# functionList = [
#     (alwaysZero, "AlwaysZero"),
#     (alwaysOne, "AlwaysOne"),
#     (isOdd, "isOdd"),
#     (isEven, "isEven")
# ]


# Testing functions
# def adderTest(adder, qs, k=0):
#     print('BEGINNING ADDER TEST... DONE')
#     n1 = 10
#     n2 = 12
#     adder.setAdderBinaryValues(n1, n2)
#     log("Trying to do %s + %s" % (n1, n2))
#     log('a: %s' % adder.bin_1)
#     log('b: %s' % adder.bin_2)
#     r, res = adder.rippleCarryAdder(BIT_ARITHMETIC_AMOUNT, qs)
#     print('ADD RESULT: %s + %s = %s' % (n1, n2, res))
#     assert res == n1 + n2
#     k = k + 1
#     print('TEST PASSED 16-BIT QUANTUM RIPPLE CARRY ADDER')
#     return res


# def multiplierTest(qs, k=0):
#     print('\nBEGINNING MULTIPLIER TEST... DONE')
#     for i in range(3):
#         a1 = 9 + i
#         b1 = 9 + i
#         n1, n2 = m.prepMultiplier(a1, b1, 4)  # a1,b1 -> binary
#         res = m.applyMultiplier(qs, n1, n2)
#         print('MUL R: %s = %s * %s' % (res, bArrToDec(n1), bArrToDec(n2)))
#         assert res == a1 * b1
#         k = k + 1
#         log('Successful results: %s' % k)
#         print('TEST PASSED 4-BIT MULTIPLIER')


def MTSGGateTest(self, qs):
    for i in range(pow(2, 4)):
        r = QuantumRegister(4, i)
        qs.doMTSGGate(r)
        inp = self.service.getBinNum(i, 4)
        out = qs.measureMQubits(r, 4)
        self.logger.info('MTSG[%s] R: %s' % (inp, out))
    print('MTSG Gate Test SUCCESSFUL')


def peresGateTest(self, qs):
    ''' PERES: TOF (C, B, A), flips A bit if C & B are set
               CNOT(C, B), flips B bit if C is set
        Image of circuit:
        http://www.informatik.uni-bremen.de/rev_lib/doc/real/peres_9.jpg '''

    # PERES gate truth table
    tt = np.matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 1, 0],
                   [1, 1, 1], [1, 0, 1], [1, 0, 0]])

    for i in range(pow(2, 3)):
        r = QuantumRegister(3, i)  # iterating over all possibilities, i.e. 000, 001, ...
        qs.doPeresGate(r)  # apply the peres gate to those possibilities
        inp = self.service.getBinNum(i, 3)  # Our binary representation input we began with
        out = qs.measureMQubits(r, 3)  # Our binary result after PERES gate
        self.logger.info('PERES[%s] R: %s' % (inp, out))  # log the result
        assert out == tt[i].tolist()[0]  # Check against the truth table
    print('PERES TEST SUCCESSFUL!')


# def qsimDeutschTest(self, qs):
#     """
#     David Deutsch's Algorithm (1992)
#     """
#     for function, name in functionList:
#         quantum_register = QuantumRegister(4, 0)
#         print("Beginning amps: %s" % quantum_register.amps.T)
#         quantum_register.applyGate(self.service.tensor(HAD, ID, ID, ID))
#         quantum_register.applyGate(self.service.tensor(ID, HAD, ID, ID))
#         quantum_register.applyGate(self.service.tensor(ID, ID, HAD, ID))
#         quantum_register.applyGate(self.service.tensor(ID, ID, ID, HAD))
#         print("After hadding all bits: %s" % quantum_register.amps.T)

#         qs.quantumOracle(function, quantum_register)

#         quantum_register.applyGate(self.service.tensor(HAD, ID, ID, ID))
#         quantum_register.applyGate(self.service.tensor(ID, HAD, ID, ID))
#         quantum_register.applyGate(self.service.tensor(ID, ID, HAD, ID))
#         quantum_register.applyGate(self.service.tensor(ID, ID, ID, HAD))
#         print("After hadding all bits again: %s" % quantum_register.amps.T)
#         functionChanges = False

#         for qubit in range(4):
#             functionChanges |= (qs.measure(quantum_register, qubit) == 1)

#         if functionChanges:
#             print("FOUND RESULT: %s is balanced\n" % name)
#         else:
#             print("FOUND RESULT: %s is constant\n" % name)


# def wrapperTests():
#     r = ADD(15, 35)
#     MEASURE(([0, 15], r))  # Somehow need to verify this

# def runTests(qs, adder, m):
#     print('BEGINNING TESTS... DONE')
#     # adderTest(adder, qs)
#     multiplierTest(qs)
#     # peresGateTest(qs)
#     # MTSGGateTest(qs)
#     # qsimDeutschTest(qs)
#     # wrapperTests()
#     print('END OF TESTS... DONE')


def pretty(reg, y=0):
    x = "{0:b}".format(reg.argmax())
    zeroes = ''
    y = y + 2 if reg.argmax() <= 1 else y + 1 if reg.argmax() <= 3 else 0

    for _ in range(y):
        zeroes = zeroes + '0'

    return str('|' + zeroes + str(x) + '>')

quantum_simulator_service = QuantumSimulatorService()

if __name__ == "__main__":
    quantum_simulator_service.get_quantum_entanglement_system()

    # adder = Adder()
    # m = Multiplier()
    # qs = QSimulator()

    # Bell states demonstration - Entanglement of states
    # Init state |00>

    # SWAP gate demonstration on two qubit system
    # reg = QReg(2, 2)  # Init state |00>
    # print(reg.amps.T)  # Before swap
    # qs.applyGate(SWAP, reg)  # Apply SWAP gate
    # print(reg.amps.T)  # After swap

    # Classical computation NAND gate demonstration
    # reg = QReg(3)
    # print('NAND |001> -> %s' % pretty(qs.NAND(0, 0, QReg(3)).T))
    # print('NAND |011> -> %s' % pretty(qs.NAND(0, 1, QReg(3)).T))
    # print('NAND |101> -> %s' % pretty(qs.NAND(1, 0, QReg(3)).T))
    # print('NAND |111> -> %s' % pretty(qs.NAND(1, 1, QReg(3)).T))

    # -- TESTING - #
    # runTests(qs, adder, m)

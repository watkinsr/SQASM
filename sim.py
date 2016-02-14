#!/usr/bin/env python
# encoding: utf-8

from cmath import sqrt
import random
import numpy as np
import math
import time

# Quantum Simulator - Ryan Watkins
# MIT LICENCE

ONE_LOWER_TOLERANCE = 0.999
ONE_UPPER_TOLERANCE = 1.001
BIT_ARITHMETIC_AMOUNT = 16
DEBUG = False

# TODO: Fix multiplier - produce graphs of registers used and time spent in
# processing tests..


"""
Quantum Gate Matrices
"""

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


class QReg:
    def __init__(self, n_qubits, setVal=-1):
        self.n_qubits = n_qubits
        self.qubits = [0] * n_qubits
        # in this classical simulation, we use 2^n_qubits complex numbers
        self.amps = [0] * (1 << n_qubits)
        self.amps[len(self.amps) - 1] = 1
        if (setVal != -1):
            self.amps[setVal] = 1
            if (setVal != len(self.amps) - 1):
                self.amps[len(self.amps) - 1] = 0
        self.amps = np.matrix(self.amps).T

    def getState(self, qs):
        return qs.measureMQubits(self.amps)


class QSimulator:
    def NAND(self, a, b, r):
        binNumStr = str(a) + str(b) + str(1)
        binNum = int(binNumStr, 2)
        states = [0] * len(r.amps)
        states[binNum] = 1
        return self.applyGate(self.T, np.matrix(states).T)

    def doPeresGate(self, r):
        self.applyGate(T, r)
        self.applyGate(t(CNOT, ID), r)
        return r

    def doMTSGGate(self, r):
        """
        Implementation of quantum circuitry from:
        http://ijarcet.org/wp-content/uploads/IJARCET-VOL-4-ISSUE-4-1382-1386.pdf
        """
        # 1st op: v(b, d)
        self.applyGate(t(ID, SWAP, ID), r)
        self.applyGate(t(ID, ID, CV), r)
        self.applyGate(t(ID, SWAP, ID), r)
        # 2nd op: v(a, d)
        self.applyGate(t(SWAP, ID, ID), r)
        self.applyGate(t(ID, SWAP, ID), r)
        self.applyGate(t(ID, ID, CV), r)
        self.applyGate(t(ID, SWAP, ID), r)
        self.applyGate(t(SWAP, ID, ID), r)
        # 3rd op: cnot(a, b)
        self.applyGate(t(CNOT, ID, ID), r)
        # 4th op:
        self.applyGate(t(ID, ID, CV), r)
        log('After CV[3]: %s' % r.amps.T)
        # 5th op:
        self.applyGate(t(ID, CNOT, ID), r)
        # 6th op:
        self.applyGate(t(ID, ID, CVPLUS), r)
        log('After CPLUS: %s' % r.amps.T)

    def measure(self, r, q):
        oneProb, zeroProb = self.getProbsForQubit(r, q, r.amps[:])
        oneProb = abs(oneProb)
        zeroProb = abs(zeroProb)

        if(oneProb > 0.999):
            return 1  # self.alterStates(r, q, 0)
        elif(zeroProb > 0.999):
            return 0  # self.alterStates(r, q, 1)
        else:
            print('Undefinite state detected: probabilistic collapse needed')
            zeroProb = math.ceil(zeroProb * 100)
            oneProb = math.ceil(oneProb * 100)
            # int makes sure we haven't got a float...
            probs = [0] * int(zeroProb) + [1] * int(oneProb)
            choice = random.choice(probs)
            return choice

    def measureMQubits(self, r, d_length=0):
        # st = time.clock()
        # for i in range(len(r.qubits)):
        # self.measure(r, r.qubits[i])
        # end = time.clock()
        # print('Time spent measuring all qubits of register: %s' % (end-st))
        for i in range(len(r.amps)):
            if (r.amps[i].real.item(0) > ONE_LOWER_TOLERANCE):
                return getBinNum(i, d_length)

# Apply a gate to a register
    def applyGate(self, u, r):
        r.amps = np.dot(u, r.amps)

    def select(self, r, off, n_qubits):
        selection = []
        for i in range(off, n_qubits + 1):
            selection.append(i)
        return selection

    def getProbsForQubit(self, r, q, amps, oneProb=0.0, zeroProb=0.0):
        log('Current qubit: %d' % q)
        log(r.amps)
        for index in range(0, len(r.amps)):
            bin_n = getBinNum(index, r.n_qubits)
            bin_n = list(reversed(bin_n))
            log('Bin number for index: %s' % bin_n)
            log('bin_n[q]: %d' % bin_n[q])
            if bin_n[q] == 1:   # If there is a 1 in column of index & mask
                oneProb += amps[index] * amps[index]
            else:
                zeroProb += amps[index] * amps[index]
        log('oneProb: %s, zeroProb: %s, qbit(%d)' % (oneProb, zeroProb, q))
        return (oneProb, zeroProb)

    def getAvgToAddFromOldStates(self, r, q, np_state, pStates=0, carry=0):
        for index in range(0, len(r.amps)):
            bin_n = getBinNum(index)
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
            bin_n = getBinNum(index)
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

    def isOne(self, number):  # evaluates if our number is 1.0
        #  isOne = number > self.ONE_LOWER_TOLERANCE and \
        #    number < self.ONE_UPPER_TOLERANCE
        #  print('eval in isOne(): %s, for number: ' % isOne, number)
        return number > ONE_LOWER_TOLERANCE and \
            number < ONE_UPPER_TOLERANCE


class Adder:
    def __init__(self):
        self.aOuts = [None] * BIT_ARITHMETIC_AMOUNT  # AOut in QAdder Paper
        self.bOuts = [None] * BIT_ARITHMETIC_AMOUNT  # bOuts in QA Paper
        self.sOuts = []  # output sums
        self.tZeros = [None] * BIT_ARITHMETIC_AMOUNT  # TODO
        self.bZero = 0   # TODO
        self.bin_1 = None
        self.bin_2 = None
        self.regs = []

    def clearVars(self):
        self.aOuts = []  # AOut in QAdder Paper
        self.bOuts = []  # bOuts in QA Paper
        self.sOuts = []  # output sums
        self.tZeros = []
        self.bZero = 0
        self.regs = []

    def rippleCarryAdderPreProcess(self, b1, b2, isSubtract):
        """
        Preprocess values so that continual adders can be applied
        and also utilize twos compliment in event of subtraction
        on the adder
        """
        self.clearVars()
        minusStr = self.minusStr(isSubtract)
        log('Beginning addition for: %s + (%s)%s' % (b1, minusStr, b2))

        if(isSubtract):
            b2 = self.twosCompliment(b2)
        return b2

    def rippleCarryAdder(self, nbits, qs, subtract=False, j=0):
        """
        Entirety of quantum adder processing is here,
        qs = Quantum Simulator, bin_1 = binary number 1,
        bin_2 = binary number 2, number of bits to perform addition on
        {tZero, aOuts, bOuts, bZero} are all outputs of implementation
        sOuts means outputs used for summation at the end...
        """
        #  TODO: make tZeros, aOuts & bOuts their own regs.

        log("bin_1: %s" % self.bin_1)
        log("bin_2: %s" % self.bin_2)

        # Preprocess to deal with subtraction edge case
        self.rippleCarryAdderPreProcess(self.bin_1, self.bin_2, subtract)
        log("BEGIN QFA PART OF QUANTUM RIPPLE CARRY ADDER")
        self.doQRCFullAdderPart(BIT_ARITHMETIC_AMOUNT, qs)
        self.sOuts.append(self.bOuts[0])  # Stores bOuts[0] for summation later
        self.logQFAOuts()

        log("BEGIN QMAJORITY PART OF QUANTUM RIPPLE ADDER")
        for i in range(1, nbits):
            tZero = self.tZeros[i]
            r = self.getQMAReg(tZero, self.aOuts[i], self.bOuts[i], self.bZero)

            self.applyQuantumMajorityGate(r, qs)

            # Measure and check results..
            m = qs.measureMQubits(r, nbits)
            log('After QMAJ: %s\n' % m)
            self.bZero = m[nbits - 4]

            self.sOuts.append(m[nbits - 2])

        log('Sums: %s' % self.sOuts)

        # Begin summation part..
        negBit = [self.sOuts[0]]

        for i in range(nbits - 1):
            negBit.append(0)

        negBit = int(''.join(map(str, negBit)), 2)
        self.sOuts[0] = 0

        # Joins all the sums
        # TODO: Should be a quantum operation
        result = int(''.join(map(str, self.sOuts)), 2)

        r = QReg(BIT_ARITHMETIC_AMOUNT, result)
        if (subtract):
            return (r, result + -(negBit))
        else:
            return (r, result + negBit)

    def doQRCFullAdderPart(self, nbits, qs):
        """
        Do Quantum Ripple Carry Full Adder processing
        """
        j = 0
        for i in range(nbits - 1, -1, -1):
            # Get the Quantum Full Adder Register by giving the ith element
            # of the binary numbers, bZero is the first element
            # We end up with a register like so: [bZero, bin1, bin2, 0]
            r = self.getQFAReg(self.bin_1[i], self.bin_2[i], self.bZero, j, 4)

            log('QFA Reg Begin: %s' % r.amps.T)

            self.applyQuantumFullAdder(r, qs)  # Do actual gate operations

            # Check if our quantum full adder worked.
            m = qs.measureMQubits(r, 4)
            log('After QFA: %s\n' % m)

            # Store vals for Quantum Majority Gate portion of implementation
            self.storeQFAValues(m)
            j += 1  # for iterative purposes

    def getQFAReg(self, a, b, bZero, j, nbits):
        bState = [str(bZero), str(a), str(b), str(0)]
        bState = ''.join(bState)
        state = int(bState, 2)
        log('QReg[%s]: %s' % (j, bState))
        r = QReg(nbits, state)
        self.regs.append(r)
        return r

    def logQFAOuts(self):
        log('tZeros: %s' % self.tZeros)
        log('aOuts: %s' % self.aOuts)
        log('bOuts: %s' % self.bOuts)
        log('bZero: %s' % self.bZero)

    def storeQFAValues(self, m):
        """
         Store vals to plug back into our Quantum Majority Gate portion of
        implementation
        """
        self.tZeros.insert(0, m[0])
        self.aOuts.append(m[1])
        self.bOuts.insert(0, m[2])
        self.bZero = m[3]

    def twosCompliment(self, b):
        bState = ''.join(map(str, b))
        state = int(bState, 2)
        print('Initial state before inversion: %s' % bState)
        r = QReg(4, state)
        qs.applyGate(t(NOT, ID, ID, ID), r)
        qs.applyGate(t(ID, NOT, ID, ID), r)
        qs.applyGate(t(ID, ID, NOT, ID), r)
        qs.applyGate(t(ID, ID, ID, NOT), r)
        m = qs.measureMQubits(r, 4)
        print("Measurement inside twosCompliment(): %s" % m)

        # res = APPLY([0, 0, 0, 1], m, 4, False)  # add one @end
        res = getBinNum(res, 4)
        log('After INVERT: %s' % res)
        return res

    def minusStr(self, isSubtract):
        if(isSubtract):
            return '-'

    def testQFA(self, qs):
        """
        Test against Table 2 - Quantum Full Adder - paper ref (below)
        """
        tt = np.matrix([[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0],
                        [0, 1, 1, 0], [1, 1, 1, 0], [1, 0, 1, 0], [0, 0, 1, 0],
                        [0, 1, 0, 1], [1, 1, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1],
                        [1, 0, 1, 1], [0, 0, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]])
        for i in range(16):
            r = QReg(4, i)
            self.qfadder(r)
            inp = getBinNum(i, 4)[::-1]
            out = qs.measureMQubits(r, 4)[::-1]
            print('QFA[%s] R: %s' % (inp, out))
            assert out == tt[i].tolist()[0]

    def setAdderBinaryValues(self, n1, n2):
        bitsAvailable = pow(2, BIT_ARITHMETIC_AMOUNT - 1)
        if (n1 >= bitsAvailable or n2 >= bitsAvailable):
            raise Exception('Value error: Integer too big for addition')
        self.bin_1 = getBinNum(n1, BIT_ARITHMETIC_AMOUNT)
        self.bin_2 = getBinNum(n2, BIT_ARITHMETIC_AMOUNT)

    def testAdder(res, n1, n2):
        print('ADD RESULT: %s' % res)
        assert res == n1 + n2
        print('SUCCESSFUL RESULT \n\n')

    def applyQuantumMajorityGate(self, r, qs):
        qs.applyGate(t(ID, T), r)  # 1st op - Toffoli (b, c, d)
        qs.applyGate(t(ID, CNOT, ID), r)  # 2nd op - CNOT (b, c)
        qs.applyGate(t(ID, SWAP, ID), r)  # sw(b, c) -> (a, c, b, d)
        qs.applyGate(t(ID, ID, SWAP), r)  # sw(b, d) -> (a, c, d, b)
        qs.applyGate(t(T, ID), r)  # tof(a, c, d)
        qs.applyGate(t(ID, ID, SWAP), r)  # sw(b, d) -> (a, c, b, d)
        qs.applyGate(t(ID, SWAP, ID), r)  # sw(c, b) -> (a, b, c, d)
        qs.applyGate(t(ID, CNOT, ID), r)  # 4th op - CNOT (b, c)

    def getQMAReg(self, tZero, a, b, bZero):
        bState = [str(tZero), str(a), str(b), str(bZero)]
        bState = ''.join(bState)
        state = int(bState, 2)
        r = QReg(4, state)
        return r

    def applyQuantumFullAdder(self, r, qs):
        """
        Quantum full adder implementation ref:
        http://arxiv.org/pdf/quant-ph/9808061.pdf
        """
        qs.applyGate(t(ID, T), r)  # 1st op - TOF(b, c, d)
        qs.applyGate(t(ID, CNOT, ID), r)  # 2nd op - CNOT(b, c)

        # 3rd op: TOF(A, C, D), => SWAP B & C, SWAP B & D, SWAP BACK
        qs.applyGate(t(ID, SWAP, ID), r)
        qs.applyGate(t(ID, ID, SWAP), r)
        qs.applyGate(t(T, ID), r)

        # Now we need to swap d & b, then c and b and we're back to normal
        qs.applyGate(t(ID, ID, SWAP), r)
        qs.applyGate(t(ID, SWAP, ID), r)

        # 4th op - need to swap b & c and back again after cnot(a, c)
        qs.applyGate(t(ID, SWAP, ID), r)
        qs.applyGate(t(CNOT, ID, ID), r)
        qs.applyGate(t(ID, SWAP, ID), r)


class Multiplier():
    def __init__(self):
        self.regs = []
        self.sumRegs = []

    def applyMultiplier(self, qs, b1, b2, l=0, m=0, prevRes=0):
        ''' Fig 9. Fig. 10 from paper: http://ijarcet.org/?page_id=3143
            for part1 and part2 respectively                            '''

        log('Applying multiplication to: %s * %s' % (b1, b2))
        bLength = len(b1)  # Get length of binary values passed in
        log('bLength: %s' % bLength)

        # Partial Product Generation (Using PERES Gate to generate AND gate)
        # Does PERES gate, line by line (x[j], y[i])
        # x0 is b1[0], y0 is b2[0]
        for i in range(bLength - 1, -1, -1):
            m = 0  # Used to keep track of variables in logging
            for j in range(bLength - 1, -1, -1):
                r = self.prepAND(b1[j], b2[i], i)
                log('Begin state x[%s]y[%s]: %s ' % (m, l, r.amps.T))
                r = qs.doPeresGate(r)
                log('After PERES x[%s]y[%s]: %s\n' % (m, l, r.amps.T))
                m += 1
                if (j == 0):
                    s = []  # s is the sum array of the and operations

                    for k in range(bLength - 1, -1, -1):
                        print("Reg accessed for sum: %s" % (k + (l * bLength)))
                        m = qs.measureMQubits(self.regs[k+(l * bLength)],
                                              bLength - 1)
                        print("Measurement on reg %s" % m)
                        print("Sum is appending val: %s" % (m[bLength - 4 + 2]))
                        s.append(m[bLength - 4 + 2])
                    for p in range(l):  # amount to start of binary
                        s.append(0)
                    for p in range(bLength - l - 1):
                        s.insert(0, 0)

                    l = l + 1

                    # Creates a new quantum register to store sums
                    self.sumRegs.append(QReg(bLength + l, bArrToDec(s)))
                    log('Summation of (%s)th line: %s\n' % (l, s))

        print('REGISTERS USED IN PART ONE: %s\n' % (len(self.regs)
                                                    + len(self.sumRegs)))
        print('STARTING PART TWO')
        self.regs = []
        for i in range(len(self.sumRegs) - 1):
            st = time.clock()
            if(prevRes == 0):
                # st2 = time.clock()
                a = qs.measureMQubits(self.sumRegs[i], bLength)
                # end2 = time.clock()
                # print('Time elapsed measuring a: %s' % (end2-st2))
            else:
                a = getBinNum(prevRes, bLength)
            # st2 = time.clock()
            b = qs.measureMQubits(self.sumRegs[i + 1], bLength)
            # end2 = time.clock()
            # print('Time elapsed measuring b: %s' % (end2-st2))
            print('a: %s' % a)
            print('b: %s' % b)
            adder.setAdderBinaryValues(bArrToDec(a), bArrToDec(b))
            r, prevRes = adder.rippleCarryAdder(BIT_ARITHMETIC_AMOUNT, qs)
            end = time.clock()
            print('Time elapsed for cycle[%s] in P2: %s' % (i, end-st))
        res = prevRes
        self.sumRegs = []
        return res

    def getState(self, i1, i2, i3=0, i4=0):
        if (i3 == 0):
            return int(''.join([str(i1), str(i2)]), 2)
        elif (i4 == 0):
            return int(''.join([str(i1), str(i2), str(i3)]), 2)
        else:
            return int(''.join([str(i1), str(i2), str(i3), str(i4)]), 2)

    def prepMultiplier(self, n1, n2, b_amount=4):
            print('Starting multiplier with bit amount: %s' % b_amount)
            b1 = getBinNum(n1, b_amount)
            b2 = getBinNum(n2, b_amount)
            return b1, b2

    def prepAND(self, a, b, j):
        bState = [str(a), str(b), str(0)]
        bState = ''.join(bState)
        state = int(bState, 2)
        log('QReg[%s]: %s' % (j, bState))
        r = QReg(3, state)  # Note: [1 0 0 0 0 0 0 0] - means 000
        self.regs.append(r)  # Saving reg for later use
        return r


# Various ancillary functions
def t(f1, f2, f3=0, f4=0):
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


def bArrToDec(ba):
    return int(''.join(map(str, ba)), 2)


def dec_to_bin(x):
    return int(bin(x)[2:])


def fixBinToDec(x, d_length):
    if (len(x) < d_length):
        amountToPad = d_length - len(x)
        for i in range(amountToPad):
            x.insert(0, 0)
        return x
    else:
        return x


def getBinNum(x, d_length=0):
    if (d_length == 0):
        d_length = len(bin(x))
    bin_n = [int(i) for i in str(dec_to_bin(x))]
    return fixBinToDec(bin_n, d_length)


def log(s):
    # For debugging purposes
    if DEBUG:
        print(s)


def checkProbs(l):
    """
    Checks if probabilities add to one in sufficient manner
    """
    probs = sum(abs(i)*abs(i) for i in l)
    probs = probs.item(0)
    assert probs < ONE_UPPER_TOLERANCE and probs > ONE_LOWER_TOLERANCE


# Wrapper functions for quantum programming language SQASM
def MEASURE(r):
    ''' Measurement on a given register in a given range
        r[0] = selection, r[1] = reg - Error handling for
        other situations included '''
    qs = QSimulator()

    # Error handling for passing various value types from compiler
    try:
        selection = r[0]
    except AttributeError:
        selection = [0, r.n_qubits - 1]
    try:
        reg = r[1]
    except AttributeError:
        reg = r

    res = []

    print("Amount of amplitudes in register %s" % len(reg.amps))
    print('selection range: %s' % selection)
    begin = selection[0]
    end = selection[1] + 1

    for i in range(begin, end):
        res.append(qs.measure(reg, i))

    print('RES: %s' % res)  # Reads left to right in order of qubits
    return res


def SELECT(r, begin, end):
    qs = QSimulator()
    return (qs.select(r, begin, end), r)


def INITIALIZE(n):
    return QReg(int(n))


def APPLY(gate, qreg):
    qs = QSimulator()
    qs.applyGate(gate, qreg)
    return qreg


def ADD(a, b):
    r = QReg(BIT_ARITHMETIC_AMOUNT)  # 16 bit addition
    t0 = time.clock()
    adder = Adder()
    adder.setAdderBinaryValues(a, b)
    log('a: %s, b: %s' % (adder.bin_1, adder.bin_2))
    qs = QSimulator()
    r, res = adder.rippleCarryAdder(BIT_ARITHMETIC_AMOUNT, qs)
    print('Elapsed time for add: %ss' % (time.clock() - t0))
    log('ADD RESULT: %s + %s = %s' % (a, b, res))
    assert res == a + b
    print('SUCCESS: ADD')
    return r


# Deutsch's algorithm functions
def alwaysZero(value):
    return 0


def alwaysOne(value):
    return 1


def isOdd(value):
    #  print('value & 1 inside isOdd is: ' + str(value & 1))
    return (value & 1)


def isEven(value):
    #  print('(value ^ 1) & 1 is: ' + str((value ^ 1) & 1))
    return (value ^ 1) & 1


functionList = [
    (alwaysZero, "AlwaysZero"),
    (alwaysOne, "AlwaysOne"),
    (isOdd, "isOdd"),
    (isEven, "isEven")
]


# Testing functions
def adderTest(adder, qs, k=0):
    print('BEGINNING ADDER TEST... DONE')
    n1 = 7
    n2 = 7
    adder.setAdderBinaryValues(n1, n2)
    log("Trying to do %s + %s" % (n1, n2))
    log('a: %s' % adder.bin_1)
    log('b: %s' % adder.bin_2)
    r, res = adder.rippleCarryAdder(BIT_ARITHMETIC_AMOUNT, qs)
    print('ADD RESULT: %s + %s = %s' % (n1, n2, res))
    assert res == n1 + n2
    k = k + 1
    print('TEST PASSED 4-BIT QUANTUM RIPPLE CARRY ADDER')
    return res


def multiplierTest(qs, k=0):
    print('\nBEGINNING MULTIPLIER TEST... DONE')
    for i in range(3):
        a1 = 9 + i
        b1 = 9 + i
        n1, n2 = m.prepMultiplier(a1, b1, 4)  # Creates binary versions of a1,b1
        res = m.applyMultiplier(qs, n1, n2)
        print('MUL R: %s = %s * %s' % (res, bArrToDec(n1), bArrToDec(n2)))
        assert res == a1 * b1
        k = k + 1
        log('Successful results: %s' % k)
        print('TEST PASSED 4-BIT MULTIPLIER')


def MTSGGateTest(qs):
    for i in range(pow(2, 4)):
        r = QReg(4, i)
        qs.doMTSGGate(r)
        inp = getBinNum(i, 4)
        out = qs.measureMQubits(r, 4)
        log('MTSG[%s] R: %s' % (inp, out))
    print('MTSG Gate Test SUCCESSFUL')


def peresGateTest(qs):
    ''' PERES: TOF (C, B, A), flips A bit if C & B are set
               CNOT(C, B), flips B bit if C is set
        Image of circuit:
        http://www.informatik.uni-bremen.de/rev_lib/doc/real/peres_9.jpg '''

    # PERES gate truth table
    tt = np.matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 1, 0],
                   [1, 1, 1], [1, 0, 1], [1, 0, 0]])

    for i in range(pow(2, 3)):
        r = QReg(3, i)  # iterating over all possibilities, i.e. 000, 001, ...
        qs.doPeresGate(r)  # apply the peres gate to those possibilities
        inp = getBinNum(i, 3)  # Our binary representation input we began with
        out = qs.measureMQubits(r, 3)  # Our binary result after PERES gate
        log('PERES[%s] R: %s' % (inp, out))  # log the result
        assert out == tt[i].tolist()[0]  # Check against the truth table
    print('PERES TEST SUCCESSFUL!')


def qsimDeutschTest(qs):
    """
    David Deutsch's Algorithm (1992)
    """
    for function, name in functionList:
        r = QReg(4, 0)
        print("Beginning amps: %s" % r.amps.T)
        qs.applyGate(t(HAD, ID, ID, ID), r)
        qs.applyGate(t(ID, HAD, ID, ID), r)
        qs.applyGate(t(ID, ID, HAD, ID), r)
        qs.applyGate(t(ID, ID, ID, HAD), r)
        print("After hadding all bits: %s" % r.amps.T)

        qs.quantumOracle(function, r)

        qs.applyGate(t(HAD, ID, ID, ID), r)
        qs.applyGate(t(ID, HAD, ID, ID), r)
        qs.applyGate(t(ID, ID, HAD, ID), r)
        qs.applyGate(t(ID, ID, ID, HAD), r)
        print("After hadding all bits again: %s" % r.amps.T)
        functionChanges = False

        for qubit in range(4):
            functionChanges |= (qs.measure(r, qubit) == 1)

        if functionChanges:
            print("FOUND RESULT: %s is balanced\n" % name)
        else:
            print("FOUND RESULT: %s is constant\n" % name)


def wrapperTests():
    r = ADD(15, 35)
    MEASURE(([0, 15], r))  # Somehow need to verify this


def runTests(qs, adder, m):
    print('BEGINNING TESTS... DONE')
    adderTest(adder, qs)
    multiplierTest(qs)
    peresGateTest(qs)
    MTSGGateTest(qs)
    qsimDeutschTest(qs)
    wrapperTests()
    print('END OF TESTS... DONE')


if __name__ == "__main__":
    adder = Adder()
    m = Multiplier()
    qs = QSimulator()

    # -- TESTING -- #
    runTests(qs, adder, m)

    print('Starting up quantum simulator...   DONE')

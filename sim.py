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


# Tensor product for up to three functions
def t(f1, f2, f3=0, f4=0):
    if(type(f3) is int):
        return np.kron(f1, f2)
    elif(type(f4) is int):
        u = np.kron(f1, f2)
        return np.kron(u, f3)
    else:
        u = np.kron(f1, f2)
        u = np.kron(u, f3)
        return np.kron(u, f4)


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

# Quantum Gate Matrices
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


def doPeresGate(r, qs):
    qs.applyGate(T, r)
    qs.applyGate(t(CNOT, ID), r)
    return r


# Taken from quantum representation in paper
# http://ijarcet.org/wp-content/uploads/IJARCET-VOL-4-ISSUE-4-1382-1386.pdf
def doMTSGGate(r, qs):
    # 1st op: v(b, d)
    qs.applyGate(t(ID, SWAP, ID), r)
    qs.applyGate(t(ID, ID, CV), r)
    qs.applyGate(t(ID, SWAP, ID), r)
    # 2nd op: v(a, d)
    qs.applyGate(t(SWAP, ID, ID), r)
    qs.applyGate(t(ID, SWAP, ID), r)
    qs.applyGate(t(ID, ID, CV), r)
    qs.applyGate(t(ID, SWAP, ID), r)
    qs.applyGate(t(SWAP, ID, ID), r)
    # 3rd op: cnot(a, b)
    qs.applyGate(t(CNOT, ID, ID), r)
    # 4th op:
    qs.applyGate(t(ID, ID, CV), r)
    log('After CV[3]: %s' % r.amps.T)
    # 5th op:
    qs.applyGate(t(ID, CNOT, ID), r)
    # 6th op:
    qs.applyGate(t(ID, ID, CVPLUS), r)
    log('After CPLUS: %s' % r.amps.T)


def MTSGGateTest(qs):
    for i in range(pow(2, 4)):
        r = QReg(4, i)
        doMTSGGate(r, qs)
        inp = getBinNum(i, 4)
        out = qs.measureMQubits(r, 4)
        log('MTSG[%s] R: %s' % (inp, out))
    print('MTSG Gate Test SUCCESSFUL')


def bArrToDec(ba):
    return int(''.join(map(str, ba)), 2)


def peresGateTest(qs):
    tt = np.matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 1, 0],
                    [1, 1, 1], [1, 0, 1], [1, 0, 0]])

    for i in range(pow(2, 3)):
        r = QReg(3, i)
        doPeresGate(r, qs)
        inp = getBinNum(i, 3)
        out = qs.measureMQubits(r, 3)
        log('PERES[%s] R: %s' % (inp, out))
        assert out == tt[i].tolist()[0]
    print('PERES TEST SUCCESSFUL!')


# Select subset of qubits from register
def dec_to_bin(x):
    return int(bin(x)[2:])


def log(s):
    if DEBUG:
        print(s)


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


class QSimulator:
    def NAND(self, a, b, r):
        binNumStr = str(a) + str(b) + str(1)
        binNum = int(binNumStr, 2)
        states = [0] * len(r.amps)
        states[binNum] = 1
        return self.applyGate(self.T, np.matrix(states).T)

    def measure(self, r, q):
        oneProb, zeroProb = self.getProbsForQubit(r, q, r.amps[:])
        oneProb = abs(oneProb)
        zeroProb = abs(zeroProb)

        if(oneProb > 0.999):
            return 1  # self.alterStates(r, q, 0)
        elif(zeroProb > 0.999):
            return 0  # self.alterStates(r, q, 1)
        else:
            zeroProb = math.ceil(zeroProb * 100)
            oneProb = math.ceil(oneProb * 100)
            probs = [0] * zeroProb + [1] * oneProb
            choice = random.choice(probs)
            # if (choice == 0):
            # self.alterStates(r, q, 1)
            # else:
            # self.alterStates(r, q, 0)
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
        for index in range(0, len(r.amps)):
            bin_n = getBinNum(index)
            if bin_n[q] == 1:   # If there is a 1 in column of index & mask
                oneProb += amps[index] * amps[index]
            else:
                zeroProb += amps[index] * amps[index]

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


def qaDeutsch(qs):
    r = INITIALIZE(3)
    qs.applyGate(t(HAD, ID, ID, ID), r)
    qs.applyGate(t(ID, HAD, ID, ID), r)
    qs.applyGate(t(ID, ID, HAD, ID), r)
    qs.applyGate(t(ID, ID, ID, HAD), r)
    m = qs.measureMQubits(r)
    print(m)


def INITIALIZE(n):
    return QReg(n)


# QAssembly chapter 7.2 Quantum Computing for Computer Scientists
def tryAssemblyInstructions(qs):
    r = QReg(2)
    res = [0, 0]
    while(res != [1, 0]):
        qs.applyGate(t(qs.ID, qs.HAD), r)
        print('After instruction: APPLY U R: %s' % r.amps)
        s1 = qs.select(r, 1, 1)
        print('After Instruction: SELECT S1 R 1 1: %s' % s1)
        res = qs.measure(r, s1[0])
        print('After Instruction: MEASURE S1 RES: %s' % res)
        qs.applyGate(qs.CNOT, r)
        print('After Instruction: APPLY CNOT R: %s' % r.amps)
        res = qs.measureMQubits(r)
        print('After Instruction: MEASURE R RES: %s' % res)


class Adder:
    def __init__(self):
        self.aOuts = []
        self.bOuts = []
        self.sOuts = []
        self.tZeros = []
        self.bZero = 0
        self.regs = []

    def clearVars(self):
        self.aOuts = []
        self.bOuts = []
        self.sOuts = []
        self.tZeros = []
        self.bZero = 0
        self.regs = []

    def applyAdder(self, qs, b1, b2, nbits, subtract=False):
        #  TODO: make tZeros, aOuts & bOuts their own regs.
        self.clearVars()
        minusStr = self.minusStr(subtract)
        log('Beginning addition for: %s + (%s)%s' % (b1, minusStr, b2))
        j = 0
        if(subtract):
            b2 = self.twoscompliment(b2, subtract)
        log("BEGIN QFA PART OF QUANTUM RIPPLE ADDER")
        for i in range(nbits - 1, -1, -1):
            r = self.prepQFA(b1[i], b2[i], self.bZero, j, 4)
            log('After prepQFA: %s' % r.amps.T)
            self.qfadder(r, qs)
            m = qs.measureMQubits(r, 4)

            log('After QFA: %s\n' % m)

            self.tZeros.insert(0, m[0])
            self.aOuts.append(m[1])
            self.bOuts.insert(0, m[2])
            self.bZero = m[3]

            j = j + 1

        self.sOuts.append(self.bOuts[0])
        log('tZeros: %s' % self.tZeros)
        log('aOuts: %s' % self.aOuts)
        log('bOuts: %s' % self.bOuts)
        log('bZero: %s' % self.bZero)

        log("BEGIN QMAJORITY PART OF QUANTUM RIPPLE ADDER")

        for i in range(1, nbits):
            tZero = self.tZeros[i]
            r = self.preQMA(tZero, self.aOuts[i], self.bOuts[i], self.bZero)
            self.qmaj(r, qs)
            m = qs.measureMQubits(r, nbits)
            log('After QMAJ: %s\n' % m)
            self.bZero = m[nbits - 4 + 0]

            self.sOuts.append(m[nbits - 4 + 2])

        log('Sums: %s' % self.sOuts)

        negBit = [self.sOuts[0]]

        for i in range(nbits - 1):
            negBit.append(0)

        negBit = int(''.join(map(str, negBit)), 2)
        self.sOuts[0] = 0
        result = int(''.join(map(str, self.sOuts)), 2)

        if (subtract):
            return result + -(negBit)
        else:
            return result + negBit

    # Taken from: cs stackexchange paper
    def qfadder2(self, r, qs):
        qs.applyGate(t(qs.T, qs.ID), r)
        qs.applyGate(t(qs.CNOT, qs.ID, qs.ID), r)
        qs.applyGate(t(qs.ID, qs.ID, qs.SWAP), r)
        qs.applyGate(t(qs.ID, qs.T), r)
        qs.applyGate(t(qs.ID, qs.CNOT, qs.ID), r)
        print('QFA RESULT: %s' % r.amps.T)

    def prepQFA(self, a, b, bZero, j, nbits):
        bState = [str(bZero), str(a), str(b), str(0)]
        bState = ''.join(bState)
        state = int(bState, 2)
        log('QReg[%s]: %s' % (j, bState))
        r = QReg(nbits, state)
        self.regs.append(r)
        return r

    def twosCompliment(self, b, qs):
        bState = ''.join(map(str, b))
        state = int(bState, 2)
        log('Initial state before inversion: %s' % bState)
        r = QReg(4, state)
        qs.applyGate(t(qs.NOT, qs.ID, qs.ID, qs.ID), r)
        qs.applyGate(t(qs.ID, qs.NOT, qs.ID, qs.ID), r)
        qs.applyGate(t(qs.ID, qs.ID, qs.NOT, qs.ID), r)
        qs.applyGate(t(qs.ID, qs.ID, qs.ID, qs.NOT), r)
        m = qs.measureMQubits(r, 4)
        res = apply([0, 0, 0, 1], m, 4, False)  # add one @end
        res = getBinNum(res, 4)
        log('After INVERT: %s' % res)
        return res

    def minusStr(self, isSubtract):
        if(isSubtract):
            return '-'

    # Test against Table 2 - Quantum Full Adder - paper ref (below)
    def testQFA(self, qs):
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

    def prepAdder(self, n1, n2):
        bitsAvailable = pow(2, BIT_ARITHMETIC_AMOUNT - 1)
        if (n1 >= bitsAvailable or n2 >= bitsAvailable):
            raise Exception('Value error: Integer too big for addition')
        b1 = getBinNum(n1, BIT_ARITHMETIC_AMOUNT)
        b2 = getBinNum(n2, BIT_ARITHMETIC_AMOUNT)

        return b1, b2

    def testAdder(res, n1, n2):
        print('ADD RESULT: %s' % res)
        assert res == n1 + n2
        print('SUCCESSFUL RESULT \n\n')

    def qmaj(self, r, qs):
        qs.applyGate(t(ID, T), r)  # 1st op - Toffoli (b, c, d)
        qs.applyGate(t(ID, CNOT, ID), r)  # 2nd op - CNOT (b, c)
        qs.applyGate(t(ID, SWAP, ID), r)  # sw(b, c) -> (a, c, b, d)
        qs.applyGate(t(ID, ID, SWAP), r)  # sw(b, d) -> (a, c, d, b)
        qs.applyGate(t(T, ID), r)  # tof(a, c, d)
        qs.applyGate(t(ID, ID, SWAP), r)  # sw(b, d) -> (a, c, b, d)
        qs.applyGate(t(ID, SWAP, ID), r)  # sw(c, b) -> (a, b, c, d)
        qs.applyGate(t(ID, CNOT, ID), r)  # 4th op - CNOT (b, c)

    def preQMA(self, tZero, a, b, bZero):
        bState = [str(tZero), str(a), str(b), str(bZero)]
        bState = ''.join(bState)
        state = int(bState, 2)
        r = QReg(4, state)
        return r

    # Quantum full adder from paper: http://arxiv.org/pdf/quant-ph/9808061.pdf
    def qfadder(self, r, qs):
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
        log('Doing multiplication for: %s * %s' % (b1, b2))
        bLength = len(b1)
        log('bLength: %s' % bLength)
        # AND GATE(PERES) part
        for i in range(bLength - 1, -1, -1):
            m = 0
            for j in range(bLength - 1, -1, -1):
                r = self.prepAND(b1[j], b2[i], i)
                log('Begin state x[%s]y[%s]: %s ' % (m, l, r.amps.T))
                r = doPeresGate(r, qs)
                log('After PERES x[%s]y[%s]: %s\n' % (m, l, r.amps.T))
                m = m + 1
                if (j == 0):
                    s = []

                    for k in range(bLength - 1, -1, -1):
                        m = qs.measureMQubits(self.regs[k+(l * bLength)],
                                              bLength - 1)
                        s.append(m[bLength - 4 + 2])
                    for p in range(l):  # amount to start of binary
                        s.append(0)
                    for p in range(bLength - l - 1):
                        s.insert(0, 0)

                    l = l + 1
                    self.sumRegs.append(QReg(bLength + l, bArrToDec(s)))
                    log('Summation of (%s)th line: %s\n' % (l, s))

        print('REGISTERS USED IN PART ONE: %s\n' % (len(self.regs)
                                                    + len(self.sumRegs)))
        print('STARTING PART TWO')
        self.regs = []
        for i in range(len(self.sumRegs) - 1):
            st = time.clock()
            if(prevRes == 0):
                st2 = time.clock()
                a = qs.measureMQubits(self.sumRegs[i], bLength)
                end2 = time.clock()
                print('Time elapsed measuring a: %s' % (end2-st2))
            else:
                a = getBinNum(prevRes, bLength)
            st2 = time.clock()
            b = qs.measureMQubits(self.sumRegs[i + 1], bLength)
            end2 = time.clock()
            print('Time elapsed measuring b: %s' % (end2-st2))
            print('a: %s' % a)
            print('b: %s' % b)
            prevRes = adder.applyAdder(qs, a, b, bLength)
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
        r = QReg(3, state)
        self.regs.append(r)
        return r


if __name__ == "__main__":

    adder = Adder()
    m = Multiplier()

    def adderTest(k=0):
        print('BEGINNING ADDER TEST... DONE')
        n1 = 250
        n2 = 250
        a, b = adder.prepAdder(n1, n2)
        log('a: %s' % a)
        log('b: %s' % b)
        res = adder.applyAdder(qs, a, b, BIT_ARITHMETIC_AMOUNT)
        print('ADD RESULT: %s + %s = %s' % (n1, n2, res))
        assert res == n1 + n2
        k = k + 1
        print('TEST PASSED 4-BIT QUANTUM RIPPLE CARRY ADDER')
        return res

    print('Starting up quantum simulator...   DONE')

    def multiplierTest(k=0, prevRes=0):
        print('\nBEGINNING MULTIPLIER TEST... DONE')
        for i in range(10, 30):
            a1 = i
            b1 = i
            n1, n2 = m.prepMultiplier(a1, b1, 11)
            res = m.applyMultiplier(qs, n1, n2)
            print('MUL R: %s = %s * %s' % (res, bArrToDec(n1), bArrToDec(n2)))
            assert res == a1 * b1
            k = k + 1
        log('Successful results: %s' % k)
        print('TEST PASSED 4-BIT MULTIPLIER')

    def runTests(qs):
        print('BEGINNING TESTS... DONE')
        adderTest()
        # peresGateTest(qs)
        # MTSGGateTest(qs)
        multiplierTest()
        print('END OF TESTS... DONE')

    qs = QSimulator()
    runTests(qs)

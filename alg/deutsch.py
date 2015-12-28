#!/usr/bin/python

import math


class QuantumComputerSimulator:
    SQRT_2 = math.sqrt(2)
    ONE_LOWER_TOLERANCE = 0.999
    ONE_UPPER_TOLERANCE = 1.001

    def __init__(self, numberOfQubits, initialState, verbose):
        self.__state = [0.0 for _ in range(0, pow(2, numberOfQubits))]

        # Our quantum computer definitely starts in "initialState".
        self.__state[initialState] = 1.0
        self.__verbose = verbose
        self.log("Initial state")

    def applyHadamard(self, qubitIndex):
        "This is a constant time operation in a quantum computer."
        for index in range(0, len(self.__state), 2):
            zeroIndex = self.swapBits(0, qubitIndex, index)
            oneIndex = self.swapBits(0, qubitIndex, index + 1)

            zero = self.__state[zeroIndex]
            one = self.__state[oneIndex]

            self.__state[zeroIndex] = (zero + one) / self.SQRT_2
            self.__state[oneIndex] = (zero - one) / self.SQRT_2

        self.log("After Hadamard transformation on Qubit %s" % qubitIndex)

    def quantumOracle(self, function):
        "^ Is constant time on a quantum computer if function is constant time"
        # We go in steps of 2 as the first qubit is not an input to our function
        for index in range(0, len(self.__state), 2):
            result = function(index // 2)

            if result == 1:
                print("Result was 1 inside quantumOracle")
                self.__state[index] = -self.__state[index]
                self.__state[index + 1] = -self.__state[index + 1]

        self.log("After quantum oracle")

    def readQubit(self, qubit):
        mask = 1 << qubit
        zeroProb = 0.0
        oneProb = 0.0

        for index in range(0, len(self.__state)):
            stateProb = self.__state[index]
            stateProb *= stateProb
            if index & mask:  # if there is a 1 in column of index & mask
                oneProb += stateProb
            else:
                zeroProb += stateProb

        if not self.isOne(oneProb + zeroProb):
            message = \
                "Something went wrong. " + \
                "Total probability for a Qubit should be 1.0. " + \
                "Could be a rounding error."
            raise Exception(message)

        if self.isOne(oneProb):
            return True

        if self.isOne(zeroProb):
            return False

        # In reality, observing a qubit in a superposition (not definitely 1
        # or 0) would result in a 1 or 0, and all entangled Qubits would need
        # to be adjusted accordingly.
        raise Exception("Qubit is not in a known state.")

    def isOne(self, number):
        isOne = number > self.ONE_LOWER_TOLERANCE and \
            number < self.ONE_UPPER_TOLERANCE
        print('eval is isOne(): %s, for number: ' % isOne, number)
        return number > self.ONE_LOWER_TOLERANCE and \
            number < self.ONE_UPPER_TOLERANCE

    @staticmethod
    def swapBits(index1, index2, number):
        "Swap 2 bits in number, specified by index1 and index2"
        # mask for the required bits
        mask1 = number & (1 << index1)
        mask2 = number & (1 << index2)

        # Move them to the 1st bit
        bit1 = (mask1) >> index1
        bit2 = (mask2) >> index2

        # Zero out the bits in the number
        number ^= (mask1 | mask2)

        # Set the swapped bits
        number |= (bit1 << index2)
        number |= (bit2 << index1)

        return number

    def log(self, name):
        if self.__verbose:
            print("%s, %s" % (name, ", ".join(map(str, self.__state))))


def always0(value):
    return 0


def always1(value):
    return 1


def isOdd(value):
    return (value & 1)


def isEven(value):
    return (value ^ 1) & 1


def isConstantFunction(function, name, verbose):
    "This is the Deutsch-Jozsa algorithm"
    print('Running code on f(x) = ' + name)
    qubits = 3
    computer = QuantumComputerSimulator(qubits, 1, verbose)
    print('Starting simulator...')
    for qubit in range(0, qubits):
        computer.applyHadamard(qubit)

    computer.quantumOracle(function)

    for qubit in range(1, qubits):
        computer.applyHadamard(qubit)

    functionChanges = False

    for qubit in range(1, qubits):
        functionChanges |= computer.readQubit(qubit)

    if verbose:
        print("")

    if functionChanges:
        print("%s is balanced" % name)
    else:
        print("%s is constant" % name)

    if verbose:
        print

print('For ref.......-------!!!!!')


functionList = [
    (always0, "Always0"),
    (always1, "Always1"),
    (isOdd, "isOdd"),
    (isEven, "isEven")
]


for function, name in functionList:
    isConstantFunction(function, name, True)

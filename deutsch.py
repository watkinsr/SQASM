import math


class QuantumSystem:
    SQRT_2 = math.sqrt(2)
    zeroKets = []
    oneKets = []
    ONE_LOWER_TOLERANCE = 0.999
    ONE_UPPER_TOLERANCE = 1.001

    def __init__(self, n_qubits, initial_state, verbose):
        self.__state = [0.0 for _ in range(0, pow(2, n_qubits))]
        self.n_qubits = n_qubits
        self.__state[initial_state] = 1.0
        self.__verbose = verbose
        print("Initial state %s" % self.__state)

    def quantumOracle(self, function):
        "This is constant time on a quantum computer if f(x) is constant time"
        # We go in steps of 2 as the first qubit is not an input to our function
        for index in range(0, len(self.__state), 2):
            result = function(index // 2)  # Check if f(x) = balanced/constant
            #  print('result for ' + str(index) + ' // 2: ' + str(index // 2))
            if result == 1:
                self.__state[index] = - self.__state[index]
                self.__state[index + 1] = - self.__state[index + 1]

        print('After Uf (quantum oracle) applied: %s ' % self.__state)

    def getState(self):
        return self.__state

    def readQubit(self, qubit):
        #  print('Observing the qubit: ' + str(qubit))
        mask = 1 << qubit  # This identifies where a 1 is in our qubit binary
        zeroProb = 0.0
        oneProb = 0.0

        for index in range(0, len(self.__state)):
            stateProb = self.__state[index]
            stateProb *= stateProb  # Normalising procedure
            if index & mask:  # If there is a 1 in column of index & mask
                oneProb += stateProb
            else:
                zeroProb += stateProb

        if not self.isOne(oneProb + zeroProb):
            message = \
                "Something went wrong. " + \
                "Total probability for Qubit should be 1.0 " + \
                "Could be a rounding error."
            raise Exception(message)

        if self.isOne(oneProb):
            return True

        if self.isOne(zeroProb):
            return False

        raise Exception("Qubit is not in a known state.")

    def isOne(self, number):  # evaluates if our number is 1.0
        #  isOne = number > self.ONE_LOWER_TOLERANCE and \
        #    number < self.ONE_UPPER_TOLERANCE
        #  print('eval in isOne(): %s, for number: ' % isOne, number)
        return number > self.ONE_LOWER_TOLERANCE and \
            number < self.ONE_UPPER_TOLERANCE

    def logState(self, qubitIndex):
        print("H[q%s] State: " % qubitIndex, self.__state)

    def applyHadamard(self, qubitIndex):
        self.resetKets()
        self.processKetPairs(qubitIndex)

        for index in range(int(len(self.__state) / 2)):
            zeroIndex = self.zeroKets[index]
            oneIndex = self.oneKets[index]

            zero = self.__state[zeroIndex]
            one = self.__state[oneIndex]

            self.__state[zeroIndex] = (zero + one) / self.SQRT_2
            self.__state[oneIndex] = (zero - one) / self.SQRT_2

        self.logState(qubitIndex)

    def processKetPairs(self, qubitIndex):
        diff = pow(2, qubitIndex)  # diff between x and y, 2 ^ qubit
        end_num = 0  # num to increase by when we have done 2 ^ qubit + 1 calcs
        j = 0  # for incrementing inside
        loopAmount = (int(len(self.__state) / 2))
        for i in range(loopAmount):
            self.zeroKets.append(j + end_num)
            self.oneKets.append(j + end_num + diff)
            j = j + 1
            if (j == pow(2, qubitIndex)):
                end_num = self.oneKets[len(self.oneKets) - 1] + 1
                j = 0
        # print('zeroKets for qubit %s: %s' % (qubitIndex, self.zeroKets))
        # print('oneKets for qubit %s: %s' % (qubitIndex, self.oneKets))

    def resetKets(self):
        self.zeroKets = []
        self.oneKets = []

    def logPairs(self):
        print("Zero: " + str(self.zeroKets))
        print("One: " + str(self.oneKets))


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


def startSystem():
    print('---STARTING UP QUANTUM COMPUTER SIMULATION... DONE---')
    print('---MIT LICENCE - Ryan Watkins---\n')

    for function, name in functionList:
        runDeutschJozsaAlgorithm(function, name)


def runDeutschJozsaAlgorithm(function, name):
    print('---RUNNING DEUTSCH JOZSA ALGORITHM ON f(%s)---' % name)

    QUBIT_AMOUNT = 3
    qsim = QuantumSystem(QUBIT_AMOUNT, 0, True)

    for qubit in range(QUBIT_AMOUNT):
        qsim.applyHadamard(qubit)

    qsim.quantumOracle(function)

    for qubit in range(QUBIT_AMOUNT):
        qsim.applyHadamard(qubit)

    functionChanges = False

    for qubit in range(QUBIT_AMOUNT):
        functionChanges |= qsim.readQubit(qubit)

    if functionChanges:
        print("FOUND RESULT: %s is balanced\n" % name)
    else:
        print("FOUND RESULT: %s is constant\n" % name)


functionList = [
    (alwaysZero, "AlwaysZero"),
    (alwaysOne, "AlwaysOne"),
    (isOdd, "isOdd"),
    (isEven, "isEven")
]

startSystem()

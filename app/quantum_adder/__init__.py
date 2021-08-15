from app.service import QuantumSimulatorService
from app.quantum_register import QuantumRegister

from app.quantum_gates import ID, SWAP, CNOT, T
import logging

class Adder:
    def __init__(self):
        self.BIT_ARITHMETIC_AMOUNT = 16
        self.aOuts = [None] * self.BIT_ARITHMETIC_AMOUNT  # AOut in QAdder Paper
        self.bOuts = [None] * self.BIT_ARITHMETIC_AMOUNT  # bOuts in QA Paper
        self.sOuts = []  # output sums
        self.tZeros = [None] * self.BIT_ARITHMETIC_AMOUNT  # TODO
        self.bZero = 0   # TODO
        self.bin_1 = None
        self.bin_2 = None
        self.regs = []
        self.logger = logging.getLogger(__name__)
        self.quantum_simulator_service = QuantumSimulatorService()

    def clearVars(self):
        self.aOuts = []  # AOut in QAdder Paper
        self.bOuts = []  # bOuts in QA Paper
        self.sOuts = []  # output sums
        self.tZeros = []
        self.bZero = 0
        self.regs = []

    # def rippleCarryAdderPreProcess(self, b1, b2, isSubtract):
    #     """
    #     Preprocess values so that continual adders can be applied
    #     and also utilize twos compliment in event of subtraction
    #     on the adder
    #     """
    #     self.clearVars()
    #     minusStr = self.minusStr(isSubtract)
    #     self.logger.info(
    #         'Beginning addition for: %s + (%s)%s' % (b1, minusStr, b2)
    #     )

    #     if(isSubtract):
    #         b2 = self.twosCompliment(b2)
    #     return b2

    # def rippleCarryAdder(self, nbits, qs, subtract=False, j=0):
    #     """
    #     Entirety of quantum adder processing is here,
    #     qs = Quantum Simulator, bin_1 = binary number 1,
    #     bin_2 = binary number 2, number of bits to perform addition on
    #     {tZero, aOuts, bOuts, bZero} are all outputs of implementation
    #     sOuts means outputs used for summation at the end...
    #     """
    #     #  TODO: make tZeros, aOuts & bOuts their own regs.

    #     self.logger.info("bin_1: %s" % self.bin_1)
    #     self.logger.info("bin_2: %s" % self.bin_2)

    #     # Preprocess to deal with subtraction edge case
    #     self.rippleCarryAdderPreProcess(self.bin_1, self.bin_2, subtract)
    #     self.logger.info("BEGIN QFA PART OF QUANTUM RIPPLE CARRY ADDER")
    #     # self.doQRCFullAdderPart(self.BIT_ARITHMETIC_AMOUNT, qs)
    #     self.sOuts.append(self.bOuts[0])  # Stores bOuts[0] for summation later
    #     self.logQFAOuts()

    #     self.logger.info("BEGIN QMAJORITY PART OF QUANTUM RIPPLE ADDER")
    #     for i in range(1, nbits):
    #         tZero = self.tZeros[i]
    #         # Prepare a register for Quantum Majority Gate
    #         r = self.getQMAReg(tZero, self.aOuts[i], self.bOuts[i], self.bZero)

    #         self.applyQuantumMajorityGate(r, qs)

    #         # Measure and check results..
    #         m = qs.measureMQubits(r, nbits)
    #         self.logger.info('After QMAJ: %s\n' % m)
    #         self.bZero = m[nbits - 4]

    #         self.sOuts.append(m[nbits - 2])

    #     self.logger.info('Sums: %s' % self.sOuts)

    #     # Begin summation part..
    #     negBit = [self.sOuts[0]]

    #     for i in range(nbits - 1):
    #         negBit.append(0)

    #     negBit = int(''.join(map(str, negBit)), 2)
    #     self.sOuts[0] = 0

    #     # Joins all the sums
    #     result = int(''.join(map(str, self.sOuts)), 2)

    #     quantum_register = QuantumRegister(self.BIT_ARITHMETIC_AMOUNT, result)
    #     if (subtract):
    #         return (quantum_register, result + -(negBit))
    #     else:
    #         return (quantum_register, result + negBit)

    # def doQRCFullAdderPart(self, nbits, qs):
    #     """
    #     Do Quantum Ripple Carry Full Adder processing
    #     """
    #     j = 0
    #     for i in range(nbits - 1, -1, -1):
    #         # Get the Quantum Full Adder Register by giving the ith element
    #         # of the binary numbers, bZero is the first element
    #         # We end up with a register like so: [bZero, bin1, bin2, 0]
    #         r = self.getQFAReg(self.bin_1[i], self.bin_2[i], self.bZero, j, 4)

    #         self.logger.info('QFA Reg Begin: %s' % r.amps.T)

    #         self.applyQuantumFullAdder(r, qs)  # Do actual gate operations

    #         # Check if our quantum full adder worked.
    #         m = qs.measureMQubits(r, 4)
    #         self.logger.info('After QFA: %s\n' % m)

    #         # Store vals for Quantum Majority Gate portion of implementation
    #         self.storeQFAValues(m)
    #         j += 1  # for iterative purposes

    def getQFAReg(self, a, b, bZero, j, nbits):
        bState = [str(bZero), str(a), str(b), str(0)]
        bState = ''.join(bState)
        state = int(bState, 2)
        self.logger.info('QReg[%s]: %s' % (j, bState))
        r = QuantumRegister(nbits, state)
        self.regs.append(r)
        return r

    def logQFAOuts(self):
        self.logger.info('tZeros: %s' % self.tZeros)
        self.logger.info('aOuts: %s' % self.aOuts)
        self.logger.info('bOuts: %s' % self.bOuts)
        self.logger.info('bZero: %s' % self.bZero)

    def storeQFAValues(self, m):
        """
         Store vals to plug back into our Quantum Majority Gate portion of
        implementation
        """
        self.tZeros.insert(0, m[0])
        self.aOuts.append(m[1])
        self.bOuts.insert(0, m[2])
        self.bZero = m[3]

    # def twosCompliment(self, b):
    #     quantum_simulator = QuantumSimulator()
    #     bState = ''.join(map(str, b))
    #     state = int(bState, 2)
    #     print('Initial binary state before inversion: %s' % bState)
    #     print('Initial state before inversion: %s' % state)
    #     quantum_register = QuantumRegister(4, state)
    #     print("Prior to one's compliment, amps: %s" % quantum_register.amps.T)
    #     quantum_register.applyGate(self.quantum_simulator_service.tensor(NOT, ID, ID, ID))
    #     quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, NOT, ID, ID))
    #     quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, ID, NOT, ID))
    #     quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, ID, ID, NOT))
    #     print("One's compliment amps: %s" % quantum_register.amps.T)
    #     m = quantum_simulator.measureMQubits(quantum_register, 4)
    #     print("One's compliment: %s" % m)
    #     oc = int(''.join(map(str, m)), 2)
    #     ocPlusOne = oc + 1
    #     print("One's compliment integer value: %s" % oc)
    #     print("One's compliment plus one: %s" % ocPlusOne)
    #     res = self.quantum_simulator_service.getBinNum(ocPlusOne, self.BIT_ARITHMETIC_AMOUNT)
    #     self.logger.info('After INVERT: %s' % res)
    #     return res

    def minusStr(self, isSubtract):
        if(isSubtract):
            return '-'

    # def testQFA(self, qs):
    #     """
    #     Test against Table 2 - Quantum Full Adder - paper ref (below)
    #     """
    #     tt = np.matrix([[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0],
    #                     [0, 1, 1, 0], [1, 1, 1, 0], [1, 0, 1, 0], [0, 0, 1, 0],
    #                     [0, 1, 0, 1], [1, 1, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1],
    #                     [1, 0, 1, 1], [0, 0, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]])
    #     for i in range(16):
    #         r = QuantumRegister(4, i)
    #         self.qfadder(r)
    #         inp = getBinNum(i, 4)[::-1]
    #         out = qs.measureMQubits(r, 4)[::-1]
    #         print('QFA[%s] R: %s' % (inp, out))
    #         assert out == tt[i].tolist()[0]

    # def setAdderBinaryValues(self, n1, n2):
    #     bitsAvailable = pow(2, self.BIT_ARITHMETIC_AMOUNT - 1)
    #     if (n1 >= bitsAvailable or n2 >= bitsAvailable):
    #         raise Exception('Value error: Integer too big for addition')
    #     self.bin_1 = getBinNum(n1, self.BIT_ARITHMETIC_AMOUNT)
    #     self.bin_2 = getBinNum(n2, self.BIT_ARITHMETIC_AMOUNT)

    @staticmethod
    def testAdder(res, n1, n2):
        print('ADD RESULT: %s' % res)
        assert res == n1 + n2
        print('SUCCESSFUL RESULT \n\n')

    def applyQuantumMajorityGate(
        self,
        quantum_register: QuantumRegister
    ):
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, T))  # 1st op - Toffoli (b, c, d)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, CNOT, ID))  # 2nd op - CNOT (b, c)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, SWAP, ID))  # sw(b, c) -> (a, c, b, d)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, ID, SWAP))  # sw(b, d) -> (a, c, d, b)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(T, ID))  # tof(a, c, d)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, ID, SWAP))  # sw(b, d) -> (a, c, b, d)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, SWAP, ID))  # sw(c, b) -> (a, b, c, d)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, CNOT, ID))  # 4th op - CNOT (b, c)

    def getQMAReg(self, tZero, a, b, bZero):
        bState = [str(tZero), str(a), str(b), str(bZero)]
        bState = ''.join(bState)
        state = int(bState, 2)
        r = QuantumRegister(4, state)
        return r

    def applyQuantumFullAdder(
        self,
        quantum_register: QuantumRegister
    ):
        """
        Quantum full adder implementation ref:
        http://arxiv.org/pdf/quant-ph/9808061.pdf
        """
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, T))  # 1st op - TOF(b, c, d)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, CNOT, ID))  # 2nd op - CNOT(b, c)

        # 3rd op: TOF(A, C, D), => SWAP B & C, SWAP B & D, SWAP BACK
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, SWAP, ID))
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, ID, SWAP))
        quantum_register.applyGate(self.quantum_simulator_service.tensor(T, ID))

        # Now we need to swap d & b, then c and b and we're back to normal
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, ID, SWAP))
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, SWAP, ID))

        # 4th op - need to swap b & c and back again after cnot(a, c)
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, SWAP, ID))
        quantum_register.applyGate(self.quantum_simulator_service.tensor(CNOT, ID, ID))
        quantum_register.applyGate(self.quantum_simulator_service.tensor(ID, SWAP, ID))

from app.service import QuantumSimulatorService
from app.quantum_register import QuantumRegister
import logging


class QuantumMultiplier():
    def __init__(self):
        self.regs = []
        self.sumRegs = []
        self.logger = logging.getLogger(__name__)
        self.quantum_simulator_service = QuantumSimulatorService()

    # def applyMultiplier(self, qs, b1, b2, l=0, m=0, prevRes=0):
    #     ''' Fig 9. Fig. 10 from paper: http://ijarcet.org/?page_id=3143
    #         for part1 and part2 respectively                            '''

    #     self.logger.info('Applying multiplication to: %s * %s' % (b1, b2))
    #     bLength = len(b1)  # Get length of binary values passed in
    #     self.logger.info('bLength: %s' % bLength)

    #     # Partial Product Generation (Using PERES Gate to generate AND gate)
    #     # Does PERES gate, line by line (x[j], y[i])
    #     # x0 is b1[0], y0 is b2[0]
    #     for i in range(bLength - 1, -1, -1):
    #         m = 0  # Used to keep track of variables in logging
    #         for j in range(bLength - 1, -1, -1):
    #             r = self.prepAND(b1[j], b2[i], i)
    #             self.logger.info('Begin state x[%s]y[%s]: %s ' % (m, l, r.amps.T))
    #             r = qs.doPeresGate(r)
    #             self.logger.info('After PERES x[%s]y[%s]: %s\n' % (m, l, r.amps.T))
    #             m += 1
    #             if (j == 0):
    #                 s = []  # s is the sum array of the and operations

    #                 for k in range(bLength - 1, -1, -1):
    #                     self.logger.info("Reg accessed for sum: %s" % (k + (l * bLength)))
    #                     m = qs.measureMQubits(self.regs[k+(l * bLength)],
    #                                           bLength - 1)
    #                     self.logger.info("Measurement on reg %s" % m)
    #                     self.logger.info("Sum is appending val: %s" % (m[bLength - 4 + 2]))
    #                     s.append(m[bLength - 4 + 2])
    #                 for p in range(l):  # amount to start of binary
    #                     s.append(0)
    #                 for p in range(bLength - l - 1):
    #                     s.insert(0, 0)

    #                 l = l + 1

    #                 # Creates a new quantum register to store sums
    #                 self.sumRegs.append(QuantumRegister(bLength + l, self.quantum_simulator_service.bArrToDec(s)))
    #                 self.logger.info('Summation of (%s)th line: %s\n' % (l, s))

    #     print('REGISTERS IN P1: %s' % (len(self.regs) + len(self.sumRegs)))
    #     self.regs = []
    #     for i in range(len(self.sumRegs) - 1):
    #         if(prevRes == 0):
    #             a = qs.measureMQubits(self.sumRegs[i], bLength)
    #         else:
    #             a = self.quantum_simulator_service.getBinNum(prevRes, bLength)
    #         b = qs.measureMQubits(self.sumRegs[i + 1], bLength)
    #         self.logger.info('a: %s' % a)
    #         self.logger.info('b: %s' % b)
    #         adder.setAdderBinaryValues(bArrToDec(a), bArrToDec(b))
    #         r, prevRes = adder.rippleCarryAdder(BIT_ARITHMETIC_AMOUNT, qs)
    #     res = prevRes
    #     self.sumRegs = []
    #     return res

    def getState(self, i1, i2, i3=0, i4=0):
        if (i3 == 0):
            return int(''.join([str(i1), str(i2)]), 2)
        elif (i4 == 0):
            return int(''.join([str(i1), str(i2), str(i3)]), 2)
        else:
            return int(''.join([str(i1), str(i2), str(i3), str(i4)]), 2)

    def prepMultiplier(self, n1, n2, b_amount=4):
            print('\nBEGIN MULTIPLIER[%s bits]' % b_amount)
            b1 = self.quantum_simulator_service.getBinNum(n1, b_amount)
            b2 = self.quantum_simulator_service.getBinNum(n2, b_amount)
            return b1, b2

    def prepAND(self, a, b, j):
        bState = [str(a), str(b), str(0)]
        bState = ''.join(bState)
        state = int(bState, 2)
        self.logger.info('QReg[%s]: %s' % (j, bState))
        r = QuantumRegister(3, state)  # Note: [1 0 0 0 0 0 0 0] - means 000
        self.regs.append(r)  # Saving reg for later use
        return r

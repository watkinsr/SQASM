#include <assert.h>
#include <stdlib.h>
#include <Eigen/Dense>
#include <iostream>

using Eigen::MatrixXd;

/*
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
*/

class QReg
{
public:
    QReg(size_t _numQubits, int _val)
    {
        numQubits = _numQubits;
        qubits = (int *)calloc(sizeof(int), _numQubits);
        assert(qubits);
        amps = (int *)calloc(sizeof(int), _numQubits);
        assert(amps);

        for (int i = 0; i < (1 << numQubits); i++)
        {
            amps[i] = 0;
        }
        amps[numQubits - 1] = 1;
        if (_val != -1)
        {
            amps[_val] = 1;
            if (_val != numQubits - 1)
            {
                amps[numQubits - 1] = 0;
            }
        }

        MatrixXd m(2, 2);
        m(0, 0) = 3;
        m(1, 0) = 2.5;
        m(0, 1) = -1;
        m(1, 1) = m(1, 0) + m(0, 1);

        std::cout << m << std::endl;
    }

private:
    int numQubits;
    int *qubits;
    int *amps;
};
#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <complex>

using namespace std;

class QReg
{
public:
    QReg(size_t numberOfQubits, int init_bit)
    {
        numberOfQubits = numberOfQubits;
        qubits = (int *)calloc(sizeof(int), numberOfQubits);
        numberOfAmplitudes = (1 << numberOfQubits);

        vector<vector<complex<double>>> matrix_(numberOfAmplitudes, vector<complex<double>>(1));
        amplitude_matrix = matrix_;

        amplitude_matrix[init_bit][0] = 1;

        // Initialize hadamard gate
        vector<vector<complex<double>>> HAD_GATE_(2, vector<complex<double>>(2));
        HAD_GATE = HAD_GATE_;

        HAD_GATE[0][0] = 1 / sqrt(2);
        HAD_GATE[0][1] = 1 / sqrt(2);
        HAD_GATE[1][0] = 1 / sqrt(2);
        HAD_GATE[1][1] = -1 / sqrt(2);
    }

    void applyGate();

private:
    int numberOfQubits;
    int *qubits;
    vector<vector<complex<double>>> amplitude_matrix;
    vector<vector<complex<double>>> HAD_GATE;



};

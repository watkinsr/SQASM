#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <complex>

using namespace std;

class QReg
{
public:
    QReg(size_t numberOfQubits)
    {
        numberOfQubits = numberOfQubits;
        qubits = (int *)calloc(sizeof(int), numberOfQubits);
        int numberOfAmplitudes = (1 << numberOfQubits);
        printf("Number of qubits: %zu\n", numberOfQubits);
        printf("Number of amplitudes: %i\n", numberOfAmplitudes);

        vector<vector<complex<double>>> matrix_(numberOfAmplitudes, vector<complex<double>>(1));
        amplitude_matrix = matrix_;

        // Default set last value as 1.
        amplitude_matrix[numberOfAmplitudes - 1][0] = 1;

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

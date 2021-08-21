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

        HAD_GATE =
            {
                {1 / sqrt(2), 1 / sqrt(2)},
                {1 / sqrt(2), -1 / sqrt(2)}
            };

        ID_GATE =
            {
                {1, 0},
                {0, 1}
            };

        CNOT_GATE =
            {
                {1, 0, 0, 0},
                {0, 1, 0, 0},
                {0, 0, 0, 1},
                {0, 0, 1, 0}
            };
    }

    void applyGate(vector<vector<complex<double>>> gate);
    vector<vector<complex<double>>> dot_product_amplitudes(vector<vector<complex<double>>> gate);
    void printAmplitudes();
    vector<vector<complex<double>>> tensor(vector<vector<complex<double>>> A, vector<vector<complex<double>>> B);
    vector<vector<complex<double>>> HAD_GATE;
    vector<vector<complex<double>>> ID_GATE;
    vector<vector<complex<double>>> CNOT_GATE;
    void printGate(vector<vector<complex<double>>> gate);

private:
    int numberOfQubits;
    int numberOfAmplitudes;
    int *qubits;
    vector<vector<complex<double>>> amplitude_matrix;
};

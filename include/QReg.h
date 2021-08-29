#pragma once

#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <complex>

using namespace std;

using QuantumGate = vector<vector<complex<double>>>;

class QReg
{
public:
    QReg(size_t numberOfQubits, int init_bit)
    {
        numberOfQubits = numberOfQubits;
        qubits = (int *)calloc(sizeof(int), numberOfQubits);
        numberOfAmplitudes = (1 << numberOfQubits);

        QuantumGate matrix_(numberOfAmplitudes, vector<complex<double>>(1));
        amplitude_matrix = matrix_;

        amplitude_matrix[init_bit][0] = 1;
    }

    void applyGateToSystem(QuantumGate gate);
    QuantumGate dot_product_amplitudes(QuantumGate gate);
    void printAmplitudes();
    static QuantumGate tensor(QuantumGate A, QuantumGate B);
    const static QuantumGate HAD_GATE;
    const static QuantumGate ID_GATE;
    const static QuantumGate CNOT_GATE;
    static void printGate(QuantumGate gate);

    static QuantumGate getGateByString(const char* gate);

private:
    int numberOfQubits;
    int numberOfAmplitudes;
    int *qubits;
    vector<vector<complex<double>>> amplitude_matrix;
};

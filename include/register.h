#pragma once

#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <complex>

using QuantumGate = std::vector<std::vector<std::complex<double>>>;

class Register {
    private:
        int mNumberOfQubits;
        int mNumberOfAmplitudes;
        int *mQubits;
        QuantumGate mAmpMatrix;
    public:
        Register(size_t qubitSize, int initBit);
        void apply(QuantumGate gate);
        QuantumGate dot_product_amplitudes(QuantumGate gate);
        void printAmplitudes();
        static QuantumGate tensor(QuantumGate A, QuantumGate B);
        const static QuantumGate HAD_GATE;
        const static QuantumGate ID_GATE;
        const static QuantumGate CNOT_GATE;
        const static QuantumGate NO_GATE;
        static void printGate(QuantumGate gate);
        static QuantumGate getGate(const char* gate);
};

#include "register.h"
#include <cstring>
#include <stdexcept>

Register::Register(size_t qubitSize, int initBit) {
    mNumberOfQubits = qubitSize;
    mQubits = (int *)calloc(sizeof(int), mNumberOfQubits);
    mNumberOfAmplitudes = (1 << mNumberOfQubits);
    QuantumGate matrix_(mNumberOfAmplitudes, std::vector<std::complex<double>>(1));
    _amplitudes = matrix_;
    _amplitudes[initBit][0] = 1;
}

void Register::apply(QuantumGate B) {
    LOG_INFO("[TRACE] Register::apply(?)");

    if (_amplitudes.size() != B.size()) {
        fprintf(stdout, "Unable to apply. Expected GATE to match Register size: %i\n", _amplitudes.size());
        return;
    }

    QuantumGate C(mNumberOfAmplitudes, std::vector<std::complex<double>>(1));

    // Dot Product Formula: The element 𝐶𝑖𝑗 in the resulting matrix 𝐶 is computed by:
    //                      taking the dot product of the i-th row of matrix 𝐴
    //                      with the j-th column of matrix 𝐵
    for (size_t i = 0; i < _amplitudes.size(); ++i) {
        for (size_t j = 0; j < _amplitudes.size(); ++j) {
            C[i][0] += B[i][j] * _amplitudes[j][0];
        }
    }
    _amplitudes = std::move(C);
}

QuantumGate Register::tensor(QuantumGate A, QuantumGate B) {
    QuantumGate C(4, std::vector<std::complex<double>>(4));
    int i = 0;
    int j = 0;
    int n = 0;
    int m = 0;  // How many times through A rows.

    for (auto rowA: A) {
        for (auto valueA: rowA) {
            for (auto rowB : B) {
                int k = j; // save j calculated below
                for (auto valueB : rowB) {
                    C[i][j] = valueA * valueB;
                    j++;
                }
                j = k;
                i++;
            }
            n++; // How many times have we been through B.

            i = m * 2;

            if (n % 2 == 0) {
                j = 0;
            } else {
                j = 2;
            }
        }
        m++;
        i = m * 2;
    }

    return C;
}

void Register::printGate(QuantumGate gate) {
    for (auto row: gate) {
        for (auto value: row) {
            std::cout << value << ' ';
        }
        printf("\n");
    }
    printf("\n");
}

void Register::printAmplitudes() {
    std::cout << "System: ";
    for (auto row: _amplitudes) {
        for (auto column: row) {
            std::cout << column << ' ';
        }
    }
    printf("\n");
}

QuantumGate Register::getGate(const char* gate) {
    if (strcmp(gate, "HAD") == 0) {
        return Register::HAD_GATE;
    } else if (strcmp(gate, "ID") == 0) {
        return Register::ID_GATE;
    } else if (strcmp(gate, "CNOT") == 0) {
        return Register::CNOT_GATE;
    } else {
        return Register::NO_GATE;
    }
}

const QuantumGate Register::CNOT_GATE = {
    {1, 0, 0, 0},
    {0, 1, 0, 0},
    {0, 0, 0, 1},
    {0, 0, 1, 0}
};

const QuantumGate Register::NO_GATE = {
    {0, 0, 0, 0},
    {0, 0, 0, 0},
    {0, 0, 0, 0},
    {0, 0, 0, 0}
};

const QuantumGate Register::ID_GATE = {
    {1, 0},
    {0, 1}
};

const QuantumGate Register::HAD_GATE = {
    {1 / sqrt(2), 1 / sqrt(2)},
    {1 / sqrt(2), -1 / sqrt(2)}
};

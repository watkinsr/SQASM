#include "../include/QReg.h"
#include <cstring>
#include <stdexcept>

using namespace std;

void QReg::applyGateToSystem(vector<vector<complex<double>>> gate) {
    amplitude_matrix = dot_product_amplitudes(gate);
}

vector<vector<complex<double>>> QReg::tensor(vector<vector<complex<double>>> A, vector<vector<complex<double>>> B)
{

    vector<vector<complex<double>>> C(4, vector<complex<double>>(4));

    int i = 0;
    int j = 0;

    int n = 0;

    int m = 0;  // How many times through A rows.

    for (auto rowA: A)
    {
        for (auto valueA: rowA)
        {
            for (auto rowB : B)
            {
              int k = j; // save j calculated below
              for (auto valueB : rowB)
              {
                  C[i][j] = valueA * valueB;
                  j++;
              }
              j = k;
              i++;
            }
            n++; // How many times have we been through B.

            i = m * 2;

            if (n % 2 == 0)
            {
                j = 0;
            }
            else
            {
                j = 2;
            }
        }
        m++;
        i = m * 2;
    }

    return C;
}

vector<vector<complex<double>>> QReg::dot_product_amplitudes(vector<vector<complex<double>>> gate) {
    int j = 0;
    int k = 0;

    vector<vector<complex<double>>> C(numberOfAmplitudes, vector<complex<double>>(1));

    for (auto rowGate: gate) {
        for (auto valueGate: rowGate) {
            auto ampValue = amplitude_matrix[j][0];
            C[k][0] += ampValue * valueGate;
            j++;
        }
        j = 0;
        k++;
    }

    return C;
}

void QReg::printGate(vector<vector<complex<double>>> gate) {
    for (auto row: gate) {
        for (auto value: row) {
            std::cout << value << ' ';
        }
        printf("\n");
    }
    printf("\n");
}

void QReg::printAmplitudes() {
    std::cout << "System: ";
    for (auto row: amplitude_matrix) {
        for (auto column: row) {
            std::cout << column << ' ';
        }
    }
    printf("\n");
}

vector<vector<complex<double>>> QReg::getGateByString(const char* gate)
{
    if (strcmp(gate, "HAD") == 0)
    {
        return QReg::HAD_GATE;
    }
    else if (strcmp(gate, "ID") == 0)
    {
        return QReg::ID_GATE;
    }
    else if (strcmp(gate, "CNOT") == 0)
    {
        return QReg::CNOT_GATE;
    }
    else
    {
        throw std::invalid_argument("invalid gate provided");
    }
}

const vector<vector<complex<double>>> QReg::CNOT_GATE =
{
    {1, 0, 0, 0},
    {0, 1, 0, 0},
    {0, 0, 0, 1},
    {0, 0, 1, 0}
};

const vector<vector<complex<double>>> QReg::ID_GATE =
{
    {1, 0},
    {0, 1}
};

const vector<vector<complex<double>>> QReg::HAD_GATE =
{
    {1 / sqrt(2), 1 / sqrt(2)},
    {1 / sqrt(2), -1 / sqrt(2)}
};

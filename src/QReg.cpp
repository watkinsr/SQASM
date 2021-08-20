#include "../include/QReg.h"

using namespace std;

void QReg::applyGate(vector<vector<complex<double>>> gate) {
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
    int k = 0;

    vector<vector<complex<double>>> C(numberOfAmplitudes, vector<complex<double>>(1));

    vector<vector<complex<double>>> temporary_gate_transposed(numberOfAmplitudes, vector<complex<double>>(1));

    for (auto row: gate) {
        for (auto column: row) {
            temporary_gate_transposed[k][0] = column;
            k++;
        }
    }

    k = 0;

    for (auto row: amplitude_matrix) {
        for (auto amplitude: row) {
            auto gate_value = temporary_gate_transposed[k][0];
            auto dot_value = amplitude * gate_value;
            C[k][0] = dot_value;
            k++;
        }
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
    for (auto row: amplitude_matrix) {
        for (auto column: row) {
            std::cout << column << ' ';
        }
    }
    printf("\n");
}

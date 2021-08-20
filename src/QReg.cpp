#include "../include/QReg.h"

void QReg::applyGate() {
    printf("applyGate\n");
using namespace std;

    printf("Printing hadamard gate...\n");
    for (auto row : HAD_GATE) {
      for (auto column : row) {
        std::cout << column << ' ';
      }
      printf("\n");
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
    }
}

#include "../include/register.h"
#include <cstring>
#include <stdexcept>

namespace Engine {
  Register::Register(size_t qubitSize, int initBit) {
    mNumberOfQubits = qubitSize;
    mQubits = (int *)calloc(sizeof(int), mNumberOfQubits);
    mNumberOfAmplitudes = (1 << mNumberOfQubits);
    QuantumGate matrix_(mNumberOfAmplitudes, std::vector<std::complex<double>>(1));
    mAmpMatrix = matrix_;
    mAmpMatrix[initBit][0] = 1;
  }
  void Register::apply(QuantumGate gate) {
    mAmpMatrix = dot_product_amplitudes(gate);
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

  QuantumGate Register::dot_product_amplitudes(QuantumGate gate) {
    int j = 0;
    int k = 0;

    QuantumGate C(mNumberOfAmplitudes, std::vector<std::complex<double>>(1));

    for (auto rowGate: gate) {
      for (auto valueGate: rowGate) {
        auto ampValue = mAmpMatrix[j][0];
        C[k][0] += ampValue * valueGate;
        j++;
      }
      j = 0;
      k++;
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
      for (auto row: mAmpMatrix) {
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
      throw std::invalid_argument("invalid gate provided");
    }
  }

  const QuantumGate Register::CNOT_GATE = {
    {1, 0, 0, 0},
    {0, 1, 0, 0},
    {0, 0, 0, 1},
    {0, 0, 1, 0}
  };

  const QuantumGate Register::ID_GATE = {
    {1, 0},
    {0, 1}
  };

  const QuantumGate Register::HAD_GATE = {
    {1 / sqrt(2), 1 / sqrt(2)},
    {1 / sqrt(2), -1 / sqrt(2)}
  };
}

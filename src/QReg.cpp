#include "../include/QReg.h"

void QReg::applyGate() {
    printf("applyGate\n");

    printf("Printing hadamard gate...\n");
    for (auto row : HAD_GATE) {
      for (auto column : row) {
        std::cout << column << ' ';
      }
      printf("\n");
    }
}

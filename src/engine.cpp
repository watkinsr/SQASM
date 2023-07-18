#include "../include/register.h"
#include "../include/engine.h"
#include <unordered_map>

namespace Engine {
  int QuantumComputationEngine::init(char **args) {
    if (args[1] == NULL || args[2] == NULL || args[3] == NULL) {
      fprintf(stderr, "invalid args to INIT, example: INIT R2 2 0\n");
      return -1;
    } else {
      int amountOfQubits = atoi(args[2]);
      Register reg = Register(amountOfQubits, atoi(args[3]));
      // First check if it exists
      auto iter = mQuantumRegisterHashmap.find(args[1]);
      if (iter != mQuantumRegisterHashmap.end()) {
        mQuantumRegisterHashmap.erase(args[1]);
      }
      auto registerVariablePair = std::pair<std::string, Register>(args[1], reg);
      mQuantumRegisterHashmap.insert(registerVariablePair);
      reg.printAmplitudes();
      return 1;
    }
  }

  int QuantumComputationEngine::peek(char **args) {
    if (args[1] == NULL) {
      fprintf(stderr, "bad input");
      return 1;
    } else {
      auto iter = mQuantumRegisterHashmap.find(args[1]);
      if (iter == mQuantumRegisterHashmap.end()) {
        printf("Couldn't find variable.\n");
      } else {
        iter->second.printAmplitudes();
      }
      return 1;
    }
  }

  int QuantumComputationEngine::apply(char **args) {
    if (args[1] == NULL || args[2] == NULL) {
      fprintf(stderr, "bad input");
      return 1;
    } else {
      auto gateIter = mGateHashmap.find(args[1]);
      if (gateIter == mGateHashmap.end()) {
        printf("Couldn't find gate variable.\n");
      }
      auto registerIter = mQuantumRegisterHashmap.find(args[2]);
      if (registerIter == mQuantumRegisterHashmap.end()) {
        printf("Couldn't find register variable.\n");
      }
      registerIter->second.apply(gateIter->second);
      registerIter->second.printAmplitudes();
      return 1;
    }
  }

  int QuantumComputationEngine::formgate(char **args) {
    if (args[1] == NULL || args[2] == NULL || args[3] == NULL) {
      fprintf(stderr, "bad input");
      return 1;
    } else {
      auto gate1 = Register::getGate(args[2]);
      auto gate2 = Register::getGate(args[3]);
      auto U = Register::tensor(gate1, gate2);
      auto gatePair = std::pair<std::string, QuantumGate>(args[1], U);
      mGateHashmap.insert(gatePair);
      auto iter = mGateHashmap.find(args[1]);
      if (iter == mGateHashmap.end()) {
        printf("Couldn't find variable.\n");
      } else {
        Register::printGate(iter->second);
      }
      return 1;
    }
  }
}

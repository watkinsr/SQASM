#ifndef ENGINE_H
#define ENGINE_H

#include <string>
#include "register.h"
#include <unordered_map>

namespace Engine {
  class QuantumComputationEngine {
    std::unordered_map<std::string, Register> mQuantumRegisterHashmap;
    std::unordered_map<std::string, QuantumGate> mGateHashmap;

    public:
      int init(char **args);
      int peek(char **args);
      int apply(char **args);
      int formgate(char **args);
  };
}

#endif

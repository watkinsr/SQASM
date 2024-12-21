#ifndef ENGINE_H
#define ENGINE_H

#include <string>
#include <unordered_map>
#include "register.h"
#include "Log.h"

class QuantumComputationEngine {
public:
    int init(const std::vector<std::string>&);
    int peek(std::vector<std::string>);
    int apply(std::vector<std::string>);
    int formgate(std::vector<std::string>);
private:
    std::unordered_map<std::string, Register> _reg_map = {};
    std::unordered_map<std::string, QuantumGate> _gate_map = {};
};

#endif

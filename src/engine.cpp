#include "engine.h"
#include "register.h"

int QuantumComputationEngine::init(const std::vector<std::string>& args) {
    if (args.size() != 4) {
        fprintf(stdout, "Please provide correct arguments.");
        return 1;
    }
    int qubit_size = atoi(args[2].c_str());
    int initial_bit = atoi(args[3].c_str());
    std::string _reg_lookup = args[1];
    LOG_INFO("Searching for register in cache: %s", _reg_lookup.c_str());
    if (_reg_map.size() > 0 && _reg_map.find(_reg_lookup) != _reg_map.end()) {
        _reg_map.erase(args[1]);
    }
    LOG_INFO("Create <Register size=%i, initial_bit=%i>", qubit_size, initial_bit);
    Register reg = Register(qubit_size, initial_bit);
    reg.printAmplitudes();
    _reg_map.insert(std::pair<std::string, Register>(std::move(args[1]), std::move(reg)));
    return 1;
}

int QuantumComputationEngine::peek(std::vector<std::string> args) {
    if (_reg_map.find(args[1]) == _reg_map.end()) {
        fprintf(stdout, "Couldn't find variable.\n");
    } else {
        _reg_map.at(args[1]).printAmplitudes();
    }
    return 1;
}

int QuantumComputationEngine::apply(std::vector<std::string> args) {
    QuantumGate gate;
    if (_reg_map.find(args[2]) == _reg_map.end()) {
        fprintf(stdout, "Unable to find register. Please provide correct register.\n");
        fprintf(stdout, "Current registers: [");
        uint8_t idx = 0;
        for (const auto& [key, reg] : _reg_map) {
            fprintf(stdout, key.c_str());
            if (idx != _reg_map.size() -1) fprintf(stdout, ",");
            idx++;
        }
        fprintf(stdout, "]\n");
        return 1;
    }
    if (_gate_map.find(args[1]) == _gate_map.end()) {
        gate = Register::getGate(args[1].c_str());
        if (gate == Register::NO_GATE) {
            fprintf(stderr, "Cannot comply with apply command, please offer correct gate.\n");
            return 1;
        }
    } else {
        gate = _gate_map.at(args[1]);
    }
    auto reg = _reg_map.at(args[2]);
    reg.apply(gate);
    reg.printAmplitudes();
    return 1;
}

int QuantumComputationEngine::formgate(std::vector<std::string> args) {
    auto gate1 = Register::getGate(args[2].c_str());
    auto gate2 = Register::getGate(args[3].c_str());
    auto U = Register::tensor(gate1, gate2);
    _gate_map.insert(std::pair<std::string, QuantumGate>(args[1], U));
    if (_gate_map.find(args[1]) == _gate_map.end()) {
        fprintf(stdout, "Couldn't find variable.\n");
    } else {
        Register::printGate(_gate_map[args[1]]);
    }
    return 1;
}

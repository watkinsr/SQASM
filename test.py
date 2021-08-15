class QuantumSimExample:
    def __init__(
        self,
        n_qubits,
    ):
        self.n_qubits = n_qubits
        self.qubits = [0] * n_qubits
        # in this classical simulation, we use 2^n_qubits complex numbers
        self.amps = [0] * (1 << n_qubits)
        self.amps[len(self.amps) - 1] = 1

    def __repr__(self) -> str:
        return f"TestQubits[{self.n_qubits}], amps: {self.amps}"

def main():
    quantum_sim_example = QuantumSimExample(n_qubits=3)
    print(quantum_sim_example)

if __name__ == '__main__':
    main()

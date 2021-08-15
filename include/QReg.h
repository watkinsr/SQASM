#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include <vector>

class QReg
{
public:
    QReg(size_t numberOfQubits)
    {
        numberOfQubits = numberOfQubits;
        qubits = (int *)calloc(sizeof(int), numberOfQubits);
        int numberOfAmplitudes = (1 << numberOfQubits);
        amps = (int *)calloc(sizeof(int), numberOfAmplitudes);

        printf("Number of qubits: %zu\n", numberOfQubits);
        printf("Number of amplitudes: %i\n", numberOfAmplitudes);

        for (int i = 0; i < numberOfAmplitudes; i++)
        {
            amps[i] = 0;
        }
        amps[numberOfAmplitudes - 1] = 1;

        printf("Amplitudes: ");
        // Print the amplitudes.
        for (int i = 0; i < numberOfAmplitudes; i++)
            std::cout << amps[i];

        printf("\n");

        std::vector<std::vector<int>> matrix_(numberOfAmplitudes, std::vector<int>(1));
        matrix = matrix_;

        // Default set last value as 1.
        matrix[numberOfAmplitudes - 1][0] = 1;
    }

private:
    int numberOfQubits;
    int *qubits;
    int *amps;
    std::vector<std::vector<int>> matrix;
};

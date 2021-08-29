#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "../include/QReg.h"
#include "../include/parse.h"

int main(void) {
  interpreter_loop();
  return 0;
}

void interpreter_loop(void) {
  char *line;
  char **args;
  int status;

  do {
    printf("> ");
    line = read_line();
    args = split_line(line);
    status = execute_cmd(args);

    free(line);
    free(args);
  } while (status);
}

char *read_line(void) {
  char *line = NULL;
  size_t bufsize = 0; // have getline allocate a buffer for us

  if (getline(&line, &bufsize, stdin) == -1) {
    if (feof(stdin)) {
      exit(EXIT_SUCCESS); // We recieved an EOF
    } else {
      perror("readline");
      exit(EXIT_FAILURE);
    }
  }

  return line;
}

char **split_line(char *line) {
  size_t bufsize = LSH_TOK_BUFSIZE;
  size_t position = 0;
  char **tokens = (char **)malloc(bufsize * sizeof(char *));
  char *token;

  if (!tokens) {
    fprintf(stderr, "lsh: allocation error\n");
    exit(EXIT_FAILURE);
  }

  token = strtok(line, LSH_TOK_DELIM);

  while (token != NULL) {
    // printf("token: %s\n", token);
    tokens[position++] = token;

    if (position >= bufsize) {
      bufsize += LSH_TOK_BUFSIZE;
      tokens = (char **)realloc(tokens, bufsize * sizeof(char *));
      if (!tokens) {
        fprintf(stderr, "lsh: allocation error\n");
        exit(EXIT_FAILURE);
      }
    }

    token = strtok(NULL, LSH_TOK_DELIM);
  }
  tokens[position] = NULL;
  return tokens;
}

/*
  List of builtin commands, followed by their corresponding functions.
 */

int get_num_commands() { return sizeof(tokens) / sizeof(char *); }

int sqint_init(char **args) {
  if (args[1] == NULL || args[2] == NULL || args[3] == NULL) {
    fprintf(stderr, "invalid args to INIT, example: INIT R2 2 0\n");
  } else {
    int amountOfQubits = atoi(args[2]);
    QReg reg = QReg(amountOfQubits, atoi(args[3]));
    // First check if it exists
    auto iter = quantumRegisterHashmap.find(args[1]);
    if (iter != quantumRegisterHashmap.end()) {
      quantumRegisterHashmap.erase(args[1]);
    }

    auto registerVariablePair = std::pair<string, QReg>(args[1], reg);
    quantumRegisterHashmap.insert(registerVariablePair);
    reg.printAmplitudes();
  }
  return 1;
}

int sqint_peek(char **args) {
  if (args[1] == NULL) {
    fprintf(stderr, "bad input");
    return 1;
  } else {
    auto iter = quantumRegisterHashmap.find(args[1]);
    if (iter == quantumRegisterHashmap.end()) {
      printf("Couldn't find variable.\n");
    } else {
      iter->second.printAmplitudes();
    }
    return 1;
  }
}

int sqint_apply(char **args) {
  if (args[1] == NULL || args[2] == NULL) {
    fprintf(stderr, "bad input");
    return 1;
  } else {
    auto gateIter = gateHashmap.find(args[1]);
    if (gateIter == gateHashmap.end()) {
      printf("Couldn't find gate variable.\n");
    }
    auto registerIter = quantumRegisterHashmap.find(args[2]);
    if (registerIter == quantumRegisterHashmap.end()) {
      printf("Couldn't find register variable.\n");
    }
    registerIter->second.applyGateToSystem(gateIter->second);
    registerIter->second.printAmplitudes();
    return 1;
  }
}

int sqint_formgate(char **args) {
  if (args[1] == NULL || args[2] == NULL || args[3] == NULL) {
    fprintf(stderr, "bad input");
    return 1;
  } else {
    auto gate1 = QReg::getGateByString(args[2]);
    auto gate2 = QReg::getGateByString(args[3]);
    auto U = QReg::tensor(gate1, gate2);
    auto gatePair = std::pair<string, QuantumGate>(args[1], U);
    gateHashmap.insert(gatePair);
    auto iter = gateHashmap.find(args[1]);
    if (iter == gateHashmap.end()) {
      printf("Couldn't find variable.\n");
    } else {
      QReg::printGate(iter->second);
    }
    return 1;
  }
}

int shell_help(char **args) {
  printf("SQINT - Simple Quantum Interpreter\n");
  printf("To initialize a register use INIT REG QUBITSIZE INITBIT\n");
  printf("To form a gate use FORMGATE VAR GATE1 GATE2\n");
  printf("To peek at a register use PEEK REGISTERNAME\n");
  printf("To apply a register to a register use APPLY GATE REGISTER\n");
  return 1;
}

int exit(char **args) { return 0; }

int execute_cmd(char **args) {
  int i;

  if (args[0] == NULL) {
    return 1;
  }

  for (i = 0; i < get_num_commands(); i++) {
    if (strcmp(args[0], tokens[i]) == 0) {
      return (*builtin_func[i])(args);
    }
  }
  if (strcmp(args[0], "exit") == 0) {
    return 0;
  } else {
    return shell_help(args);
  }
}

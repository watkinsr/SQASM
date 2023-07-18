#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "../include/interpreter.h"

namespace Interpreter {
  Interpreter::Interpreter() {
    Engine::QuantumComputationEngine* mEngine = new Engine::QuantumComputationEngine();
  }

  void Interpreter::loop(void) {
    printf("Begin loop.\n");
    do {
      printf("> ");
      mStatus = -1;
      read_line();
      mArgs = split_line(mLine);
      mStatus = exec(mArgs);
      printf("\nStatus was: %d", mStatus);
      printf("\n");
    } while(mStatus != -1);
  }

  void Interpreter::read_line(void) {
    size_t bufsize = 0; // have getline allocate a buffer for us

    if (getline(&mLine, &bufsize, stdin) == -1) {
      if (feof(stdin)) {
        fprintf(stderr, "Error: got EOF.");
      } else {
        fprintf(stderr , "Error: readline general error.");
      }
    }
  }

  char** Interpreter::split_line(char *line) {
    size_t bufsize = INTERPRETER_TOK_BUFSIZE;
    size_t position = 0;
    char **tokens = (char **)malloc(bufsize * sizeof(char *));
    char *token;

    if (!tokens) {
      fprintf(stderr, "Error: token allocation failed.");
      exit();
    }

    token = strtok(line, INTERPRETER_TOK_DELIM);

    while (token != NULL) {
      tokens[position++] = token;

      if (position >= bufsize) {
        bufsize += INTERPRETER_TOK_BUFSIZE;
        tokens = (char **)realloc(tokens, bufsize * sizeof(char *));
        if (!tokens) {
          fprintf(stderr, "Error: Unable to allocate correctly for tokens.");
          exit();
        }
      }

      token = strtok(NULL, INTERPRETER_TOK_DELIM);
    }
    tokens[position] = NULL;
    return tokens;
  }

  int Interpreter::help(char **args) {
    printf("SQINT - Simple Quantum Interpreter\n");
    printf("To initialize a register use INIT REG QUBITSIZE INITBIT\n");
    printf("To form a gate use FORMGATE VAR GATE1 GATE2\n");
    printf("To peek at a register use PEEK REGISTERNAME\n");
    printf("To apply a register to a register use APPLY GATE REGISTER\n");
    return 1;
  }

  int Interpreter::exit() { return 0; }

  int Interpreter::exec(char **args) {
    if (args[0] == NULL) {
      fprintf(stderr, "Error: Parse error on command. Exiting.");
      return exit();
    }
    char *cmd = args[0];
    if (strcmp(cmd, "exit") == 0) {
      return exit();
    } else if (strcmp(cmd, "HELP") == 0) {
      return help(args);
    } else if (strcmp(cmd, "INIT") == 0) {
      return mEngine->init(args);
    } else if (strcmp(cmd, "FORMGATE") == 0) {
      return mEngine->formgate(args);
    } else if (strcmp(cmd, "PEEK") == 0) {
      return mEngine->peek(args);
    } else if (strcmp(cmd, "APPLY") == 0) {
      return mEngine->apply(args);
    } else {
      fprintf(stderr, "Error: Incorrect command passed.");
      return -1;
    }
  }
};



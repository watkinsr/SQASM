#ifndef INTERPRETER_H
#define INTERPRETER_H

#include "engine.h"

#define INTERPRETER_RL_BUFSIZE 1024
#define INTERPRETER_TOK_BUFSIZE 64
#define INTERPRETER_TOK_DELIM " \t\r\n\a"
#define CMD_SIZE 5

namespace Interpreter {
  static const char *INTERPRETER_TOKENS[5] = {
    "INIT",
    "FORMGATE",
    "PEEK",
    "APPLY",
    "help",
  };
  class Interpreter {
    public:
      Interpreter();
      void loop(void);
      int help(char **args);
    private:
      Engine::QuantumComputationEngine* mEngine;
      char *mLine;
      char **mArgs;
      int mStatus;
      void read_line(void);
      char **split_line(char *line);
      int exit();
      int exec(char **args);
  };
}

#endif

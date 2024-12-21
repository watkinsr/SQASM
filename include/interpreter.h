#ifndef INTERPRETER_H
#define INTERPRETER_H

#include <cstdlib>
#include "engine.h"
#include "Log.h"

#define INTERPRETER_RL_BUFSIZE 1024
#define INTERPRETER_TOK_BUFSIZE 64
#define INTERPRETER_TOK_DELIM " \t\r\n\a"
#define CMD_SIZE 5

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
    int help(std::vector<std::string>);
private:
    std::unique_ptr<QuantumComputationEngine> _engine;
    char *mLine;
    char **_args;
    int _status;
    void read_line(void);
    char **split_line(char *line);
    int exec(char **args);
};

#endif

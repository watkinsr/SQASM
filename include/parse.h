#include <string>
#include <unordered_map>
#include <string>
#include "QReg.h"

#define LSH_RL_BUFSIZE 1024
#define LSH_TOK_BUFSIZE 64
#define LSH_TOK_DELIM " \t\r\n\a"

void interpreter_loop(void);
char *read_line(void);
char **split_line(char *line);
int exit(char **args);
int execute_cmd(char **args);
int sqint_init(char **args);
int sqint_formgate(char **args);
int sqint_peek(char **args);
int sqint_apply(char **args);
int shell_help(char **args);

unordered_map<string, QuantumGate> gateHashmap;
unordered_map<string, QReg> quantumRegisterHashmap;

const char *tokens[] = {
    "INIT",
    "FORMGATE",
    "PEEK",
    "APPLY",
    "help",
};

int (*builtin_func[])(char **) = {
    &sqint_init,
    &sqint_formgate,
    &sqint_peek,
    &sqint_apply,
    &shell_help,
};

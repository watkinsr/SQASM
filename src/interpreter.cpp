#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <algorithm>
#include "interpreter.h"

Interpreter::Interpreter() {
    _engine = make_unique<QuantumComputationEngine>();
}

void Interpreter::loop(void) {
    LOG_INFO("Begin loop.");
    do {
        fprintf(stdout, "> ");
        _status = -1;
        read_line();
        _args = split_line(mLine);
        _status = exec(_args);
    } while(_status != -1);
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
        exit(EXIT_FAILURE);
    }

    token = strtok(line, INTERPRETER_TOK_DELIM);

    while (token != NULL) {
        tokens[position++] = token;

        if (position >= bufsize) {
            bufsize += INTERPRETER_TOK_BUFSIZE;
            tokens = (char **)realloc(tokens, bufsize * sizeof(char *));
            if (!tokens) {
                fprintf(stderr, "Error: Unable to allocate correctly for tokens.");
                exit(EXIT_FAILURE);
            }
        }

        token = strtok(NULL, INTERPRETER_TOK_DELIM);
    }
    tokens[position] = NULL;
    return tokens;
}

int Interpreter::help(std::vector<std::string> args) {
    fprintf(stdout, "SQINT - Simple Quantum Interpreter\n");
    fprintf(stdout, "INIT - INIT <REG> <QUBITSIZE> <INIT_BIT>\n");
    fprintf(stdout, "FORMGATE - FORMGATE <VAR> <GATE1> <GATE2>\n");
    fprintf(stdout, "Note: Forming a gate is a tensor operation on GATE1 and GATE2.\n");
    fprintf(stdout, "PEEK - PEEK <REG>\n");
    fprintf(stdout, "APPLY - APPLY <GATE> <REG>\n");
    fprintf(stdout, "Gates available - HAD (hadamard), ID (identity) and CNOT\n");
    fprintf(stdout, "To exit, type quit.\n");
    return 1;
}

int Interpreter::exec(char **_args) {
    LOG_INFO("[TRACE] Interpreter::exec(?)");

    std::vector<std::string> args = {};
    if (_args[0] == NULL) {
        fprintf(stderr, "Please provide arguments.");
        return help(args);
    }

    int i = 0;
    while(_args[i] != NULL) {
        args.push_back(_args[i]);
        i++;
    }

    std::string cmd = std::string(_args[0]);
    std::transform(cmd.begin(), cmd.end(), cmd.begin(),
    [](unsigned char c){ return std::tolower(c); });

    if (cmd == "exit") {
        return help(args);
    } else if (cmd == "help") {
        return help(args);
    } else if (cmd == "init") {
        return _engine->init(args);
    } else if (cmd == "formgate") {
        return _engine->formgate(args);
    } else if (cmd == "peek") {
        return _engine->peek(args);
    } else if (cmd == "apply") {
        return _engine->apply(args);
    } else if (cmd == "quit") {
        exit(0);
    } else {
        return help(args);
    }
}

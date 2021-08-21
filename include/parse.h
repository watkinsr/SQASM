#include <string>

#define LSH_RL_BUFSIZE 1024
#define LSH_TOK_BUFSIZE 64
#define LSH_TOK_DELIM " \t\r\n\a"

void lsh_loop(void);
char *lsh_read_line(void);
char **lsh_split_line(char *line);
int lsh_exit(char **args);
int lsh_execute(char **args);
int lsh_init(char **args);
int lsh_formgate(char **args);

const char *tokens[] = {
    "INIT",
    "FORMGATE"
};

int (*builtin_func[])(char **) = {
    &lsh_init,
    &lsh_formgate
};

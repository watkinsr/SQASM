%{
#include "myscanner.h"
%}

%%
"add"			return ADD;
"mov"			return MOV;
"push"			return PUSH;

[ \t\n]			;
.			printf("unexpected character\n");

%%

int yywrap(void)
{
  return 1;
}

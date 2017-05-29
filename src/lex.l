%{
#include "y.tab.h"
int yylex();
void yyerror (const char *s);
%}
%%
"printf"			   {return print;}
"ret"				   {return exit_command;}
"INITIALIZE"			   {return init;}
"TENSOR"	                   {return tensor;}
"APPLY"			           {return apply;}
"SELECT"			   {return sel;}
"MEASURE"			   {return measure;}
"ADD"			           {return add;}
"PEEK"				   {return peek;}
"HAD"|"ID"|"CNOT"|"SWAP"|"NOT"|"COEF"|"CV"|"COEF2"|"CVPLUS" {yylval.id = strdup(yytext); return gate;}
[0-9]+                             {yylval.num = atoi(yytext); return number;}
[A-Z0-9]+			   {yylval.id = strdup(yytext); return identifier;}
[ \t\n]                            ;
[-+=;]           	           {return yytext[0];}
.                                  {ECHO; yyerror ("unexpected character");}

%%
int yywrap (void) {return 1;}


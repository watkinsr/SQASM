#! /bin/bash

clear 
yacc -d parser.y && lex lex.l && gcc -I/usr/include/python2.7 -lpython2.7 lex.yy.c y.tab.c -o qasm && ./qasm<input


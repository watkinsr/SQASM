#!/bin/bash

function run () {
    # echo "yacc -d parser.y";
    yacc -d parser.y;
    
    # echo "flex lex.l"
    flex lex.l;
    mv lex.yy.c lexer.c;
    mv y.tab.c parser.c;
    mv y.tab.h parser.h;
    
    mkdir -p obj;

    gcc -Wall -I/usr/include/python2.7 -c parser.c;
    gcc -Wall -I/usr/include/python2.7 -c lexer.c;

    mv lexer.o obj/lexer.o;
    mv parser.o obj/parser.o;

    mkdir -p ../bin;
    gcc obj/lexer.o obj/parser.o -lpython2.7 -o ../bin/qasm;

    # cleanup 
    rm lexer.c;
    rm parser.c;
    # rm parser.h;
    rm obj/*.o;
}

if ! command -v yacc &> /dev/null
then
    echo "yacc could not be found"
    echo "Trying to install bison (if you are on debian-based systems)"
    sudo apt install bison;
    exit
fi

if ! command -v flex &> /dev/null
then
    echo "flex could not be found"
    echo "Trying to install flex (if you are on debian-based systems)"
    sudo apt install flex;
    exit
fi

if ! command -v gcc &> /dev/null
then
    echo "gcc could not be found"
    echo "Trying to install gcc (if you are on debian-based systems)"
    sudo apt install gcc;
    exit
fi
if ! command -v python2.7 &> /dev/null
then
    echo "python2.7 could not be found"
    echo "Trying to install python2.7 (if you are on debian-based systems)"
    sudo apt install python2.7;
    exit
fi

sudo apt install python-numpy;

if [ -d "/usr/include/python2.7" ]; then
    run
else
    echo "Trying to install libpython libs (if you are on debian-based systems)"
    sudo apt install libpython-all-dev
    run
fi

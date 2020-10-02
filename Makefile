##
# QPL Interpreter
#
# @file
# @version 0.1

IDIR=include
CC=gcc
CFLAGS=-I$(IDIR)

LIBS=-lm

ODIR=obj
LDIR=lib

BDIR=bin

_DEPS = parse.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = parse.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: src/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

MKDIR_P = mkdir -p

.PHONY: clean directories

all: directories parse

parse: $(OBJ)
	$(CC) -o $(BDIR)/$@ $^ $(CFLAGS) $(LIBS)

directories: ${BDIR} ${ODIR}

${BDIR}:
	${MKDIR_P} ${BDIR}

${ODIR}:
	${MKDIR_P} ${ODIR}
clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~

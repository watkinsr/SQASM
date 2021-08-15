##
# QPL Interpreter
#
# @file
# @version 0.1

IDIR=include
CPPFLAGS=-g -I$(IDIR) -lstdc++ -std=c++11 -Wall

LIBS=

ODIR=obj
LDIR=lib

BDIR=bin

_DEPS = parse.h QReg.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = parse.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: src/%.cpp $(DEPS)
	$(CXX) $(pkg-config --cflags eigen3) -c -o $@ $< $(CPPFLAGS)

MKDIR_P = mkdir -p

.PHONY: clean directories

all: directories parse

parse: $(OBJ)
	$(CXX) -o $(BDIR)/$@ $^ $(CPPFLAGS)

directories: ${BDIR} ${ODIR}

${BDIR}:
	${MKDIR_P} ${BDIR}

${ODIR}:
	${MKDIR_P} ${ODIR}
clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~

#include "../include/interpreter.h"

int main(void) {
  printf("Entry point.\n");
  Interpreter::Interpreter* interpreter = new Interpreter::Interpreter();
  printf("Interpreter created.\n");
  interpreter->loop();
}

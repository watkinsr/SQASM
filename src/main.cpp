#include <memory>
#include "interpreter.h"

int main(void) {
  std::unique_ptr<Interpreter> interpreter = make_unique<Interpreter>();
  LOG_INFO("Interpreter created.");
  interpreter->loop();
}

#include "testlib.h"
#include "constraints.hpp"

using namespace std;

int main() {
  registerValidation();
  int a = inf.readInt(MIN_A, MAX_A, "A");
  inf.readSpace();
  int b = inf.readInt(MIN_B, MAX_B, "B");
  inf.readEoln();
  inf.readEof();
}

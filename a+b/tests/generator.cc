#include "testlib.h"
#include "constraints.hpp"

using namespace std;

int main(int argc, char* argv[]) {
  registerGen(argc, argv, 1);
  for (int i = 0; i < 20; ++i) {
    string id = to_string(i);
    if (id.size() == 1u) id = "0" + id;
    ofstream ofs(("10_random_" + id + ".in").c_str());
    ofs << rnd.next(MIN_A, MAX_A) << " " << rnd.next(MIN_B, MAX_B) << endl;
  }
}

#include <stdbool.h>

bool eq(int *a, int *b, int n) {
  bool all = true;
  for (int i = 0; i < n; ++i) {
    if (a[i] != b[i]) {
      all = false;
    }
  }
  return all;
}

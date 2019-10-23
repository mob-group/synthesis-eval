#include <stdbool.h>

bool mirror_image(int* a, int* b, int n) {
  bool all = true;
  for (int i = 0; i < n; ++i) {
    if (a[i] != b[n - i - 1]) {
      all = false;
    }
  }
  return all;
}

#include <stdbool.h>

bool member(int *arr, int n, int v) {
  bool ret = false;
  for (int i = 0; i < n; ++i) {
    if (arr[i] == v) {
      ret = true;
    }
  }
  return ret;
}

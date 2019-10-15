#include <limits.h>

int min(int *arr, int n) {
  int min_i = -1;
  int min = INT_MAX;
  for (int i = 0; i < n; ++i) {
    if (arr[i] < min) {
      min = arr[i];
      min_i = i;
    }
  }
  return min_i;
}

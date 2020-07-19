#include <limits.h>

int min_elt(int *arr, int n) {
  int min = INT_MAX;
  for (int i = 0; i < n; ++i) {
    if (arr[i] < min) {
      min = arr[i];
    }
  }
  return min;
}

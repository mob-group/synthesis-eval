#include <limits.h>

int max_elt(int *arr, int n) {
  int max = INT_MIN;
  for (int i = 0; i < n; ++i) {
    if (arr[i] > max) {
      max = arr[i];
    }
  }
  return max;
}

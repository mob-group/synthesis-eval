#include <limits.h>

int max(int *arr, int n) {
  int max_i = -1;
  int max = INT_MIN;
  for (int i = 0; i < n; ++i) {
    if (arr[i] > max) {
      max = arr[i];
      max_i = i;
    }
  }
  return max_i;
}

int last_zero_idx(int *arr, int n) {
  int idx = 0;
  for (int i = 0; i < n; ++i) {
    if (arr[i] == 0) {
      idx = i;
    }
  }
  return idx;
}

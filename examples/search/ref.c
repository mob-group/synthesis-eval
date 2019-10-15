int search(int *arr, int v, int n) {
  int idx = -1;
  for (int i = 0; i < n; ++i) {
    if (idx == -1 && arr[i] == v) {
      idx = i;
    }
  }
  return idx;
}

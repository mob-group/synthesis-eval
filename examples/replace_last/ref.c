void replace_last(int *arr, int n) {
  int v = 0;
  for (int i = 0; i < n; ++i) {
    v = arr[i];
  }

  for (int i = 0; i < n; ++i) {
    arr[i] = v;
  }
}

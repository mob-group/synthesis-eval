void clamp(int *arr, int n) {
  for (int i = 0; i < n; ++i) {
    if (arr[i] < 0) {
      arr[i] = 0;
    }
  }
}

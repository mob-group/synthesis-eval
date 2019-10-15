void reverse(int *arr, int n) {
  for (int i = 0; i < n; ++i) {
    int t = arr[i];
    arr[i] = arr[n - i - 1];
    arr[n - i - 1] = t;
  }
}

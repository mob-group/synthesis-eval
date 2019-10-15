int sum_abs(int *arr, int n) {
  int sum = 0;
  for (int i = 0; i < n; ++i) {
    sum += (arr[i] > 0 ? arr[i] : -arr[i]);
  }
  return sum;
}

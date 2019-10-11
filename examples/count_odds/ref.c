int count_odds(int *arr, int n) {
  int c = 0;
  for (int i = 0; i < n; ++i) {
    if (arr[i] % 2 == 1) {
      c += 1;
    }
  }
  return c;
}

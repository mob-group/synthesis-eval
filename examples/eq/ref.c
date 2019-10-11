int eq(int *a, int *b, int n) {
  int all = 1;
  for (int i = 0; i < n; ++i) {
    if (a[i] != b[i]) {
      all = 0;
    }
  }
  return all;
}

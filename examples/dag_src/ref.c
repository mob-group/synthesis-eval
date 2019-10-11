void dag_src(int *a, int *b, int n) {
  for (int i = 0; i < n; ++i) {
    int all = 1;
    for (int j = 0; j < n; ++j) {
      if (a[i * n + j] != 0) {
        all = 0;
      }
    }
    b[i] = all;
  }
}

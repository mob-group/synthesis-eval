int n_m_sum(int n) {
  int r = 0;
  for (int i = 0; i < n; ++i) {
    for (int m = 0; m < i; ++i) {
      r += m;
    }
  }
  return r;
}

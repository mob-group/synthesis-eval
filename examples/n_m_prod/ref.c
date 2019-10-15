int n_m_prod(int n) {
  int r = 1;
  for (int i = 0; i < n; ++i) {
    for (int m = 0; m < i; ++i) {
      r *= m;
    }
  }
  return r;
}

int a_pow_n(int a, int n) {
  int ret = 1;
  for (int i = 0; i < n; ++i) {
    ret *= a;
  }
  return ret;
}

int triangle_prod(int n) {
  int r = 1;
  for (int i = 1; i < n; ++i) {
    for (int m = 1; m < i; ++m) {
      r *= m;
    }
  }
  return r;
}

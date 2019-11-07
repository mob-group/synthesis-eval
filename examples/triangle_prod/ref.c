int triangle_prod(int n) {
  int r = 1;
  for (int i = 0; i < n; ++i) {
    for (int m = 1; m < i; ++i) {
      r *= m;
    }
  }
  return r;
}

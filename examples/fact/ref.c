int fact(int n) {
  int r = 1;
  while (n > 1) {
    r *= n;
    n -= 1;
  }
  return r;
}

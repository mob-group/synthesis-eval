int fact_fact(int n) {
  int r = 1;
  while (n > 1) {
    r *= n;
    n -= 2;
  }
  return r;
}

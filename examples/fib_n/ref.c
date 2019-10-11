int fib_n(int n) {
  int i = 1;
  int r = 1;
  while (n > 1) {
    i = r - i;
    r = i + r;
    n = n - 1;
  }
  return r;
}

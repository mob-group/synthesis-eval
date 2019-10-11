int binary_digits(int n) {
  int r = 1;
  while (n > 1) {
    r += 1;
    n /= 2;
  }
  return r;
}

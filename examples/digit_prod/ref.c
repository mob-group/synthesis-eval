int digit_prod(int n) {
  int r = 1;
  while (n > 1) {
    int t = n % 10;
    r *= t;
    n /= 10;
  }
  return r;
}

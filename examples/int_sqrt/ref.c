int int_sqrt(int n) {
  int b = 0;

  while (n >= 0) {
    n = n - b;
    b = b + 1;
    n = n - b;
  }

  return b - 1;
}

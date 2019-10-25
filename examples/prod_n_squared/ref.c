int prod_n_squared(int n) {
  int prod = 1;
  for (int i = 1; i < n; ++i) {
    prod *= i;
    prod *= i;
  }
  return prod;
}

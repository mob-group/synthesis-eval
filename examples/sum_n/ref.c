int sum_n(int n) {
  int sum = 0;
  while (n > 0) {
    sum += n;
    --n;
  }
  return sum;
}

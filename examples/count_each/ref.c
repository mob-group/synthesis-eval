void count_each(int n, int *counts) {
  while (n > 0) {
    int t = n % 10;
    counts[t] += 1;
    n /= 10;
  }
}

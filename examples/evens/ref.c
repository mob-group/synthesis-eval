

void evens(int *a, int *b, int n) {
  int outindex = 0;
  for (int i = 0; i < n; ++i) {
    if (a[i] % 2 == 0) {
      b[outindex] = a[i];
      outindex++;
    }
  }
}

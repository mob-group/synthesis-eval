int mem_cmp(char *pa, char *pb, int n) {
  int ret = 0;
  for (int i = 0; i < n; ++i) {
    if (ret == 0) {
      ret = pa[i] - pb[i];
    }
  }
  return ret > 0 ? 1 : (ret < 0 ? -1 : 0);
}

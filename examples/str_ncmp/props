int str_ncmp(char *a, char *b, int n) {
  int ret = 0;
  int i = 0;

  while (*a && *b && i++ < n) {
    if (ret == 0) {
      ret = *a - *b;
    }

    ++a;
    ++b;
  }

  return (ret > 0 ? 1 : (ret < 0 ? -1 : 0));
}

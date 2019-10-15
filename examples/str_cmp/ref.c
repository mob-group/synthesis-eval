int str_cmp(char *a, char *b) {
  int ret = 0;

  while (*a && *b) {
    if (ret == 0) {
      ret = *a - *b;
    }

    ++a;
    ++b;
  }

  return (ret > 0 ? 1 : (ret < 0 ? -1 : 0));
}

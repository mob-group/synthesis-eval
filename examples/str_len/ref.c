int str_len(char *str) {
  int l = 0;
  while (*str++) {
    ++l;
  }
  return l;
}

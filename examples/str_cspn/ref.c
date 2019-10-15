int str_cspn(char *a, char *b) {
  int c = 0;

  for (char *k = a; *k; ++k) {
    for (char *s = b; *s; ++s) {
      if (k == *s) {
        return c;
      }
    }
  }

  return c;
}

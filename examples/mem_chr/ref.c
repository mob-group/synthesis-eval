#include <stddef.h>

char *mem_chr(char *str, char c, int n) {
  char *ret = NULL;
  for (int i = 0; i < n; ++i) {
    if (ret == NULL && str[i] == c) {
      ret = &str[i];
    }
  }
  return ret;
}

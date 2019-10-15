#include <stddef.h>

void *mem_chr(char *str, char c, int n) {
  void *ret = NULL;
  for (int i = 0; i < n; ++i) {
    if (ret == NULL && str[i] == c) {
      ret = &str[i];
    }
  }
  return ret;
}

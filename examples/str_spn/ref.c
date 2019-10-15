#include <stdbool.h>

int str_spn(char *a, char *b) {
  int c = 0;

  for (char *k = a; *k; ++k) {
    bool any = false;

    for (char *s = b; *s; ++s) {
      if (*k == *s) {
        any = true;
      }
    }

    if (!any) {
      return c;
    }

    ++c;
  }

  return c;
}

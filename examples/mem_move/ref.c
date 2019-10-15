#include <stdlib.h>

void mem_move(char *dst, char *src, int n) {
  if (dst >= src && dst < src + n) {
    char *buf = malloc(n);

    for (int i = 0; i < n; ++i) {
      buf[i] = src[i];
    }

    for (int i = 0; i < n; ++i) {
      dst[i] = buf[i];
    }

    free(buf);
  } else {
    for (int i = 0; i < n; ++i) {
      dst[i] = src[i];
    }
  }
}

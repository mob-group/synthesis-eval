void merge(int *a, int *b, int *o, int na, int nb) {
  int ia = 0, ib = 0, io = 0;
  while (io < na + nb) {
    if (ia < na && ib < nb) {
      if (a[ia] < b[ib]) {
        o[io++] = a[ia++];
      } else {
        o[io++] = b[ib++];
      }
    } else if (ia < na) {
      o[io++] = a[ia++];
    } else {
      o[io++] = b[ib++];
    }
  }
}

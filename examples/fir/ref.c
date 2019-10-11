void fir(int *in, int *out, int *coefs, int N) {
  for (int n = 0; n < N; ++n) {
    out[n] = 0;
    for (int i = 0; i <= N; ++i) {
      out[n] += coefs[i] * in[N - i];
    }
  }
}

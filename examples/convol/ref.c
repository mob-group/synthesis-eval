void convol(int M, int K, float *in, float *k, float *o) {
  for (int i = 0; i < M; ++i) {
    float sum = 0;
    for (int j = 0; j < K; ++j) {
      int idx = i - j;
      float ival = i - j < 0 ? 0.0 : in[idx];
      sum += ival * k[j];
    }
    o[i] = sum;
  }
}

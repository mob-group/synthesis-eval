void norm(float *vec, float *o, int n) {
  float sum = 0.0f;
  for (int i = 0; i < n; ++i) {
    sum += vec[i];
  }

  for (int i = 0; i < n; ++i) {
    o[i] /= sum;
  }
}

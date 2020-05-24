void multiply_evens(int *arr, int *arr2, int n, int *out) {
  int filtered = 0;
  for (int i = 0; i < n; ++i) {
	  int x = arr[i] - arr2[i];
	  if (x % 2 == 0) {
		  out[filtered] = x * arr2[filtered];
	  }
  }
}

void multiply_min_diff(int *arr, int *arr2, int n, int *out) {
  int diff_so_far = 10000;
  for (int i = 0; i < n; i ++) {
	  int diff = arr[i] - arr2[i];
	  if (diff < diff_so_far) {
		  diff_so_far = diff;
	  }
  }

  for (int i = 0; i < n; i ++) {
	  out[i] = arr[i] - diff_so_far;
  }
}

int sum_of_lists_multiplied_after_dividing_by_three(int *arr, int *arr2, int n) {
  for (int i = 0; i < n; i ++) {
    arr[i] = arr[i] / 3;
  }

  for (int i = 0; i < n; i ++) {
    arr[i] = arr[i] * arr2[i];
  }

  int sum = 0;
  for (int i = 0; i < n; i ++) {
	  sum += arr[i];
  }

  return sum;
}

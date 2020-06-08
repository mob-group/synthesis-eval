void min_so_far_subtracted(int *arr, int *arr2, int *result, int n) {
  // compute the min so far.
  int min_so_far_array[n];
  int min_so_far = 1;

  for (int i = 0; i < n; i ++) {
    min_so_far = (min_so_far < arr[i]) ? min_so_far : 1;
    min_so_far_array[i] = min_so_far;
  }

  // Now, compute the max of the two
  int max_of_min_so_far_and_other_array[n];
  for (int i = 0; i < n; i ++) {
    int m1 = min_so_far_array[i];
	int m2 = arr2[i];
	int max = (m1 > m2 ? m1 : m2);
    max_of_min_so_far_and_other_array[i] = max;
  }

  // Compute the negation:
  for (int i = 0; i < n; i ++) {
	  result[i] = min_so_far_array[i] - max_of_min_so_far_and_other_array[i];
  }
}

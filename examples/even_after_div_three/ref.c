int even_after_div_three(int *arr, int n, int drop) {
  int count = 0;
  for (int i = drop; i < n; ++i) {
	if ((arr[i] / 3) % 2 == 0)
	  count ++;
  }

  return count;
}

void subtract_of_min_reverse(int *arr, int *arr2, int *arrout, int n) {
	for (int i = 0; i < n; i ++) {
		int e1 = arr[i];
		int e1_rev = arr[n - i - 1];
		int e2 = arr2[i];

		arrout[i] = e1 - ((e1_rev < e2) ? e1_rev : e2);
	}
}

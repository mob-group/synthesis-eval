int binary_mul_sum(int *arr1, int *arr2, int n) {
	int sum = 0;
	for (int i = 0; i < n; i ++) {
		arr2[i] = arr1[i] + arr2[i];
		sum += arr1[i] * arr2[i];
	}

	return sum;
}

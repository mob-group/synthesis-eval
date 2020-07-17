void elementwise_sum_of_negated_sum_and_max(int *arr, int *arr2, int *arrout, int n) {
	int negsum[n];
    int negsum_count = 1;
	for (int i = 0; i < n; i ++) {
        negsum_count -= arr[i];
        negsum[i] = negsum_count;
	}

	for (int i = 0; i < n; i ++) {
        int e1 = arr[i];
        int e2 = arr2[i];
        int n1 = negsum[i];
        int m = (e1 > e2) ? e1 : e2;

		arrout[i] = n1 + m;
	}
}

void sum_of_positives(int *arr, int *arr2, int *arrout, int n) {
	int outindex = 0;
	for (int i = 0; i < n; i ++) {
		if (arr[i] > 0) {
			int m = (arr[i] > arr2[i]) ? arr[i] : arr2[i];
			arrout[outindex] = arr[i] + m;
			outindex ++;
		}
	}
}

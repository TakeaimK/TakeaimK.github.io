#include <iostream>
using namespace std;

int d[10001];
int dn(int num) {
	int total = num;
	if (num  >= 10000){
		total += num  / 10000;
		num  %= 10000;
	}
	if (num  >= 1000){
		total += num  / 1000;
		num  %= 1000;
	}
	if (num  >= 100){
		total += num  / 100;
		num  %= 100;
	}
	if (num  >= 10){
		total += num  / 10;
		num  %= 10;
	}
	total+=num;
	return total;
}
int main() {
	for (int i = 1; i <= 10000; i++) {
		d[dn(i)] = 1;
		if (!d[i]) printf("%d\n", i);
	}
}
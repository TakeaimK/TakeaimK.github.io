#include <iostream>

using namespace std;

int main()
{

	int N, M, K;
	cin >> N >> M >> K;

	printf("%d %d", K / M, K % M);
}
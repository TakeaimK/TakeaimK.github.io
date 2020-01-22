#include <iostream>
#include <string>

using namespace std;

int main() {
	
	int i;
	string str;
	cin>>i;
	cin>>str;
	int temp=0;
	for(int j=0; j<i; j++){
		temp += (str.at(j)-'0');
	}
	cout<<temp;
}
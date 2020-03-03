#include <iostream>
using namespace std;

int main(void){
    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int a;
    int b;
    while(cin>>a>>b){
        cout<<a+b<<"\n";
    }
    //system("pause");
    return 0;
}

/*
int main(void) {

    int num;
    cin>>num;

    int a;
    int b;
    for(int i=0; i<num; i++){
        cin>>a>>b;
        cout<<a+b<<endl;
    }
    //system("pause");
    return 0;
}
*/
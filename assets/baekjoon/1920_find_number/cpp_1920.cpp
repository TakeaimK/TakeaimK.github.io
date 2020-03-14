#include <iostream>
using namespace std;

int main(void){
    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int num;
    int where=0;
    int max=-1;
    for(int i=1; i<10; i++){
        cin>>num;
        if(num>max){
            max=num;
            where=i;
        }
    }
    cout<<max<<"\n"<<where<<"\n";
    //system("pause");
    return 0;
}

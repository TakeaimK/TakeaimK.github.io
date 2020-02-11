#include <iostream>
#include <string>
using namespace std;

int main(void){
    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int arr[8];
    bool set = true;
    for(int i=0; i<8; i++){
        cin>>arr[i];
    }
        
    if(arr[0] == 1){
        for(int i=0; i<8; i++){
            if(arr[i] != i+1){
                cout<<"mixed"<<"\n";
                set=false;
                break;
            }
        }
        if(set){
            cout<<"ascending"<<"\n";
        }
        
    }
    else if(arr[0] == 8){
        for(int i=7; i>-1; i--){
            if(arr[7-i] != i+1){
                cout<<"mixed"<<"\n";
                set=false;
                break;
            }
        }
        if(set){
            cout<<"descending"<<"\n";
        }
        
    }
    else{
        cout<<"mixed"<<"\n";
    }
    //system("pause");
    return 0;
}

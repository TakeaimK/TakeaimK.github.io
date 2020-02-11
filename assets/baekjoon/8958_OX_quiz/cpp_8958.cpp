#include <iostream>
#include <string>
using namespace std;

int main(void){
    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int many = 0;
    int total = 0;
    int temp= 0 ;
    int connected = 0;
    string str = "";

    cin>>many;

    for(int i=0; i<many; i++){
        cin>>str;
        
        total=0;
        temp=0;
        connected=0;
        for(int j=0; j<str.length();j++){
            if(str.at(j) == 'O'){
                connected++;
                temp+=connected;
            }
            else{
                total+=temp;
                connected=temp=0;
            }
        }
        total+=temp;
        cout<<total<<"\n";
    }
    //system("pause");
    return 0;
}

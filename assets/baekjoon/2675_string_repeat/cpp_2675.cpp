#include <iostream>
#include <string>
using namespace std;

int main(void){
    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int many = 0;
    int repeat = 0;
    string str = "";
    string newstr = "";
   
    cin>>many;

    for(int i=0; i<many; i++){
        cin>>repeat>>str;
        
        for(int j=0; j<str.length(); j++){
            for(int k=0; k<repeat; k++){
                newstr += str.at(j);
            }
        }

        cout<<newstr<<"\n";
        newstr="";

    }

    //system("pause");
    return 0;
}

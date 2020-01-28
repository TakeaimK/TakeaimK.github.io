#include <iostream>
#include <vector>
 
using namespace std;
 
int main() {

 
    int start, end;
    cin >> start >> end;
    vector<bool> isPrime(end + 1, true);
 
    isPrime[0] = false;
    isPrime[1] = false;
    for (int i = 2; i <= end; i++) {
        if (isPrime[i]) {
           
            for (int j = 2 * i; j <= end; j += i)
                isPrime[j] = false;
        }
    }
 
    for(int i = start; i <= end; i++)
        if(isPrime[i])
            cout << i << endl;
 
    return 0;
}

/*
#include <iostream>
#include <cmath>
 
using namespace std;
 
int main() {

    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int start, end;
    cin >> start >> end;
    bool set;
 
    for (int i = start; i <= end; i++) {
        
        set=true;
        
        for (int j = 2 ; j <= floor(sqrt(i)); j++){
            if(i%j == 0){
                set=false;
                break;
            }
        }
        
        if(set && i>1){
            cout<<i<<'\n';
        }
        
    }
 
    return 0;
}


*/
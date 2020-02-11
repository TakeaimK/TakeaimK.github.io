---
layout: post
title: 14. OX 퀴즈
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.8958 : OX퀴즈](https://www.acmicpc.net/problem/8958)  

### 문제 난이도 (solved.ac 기준) : Bronze II  

### 문제 내용
![8958_OX_quiz](/assets/images/Baekjoon/8958_OX_quiz.PNG)  

### 입력 1
```
5
OOXXOXXOOO
OOXXOOXXOO
OXOXOXOXOXOXOX
OOOOOOOOOO
OOOOXOOOOXOOOOX
```
### 출력 1
```
10
9
7
55
30
```  

### 문제 이해
O가 연속적으로 나올 경우 누적해서 temp에 쌓고,  
X가 나올 경우 쌓은 값을 total에 넣고 temp를 0으로 초기화한다.  
마지막 문자 처리 후 temp를 다시 total에 넣어주고, total을 출력한다.  

### 소스 코드 (Python)
```python
if __name__ == "__main__":

    many = input()
    

    for _ in range(int(many)):
        temp=0
        connected=0
        total=0
        string = input()
        for i in range(len(string)):
            if(string[i] == "O"):
                connected+=1
                temp+=connected
            else:
                total+=temp
                connected=0
                temp=0
        
        total+=temp
        print(total)

```  


### 소스 코드 (Java)
```java
import java.util.Scanner;

public class java_8958 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int many = 0;
        int total = 0;
        int temp= 0 ;
        int connected = 0;
        String str = "";

        many = scan.nextInt();

        for(int i=0; i<many; i++){
            str = scan.next();
            scan.nextLine();

            total=0;
            temp=0;
            connected=0;

            for(int j=0; j<str.length();j++){
                if(str.charAt(j) == 'O'){
                    connected++;
                    temp+=connected;
                }
                else{
                    total+=temp;
                    connected=temp=0;
                }
            }
            total+=temp;
            System.out.println(total);
            
            
            //scan.nextLine();
            
        }   
    }
}
```  

### 소스 코드 (C++)

```cpp
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

```


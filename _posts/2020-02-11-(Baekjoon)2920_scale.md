---
layout: post
title: 13. 음계
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2920 : 음계](https://www.acmicpc.net/problem/2920)  

### 문제 난이도 (solved.ac 기준) : Bronze II  

### 문제 내용
![2920_scale](/assets/images/Baekjoon/2920_scale.PNG)  

### 입력 1
```
1 2 3 4 5 6 7 8
```
### 출력 1
```
ascending
```  
### 입력 2
```
8 7 6 5 4 3 2 1
```
### 출력 2
```
descending
```  
### 입력 3
```
8 1 7 2 6 3 5 4
```
### 출력 3
```
mixed
```  

### 문제 이해
첫 번째로 입력받은 수가 1이라면, ascending인지 비교.  
중간에 하나라도 아닐 경우 mixed 출력
첫 번째로 입력받은 수가 8이라면, descending인지 비교.  
중간에 하나라도 아닐 경우 mixed 출력
첫 번째로 입력받은 수가 1도 8도 아니라면, mixed 출력.

### 소스 코드 (Python)
```python
if __name__ == "__main__":
    
    set=0
    dingdong = list(map(int, input().split()))
    if(dingdong[0]==1):
        for i in range(0, 8):
            if(dingdong[i]!=i+1):
                print("mixed")
                set=1
                break
        if(set==0):
            print("ascending")

    elif(dingdong[0]==8):
        for i in range(7, -1, -1):
            if(dingdong[7-i]!=i+1):
                print("mixed")
                set=1
                break
        if(set==0):
            print("descending")
    else:
        print("mixed")
        

```  


### 소스 코드 (Java)
```java
import java.util.Scanner;

public class java_2920 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int arr[] = new int[8];
        boolean set = true;

        for(int i=0; i<8; i++){
            arr[i] = scan.nextInt();
        }
            
        if(arr[0] == 1){
            for(int i=0; i<8; i++){
                if(arr[i] != i+1){
                    System.out.println("mixed");
                    set=false;
                    break;
                }
            }
            if(set){
                System.out.println("ascending");
            }
            
        }
        else if(arr[0] == 8){
            for(int i=7; i>-1; i--){
                if(arr[7-i] != i+1){
                    System.out.println("mixed");
                    set=false;
                    break;
                }
            }
            if(set){
                System.out.println("descending");
            }
            
        }
        else{
            System.out.println("mixed");
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

```


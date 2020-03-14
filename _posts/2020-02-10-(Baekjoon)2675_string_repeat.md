---
layout: post
title: 14. 문자열 반복
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2675 : 문자열 반복](https://www.acmicpc.net/problem/2675){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze II

### 문제 내용

![2675_max](/assets/images/Baekjoon/2675_string_repeat.PNG)

### 입력 1

```
2
3 ABC
5 /HTP
```

### 출력 1

```
AAABBBCCC
/////HHHHHTTTTTPPPPP
```

### 문제 이해

문자열을 받아 글자 별로 지정된 횟수만큼 늘려쓰는 새로운 문자열을 만들어 출력한다.

### 소스 코드 (Python)

```python
if __name__ == "__main__":

    newstr = ""

    many = input()
    for _ in range(int(many)):
        temp = input().split()
        repeat = temp[0]
        string = temp[1]

        for i in range(len(string)):    #string의 길이만큼
            for _ in range(int(repeat)):    #문자열의 i번째 문자를 repeat번 만큼 이어붙인다
                newstr+=string[i]      #문자열에도 연산자로 이어붙이기가 가능

        print(newstr)
        newstr=""
```

### 소스 코드 (Java)

```java
import java.util.Scanner;

public class java_2675 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int many = 0;
        int repeat = 0;
        String str = "";
        String newstr = "";

        many = scan.nextInt();

        for(int i=0; i<many; i++){
            repeat = scan.nextInt();
            str = scan.next();
            scan.nextLine();

            for(int j=0; j<str.length();j++){
                for(int k=0; k<repeat; k++){
                    newstr+=str.charAt(j);
                }
            }
            System.out.println(newstr);
            newstr = "";
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

```

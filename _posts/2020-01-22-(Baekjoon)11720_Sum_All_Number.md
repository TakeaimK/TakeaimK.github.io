---
layout: post
title: 3. 숫자의 합
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon_NO.11720_숫자의 합](https://www.acmicpc.net/problem/11720)  

### 문제 난이도 (solved.ac 기준) : Bronze II  

### 문제 내용
![4673_self_number](/assets/images/Baekjoon/11720_sum_all_number.PNG)  

### 입력 1
```
1
1
```
### 출력 1
```
1
```  
### 입력 2
```
5
54321
```
### 출력 2
```
15
```  
### 입력 3
```
11
10987654321
```
### 출력 3
```
46
```  

### 문제 이해  
1. 더할 숫자의 길이 값을 받고  
2. 숫자로 이루어진 문자열을 각각 분해  
3. 더해서 출력  

### 소스 코드 (Python)
```Python
i = int(input())
string = input()       #일단 문자열로 입력받음
num = 0

for j in range(i):      #0부터 i-1까지
    num += int(string[j])   #문자열 한 자리씩 더하기

print(num)  #결과 출력
```  

### 소스 코드 (Java)
```Java

import java.util.Scanner;

public class java_11720{    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int i = scan.nextInt();
        String str = scan.next();

        int temp=0;

        for(int j=0; j<i; j++){
            temp += Character.getNumericValue(str.charAt(j)); 
        }

        System.out.println(temp);
    }
    
}
```  

### 소스 코드 (C++)
```C++
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
```

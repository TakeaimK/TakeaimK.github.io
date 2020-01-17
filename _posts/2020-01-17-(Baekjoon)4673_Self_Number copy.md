---
layout: post
title: 1. 4673번_셀프 넘버
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon_NO.4673_셀프 넘버](https://www.acmicpc.net/problem/4673)  

### 문제 난이도 (solved.ac 기준) : Bronze I  

### 문제 내용
![4673_self_number](/assets/images/Baekjoon/4673_self_number.PNG)  

### 입력
```
(없음)
```
### 출력
```
1
3
5
7
9
20
31
42
53
64
 |
 |       <-- a lot more numbers
 |
9903
9914
9925
9927
9938
9949
9960
9971
9982
9993
```  

### 문제 이해
셀프 넘버에 대해 간략하게 설명하자면, 자기 자신과 각 자릿수를 더한 수로 나오지 않는 수이다.  
예를 들면 다음과 같다.  
(한 자릿수 - 6의 경우) : 6+6=12, 12는 셀프 넘버가 아님  
(두 자릿수 - 24의 경우) : 24+2+4=30, 30은 셀프 넘버가 아님
(세 자릿수 - 396의 경우) : 396+3+9+6=414는 셀프 넘버가 아님  
즉, 범위 내에서 **셀프 넘버가 아닌 수를 제거**하면 셀프 넘버만 남게 된다.  
셀프 넘버가 아닌 수를 구하는 방법은 다음과 같다.  
__(본인 자신의 수) + (일의 자리 수) + (십의 자리 수) + ...__  
그러면 위 이해를 토대로 코드를 작성해 보자.  

### 소스 코드 (Python)
```
def non_self_number(num):
    total=num
    if(num>=10000):  #수가 10000이 넘으면
        total+=(num//10000)  #만의 자릿수를 total에 더함
        num=(num%10000)     #num에서 만의 자릿수 제거
    if(num>=1000):  #수가 1000이 넘으면
        total+=(num//1000)  #천의 자릿수를 total에 더함
        num=(num%1000)     #num에서 천의 자릿수 제거
    if(num>=100):  #수가 100이 넘으면
        total+=(num//100)  #백의 자릿수를 total에 더함
        num=(num%100)     #num에서 백의 자릿수 제거    
    if(num>=10):  #수가 10이 넘으면
        total+=(num//10)  #십의 자릿수를 total에 더함
        num=(num%10)     #num에서 십의 자릿수 제거
    total+=num  #일의 자릿수를 total에 더함
    return total

arr=[0 for _ in range(100000)]

for i in range(1, 10001):
    arr[non_self_number(i)]=1
    if(arr[i]==0):
        print(i)
```  

### 소스 코드 (Java)
```


public class java_4673{    // 채점 시 Class 명을 'Main'으로 변경

    private static int non_self_number(int num) {
        int total = num;
        if (num >= 10000) {
            total += num / 10000;
            num %= 10000;
        }
        if (num >= 1000) {
            total += num / 1000;
            num %= 1000;
        }
        if (num >= 100) {
            total += num / 100;
            num %= 100;
        }
        if (num >= 10) {
            total += num / 10;
            num %= 10;
        }
        total += num;
        return total;
    }

    public static void main(String[] args) {

        int arr[] = new int[100000];

        for (int i = 1; i < 10001; i++) {
            arr[non_self_number(i)] = 1;
            if(arr[i]==0){
                System.out.println(i);
            }
        }
    }
    
}
```  

### 소스 코드 (C++)
```
#include <iostream>
using namespace std;

int d[10001];
int dn(int i) {
	int res = i;
	if (i >= 10000) { res += i / 10000; i %= 10000; }
	if (i >= 1000) { res += i / 1000; i %= 1000; }
	if (i >= 100) { res += i / 100; i %= 100; }
	if (i >= 10) { res += i / 10; i %= 10; }
	return res += i;
}
int main() {
	for (int i = 1; i <= 10000; i++) {
		d[dn(i)] = 1;
		if (!d[i]) printf("%d\n", i);
	}
}
```

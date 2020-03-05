---
layout: post
title: 8. 구구단
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2739 : 구구단](https://www.acmicpc.net/problem/2739){: target="_blank"}  

### 문제 난이도 (solved.ac 기준) : Bronze III  

### 문제 내용
![2739_구구단](/assets/images/Baekjoon/2739_Multiplication_table.PNG)  

### 입력 1
```
2
```
### 출력 1
```
2 * 1 = 2
2 * 2 = 4
2 * 3 = 6
2 * 4 = 8
2 * 5 = 10
2 * 6 = 12
2 * 7 = 14
2 * 8 = 16
2 * 9 = 18
```  

### 문제 이해
매우 단순한 문제이다. for문을 활용해 9번 곱한 값까지 출력하면 된다.

### 소스 코드 (Python)
```python
num = int(input())

for i in range(1, 10):
    print("%d * %d = %d" %(num, i, num*i))
```  


### 소스 코드 (Java)
```java
import java.util.Scanner;

public class java_2739{    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int num = scan.nextInt();
        for(int i=1; i<10; i++){
            System.out.println(num+" * "+i+" = "+(num*i));
        }
    }
    
}
```  

### 소스 코드 (C++)

```cpp
#include <iostream>

using namespace std;

int main() {

	int num;
	cin>>num;

	for(int i=1; i<10; i++){
		printf("%d * %d = %d\n", num, i, (num*i));
	}
		
}
```


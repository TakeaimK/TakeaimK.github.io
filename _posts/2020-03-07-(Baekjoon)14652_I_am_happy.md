---
layout: post
title: 25. 나는 행복합니다~
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.14652 : 나는 행복합니다~](https://www.acmicpc.net/problem/14652){: target="_blank"}  

### 문제 난이도 (solved.ac 기준) : Bronze V

### 문제 내용
![14652_I_am_happy](/assets/images/Baekjoon/14652_I_am_happy.PNG)  

### 입력 1
```
3 4 6
```
### 출력 1
```
1 2
```  

### 입력 2
```
6 4 14
```
### 출력 2
```
3 2
```  

### 문제 이해
매우 간단하지만, 2중 반복문과 조건문을 사용하면 시간초과가 발생한다. ~~시간초과만 3번 났다~~  
주어진 번호를 가로길이로 나누어 몫은 세로, 나머지는 가로 값이다.  

### 소스 코드 (Python)
```python
if __name__ == "__main__":

    N, M, K = map(int, input().strip().split())

    print("%d %d" % (K//M, K % M))

```

### 소스 코드 (Java)
```java
import java.util.Scanner;

public class java_14652 { // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int N = scan.nextInt();
        int M = scan.nextInt();
        int K = scan.nextInt();

        System.out.println(K / M + " " + K % M);
    }

}
```  

### 소스 코드 (C++)

```cpp
#include <iostream>

using namespace std;

int main()
{

	int N, M, K;
	cin >> N >> M >> K;

	printf("%d %d", K / M, K % M);
}
```


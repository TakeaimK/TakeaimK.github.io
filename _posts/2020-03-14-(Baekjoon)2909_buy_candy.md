---
layout: post
title: 34. 캔디 구매
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2909 : 캔디 구매](https://www.acmicpc.net/problem/2909){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze II

### 문제 내용

![2909_buy_candy](/assets/images/Baekjoon/2909_buy_candy.PNG)

### 입력 1

```
184 1
```

### 출력 1

```
180
```

### 문제 이해

반올림의 자리가 0의 갯수에 따라 매번 달라짐에 유의해야 한다.  
즉, 반올림이 가능한지 비교하는 것 뿐 아니라, 결과값도 0의 갯수에 따라 반올림된 값이 다르다.

---

### 소스 코드 (Python)

```python

if __name__ == "__main__":

    price, zero = map(int, input().strip().split())

    zero = int(str(1) + str(0)*zero)
    temp = price % zero
    if temp >= zero//2:
        print((price//zero) * zero + 1*zero)
    else:
        print((price//zero) * zero)

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

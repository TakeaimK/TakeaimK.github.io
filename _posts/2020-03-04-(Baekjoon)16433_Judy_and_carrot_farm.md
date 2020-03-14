---
layout: post
title: 24. 주디와 당근 농장
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.16433 : 주디와 당근 농장](https://www.acmicpc.net/problem/16433){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze I

### 문제 내용

![16433_Judy_and_carrot_farm](/assets/images/Baekjoon/16433_Judy_and_carrot_farm.PNG)

### 입력 1

```
4 2 3
```

### 출력 1

```
.v.v
v.v.
.v.v
v.v.
```

![16433_Judy_and_carrot_farm](/assets/images/Baekjoon/16433_Judy_and_carrot_farm_sample.PNG)

### 문제 이해

1. 당근이 심긴 행 값과 열 값이 짝수인지 홀수인지 파악한다.
2. 짝수 행과 홀수 행이 동일한 값을 가짐을 이용한다. 즉, 짝수 행이라면 짝수 행끼리는 동일한 출력을 가진다.
3. 당근의 열 위치를 보고 짝수라면 짝수 열에 `v`를, 홀수 열에 `.`을 심는다. 홀수라면 반대로 심는다.
4. 행이 바뀔 때마다 개행을 넣어준다.

### 문제 이해 (간결한 풀이)

1. 당근을 심은 위치의 행+열 값이 짝수인지 홀수인지 파악한다.
2. 행+열 값이 짝수라면 짝수 칸에만 심으면 되고, 홀수라면 홀수 칸에만 심으면 된다.

### 문제풀이 Tip

- 배열을 이용하여 풀 수 있지만, 배열은 0부터 시작하기 때문에 조심해야 한다. 문제는 1부터 시작하는 밭을 사용한다.
- 파이썬 풀이에서 print("v", end='') 를 사용할 경우 개행이 되지 않는다.

### 소스 코드 (Python)

```python
if __name__ == "__main__":

    n, row, col = map(int, input().split())

    if row % 2 == 0:
        if col % 2 == 0:
            for i in range(1, n+1):
                for j in range(1, n+1):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                    else:
                        if j % 2 == 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                print("")
        else:
            for i in range(1, n+1):
                for j in range(1, n+1):
                    if i % 2 == 0:
                        if j % 2 != 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                    else:
                        if j % 2 != 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                print("")

    else:
        if col % 2 == 0:
            for i in range(n):
                for j in range(n):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                    else:
                        if j % 2 == 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                print("")
        else:
            for i in range(n):
                for j in range(n):
                    if i % 2 == 0:
                        if j % 2 != 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                    else:
                        if j % 2 != 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                print("")

```

### 소스 코드 (Python - 간결한 풀이)

```python
if __name__ == "__main__":

    n, row, col = map(int, input().split())

    if (row + col) % 2 == 0:
        for i in range(n):
            if i % 2 == 0:
                print("v." * (n // 2) + 'v' * (n % 2))
            else:
                print(".v" * (n // 2) + '.' * (n % 2))

    else:
        for i in range(n):
            if i % 2 == 1:
                print("v." * (n // 2) + 'v' * (n % 2))
            else:
                print(".v" * (n // 2) + '.' * (n % 2))



```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

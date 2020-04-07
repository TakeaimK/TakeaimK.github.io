---
layout: post
title: 42. 연구소
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.14502 : 연구소](https://www.acmicpc.net/problem/14502){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Gold V

### 문제 내용

![14502_institute](/assets/images/Baekjoon/14502_institute.PNG)

### 입력 1

```
7 7
2 0 0 0 1 1 0
0 0 1 0 1 2 0
0 1 1 0 1 0 0
0 1 0 0 0 0 0
0 0 0 0 0 1 1
0 1 0 0 0 0 0
0 1 0 0 0 0 0
```

### 출력 1

```
27
```

### 입력 2

```
4 6
0 0 0 0 0 0
1 0 0 0 0 2
1 1 1 0 0 2
0 0 0 0 0 2
```

### 출력 2

```
9
```

### 입력 3

```
8 8
2 0 0 0 0 0 0 2
2 0 0 0 0 0 0 2
2 0 0 0 0 0 0 2
2 0 0 0 0 0 0 2
2 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

### 출력 3

```
3
```

### 문제 이해

### 소스 코드 (Python) - 나의 풀이

```python
import sys
input = sys.stdin.readline

if __name__ == "__main__":
    n, m = map(int, input().split())
    d = set()
    count = 0
    ans = []
    for _ in range(n):
        t = input().strip()
        d.add(t)
    for _ in range(m):
        t = input().strip()
        if t in d:
            count += 1
            ans.append(t)
    ans.sort()
    print(count)
    for t in ans:
        print(t)
```

### 소스 코드 (Python) - 집합자료형 2개 사용 빠른 풀이

```python

N, M = map(int, input().split())
a = set()
b = set()
for i in range(N):
    a.add(input())
for i in range(M):
    b.add(input())
l = list(a&b)
print(len(l))
for e in sorted(l):
    print(e)
```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

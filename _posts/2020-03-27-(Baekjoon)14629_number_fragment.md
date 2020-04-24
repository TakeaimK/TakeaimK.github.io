---
layout: post
title: 42. 숫자 조각
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.14629 : 숫자 조각](https://www.acmicpc.net/problem/14629){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용

![14629_number_fragment](/assets/images/Baekjoon/14629_number_fragment.PNG)

### 입력 1

```
333
```

### 출력 1

```
329
```

### 문제 이해

본 문제를 list 자료형을 사용하게 되면 시간초과로 터지게 된다. 따라서 집합 자료형을 사용하여 문제를 해결한다.  
[파이썬의 집합 자료형](https://wikidocs.net/1015)  

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

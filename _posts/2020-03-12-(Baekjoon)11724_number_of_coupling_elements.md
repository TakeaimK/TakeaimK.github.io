---
layout: post
title: 32. 연결 요소의 갯수
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.11724 : 연결 요소의 갯수](https://www.acmicpc.net/problem/11724){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver II

### 문제 내용

![11724_number_of_coupling_elements](/assets/images/Baekjoon/11724_number_of_coupling_elements.PNG)

### 입력 1

```
6 5
1 2
2 5
5 1
3 4
4 6
```

### 출력 1

```
2
```

### 입력 2

```
6 8
1 2
2 5
5 1
3 4
4 6
5 4
2 4
2 3
```

### 출력 2

```
1
```

### 문제 이해

간만에 DFS로 풀기 좋은 문제가 나왔다. 가장 기본적인 DFS 자료구조 형태로 이해하면 풀기 어렵지 않다.  
일단 연결 요소의 수를 구하라는 말을 간단히 풀이해 보면, 이어지지 않은 꾸러미 갯수가 몇 개인지 묻는 것이다. 이 꾸러미 갯수를 조사하기 위해, 점에 방문했는지 확인할 수 있는 visit(방문 표식)과 한 점에 간선으로 이어지는 다른 점들의 꾸러미(m_list)가 필요하다.

1. 점을 순서대로 방문 여부를 조회한다. 해당 점이 아직 방문하지 않았다면 count+1을 한 뒤, 해당 점에 방문 표식을 남긴다. 모든 점에 방문했다면 count를 출력한다.
2. m_list를 참고하여 간선을 타고 내려가면서 방문 표식을 남기고, 더이상 갈 수 없을 때에는 한 칸씩 다시 돌아오며 갈 수 있을 때까지 찾는다.
3. 이어진 모든 간선을 타고 방문 표식을 남긴 뒤 최종적으로 더이상 갈 수 없다면 1번을 반복한다.

---

### 소스 코드 (Python)

```python

import sys

input = sys.stdin.readline
sys.setrecursionlimit(10**6)


def coupling_elements(N, M, arr, m_list):

    count = 0
    for i in range(1, N+1):
        if arr[i] != True:
            count += 1
            dfs(i)
    return count


def dfs(x):
    visit[x] = True
    for i in m_list[x]:
        if visit[i] != True:
            dfs(i)


if __name__ == "__main__":
    N, M = map(int, input().split())
    visit = [False for _ in range(N+1)]
    m_list = [[] for i in range(N+1)]

    for i in range(M):  # 행 수만큼 반복
        x, y = map(int, input().split())  # strip : 문자열 양쪽 공백을 지우기
        m_list[x].append(y)
        m_list[y].append(x)

    print(coupling_elements(N, M, visit, m_list))

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

---
layout: post
title: 39. 경로 찾기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.11403 : 경로 찾기](https://www.acmicpc.net/problem/11403){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용

![11403_find_path](/assets/images/Baekjoon/11403_find_path.PNG)

### 입력 1

```
3
0 1 0
0 0 1
1 0 0
```

### 출력 1

```
1 1 1
1 1 1
1 1 1
```

### 입력 2

```
7
0 0 0 1 0 0 0
0 0 0 0 0 0 1
0 0 0 0 0 0 0
0 0 0 0 1 1 0
1 0 0 0 0 0 0
0 0 0 0 0 0 1
0 0 1 0 0 0 0
```

### 출력 2

```
1 0 1 1 1 1 1
0 0 1 0 0 0 1
0 0 0 0 0 0 0
1 0 1 1 1 1 1
1 0 1 1 1 1 1
0 0 1 0 0 0 1
0 0 1 0 0 0 0
```

### 문제 이해

가장 기본적인 bfs를 활용하는 문제이다. 방문한 곳(visit)을 체크해 주고 가능한 모든 곳을 방문하고 나면 방문한 곳은 1로, 방문하지 못한 곳은 0으로 체크해 주면 된다.  
좀 더 상세히 설명하면 다음과 같다.

1. 모든 값을 arr에 입력받고, 한 줄씩 꺼낸다.
2. 현재 연결된 노드 번호 (1로 set된 위치)를 모아 큐에 넣는다.
3. 큐에서 노드 번호를 하나씩 꺼내서 해당 노드 번호의 visit을 True로 set한다.
4. arr에서 노드 번호에 해당하는 행을 tnode에 저장한다.
5. tnode에 대해 순차적으로 훑으며 아직 방문하지 않았으면서 tnode가 1인 경우의 위치 값을 큐에 넣는다.
6. 3~5를 큐가 모두 빌 때까지 반복한다.
7. visit가 True인 경우 1, 아닌 경우 0으로 바꾸어 리턴한다.

### 소스 코드 (Python)

```python
import sys
import copy

input = sys.stdin.readline


def find_path_bfs(arr, N, node):

    search = []
    tnode = []
    ret = [0 for _ in range(N)]
    visit = [False for _ in range(N)]

    for i in range(N):
        if node[i] == 1:
            search.append(i)

    # total_count = 0
    # first_search = False

    while search:
        x = search.pop(0)
        visit[x] = True
        now = []
        # first_search = False
        now.append(x)
        while now:
            nowx = now.pop(0)
            tnode = arr[nowx]
            visit[nowx] = True
            for i in range(N):
                if tnode[i] == 1 and visit[i] == False:
                    now.append((i))
        # if first_search:
        #     area.append(now_count)
    for i in range(N):
        if visit[i] == True:
            ret[i] = 1
    return ret


if __name__ == "__main__":
    N = int(input())

    arr = [[0 for _ in range(N)]for _ in range(N)]
    ans = [[0 for _ in range(N)]for _ in range(N)]

    for i in range(N):
        temp = (list(map(int, input().strip().split())))
        arr[i] = temp

    # for i in range(N):
    #     for j in range(N):
    #         if arr[i][j] == 1:
    #             arr[j][i] = 1

    for i in range(N):
        ans[i] = find_path_bfs(arr, N, arr[i])
    for i in range(len(ans)):
        print(" ".join(map(str, ans[i])))

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

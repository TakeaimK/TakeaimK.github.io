---
layout: post
title: 17. 미로 탐색
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2178 : 미로 탐색](https://www.acmicpc.net/problem/2178){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용

![2178_maze_search](/assets/images/Baekjoon/2178_maze_search.PNG)

### 입력 1

```
4 6
101111
101010
101011
111011
```

### 출력 1

```
15
```

### 입력 2

```
4 6
110110
110110
111111
111101
```

### 출력 2

```
9
```

### 입력 3

```
2 25
1011101110111011101110111
1110111011101110111011101
```

### 출력 3

```
38
```

### 입력 4

```
7 7
1011111
1110001
1000001
1000001
1000001
1000001
1111111
```

### 출력 4

```
13
```

### 문제 이해

기존에 풀었던 DFS 또는 BFS를 사용하여 해결할 수 있다.  
[DFS와 BFS : Baekjoon NO.1260](<http://takeaimk.tk/baekjoon/2020/01/23/(Baekjoon)1260_DFS_BFS.html>)  
처음 생각한 풀이법은 DFS, 즉 함수 재귀를 사용하여 목적지에 도달할 경우 return하여 값을 더하는 방식을 사용해서 해결하였다.
그러나 이 방식은 가능한 모든 방법을 탐색하기에 백준에서 시간초과가 발생(...)했다.  
따라서 최종 해결은 BFS를 사용하였으며, 두 가지 소스 코드를 모두 첨부하였다.

---

본 문제를 풀다 막혀 도움을 얻어 알게 된 사실

- Python은 Call By Reference 방식을 사용하여 List, Dict 등의 자료형은 데이터가 공유된다.
  > [Python 은 call-by-value 일까 call-by-reference 일까](https://www.pymoon.com/entry/Python-%EC%9D%80-callbyvalue-%EC%9D%BC%EA%B9%8C-callbyreference-%EC%9D%BC%EA%B9%8C)
- 즉, List나 Dict 자료형을 사용하면서 Call By Value 방식을 사용하려면 다음과 같은 방식을 사용한다.
  > [얕은 복사와 깊은 복사 - deepcopy](https://wikidocs.net/16038)
- Python에서 2차원 배열은 다음과 같이 쉽게 생성이 가능하다.
  > [Python에서 2차원 배열 생성](https://andrew0409.tistory.com/53)

### 소스 코드 (Python - DFS)

```python
import sys
import copy
sys.setrecursionlimit(10**6)

def maze_runner(arr, row, col, nr, nc) :
    a = 10001
    b = 10001
    c = 10001
    d = 10001
    min = 10001

    if(nr == row and col == nc):
        return 1
    else:
        tarr = copy.deepcopy(arr)
        tarr[nr][nc] = 0
        if(arr[nr+1][nc] == 1):
            a = maze_runner(tarr, row, col, nr+1, nc)
            if(min>a):
                min = a
        if(arr[nr-1][nc] == 1):
            b = maze_runner(tarr, row, col, nr-1, nc)
            if(min>b):
                min = b
        if(arr[nr][nc+1] == 1):
            c = maze_runner(tarr, row, col, nr, nc+1)
            if(min>c):
                min = c
        if(arr[nr][nc-1] == 1):
            d = maze_runner(tarr, row, col, nr, nc-1)
            if(min>d):
                min = d
        return min+1


if __name__ == "__main__":

    ans = 0

    row, col = map(int, input().split())

    arr = [[0 for _ in range(col+2)] for _ in range(row+2)]
    tstr = ""

    for i in range(1,row+1):
        tstr = input()
        for j in range(1,col+1):
            arr[i][j] = int(tstr[j-1])

    ans = maze_runner(arr, row, col, 1, 1)

    print(ans)


```

### 소스 코드 (Python - BFS)

```python
def bfs(arr, visit, row, col) :
    queue = []
    queue.append((0,0))
    visit[0][0] = 1

    dx = [0,0,1,-1]
    dy = [1,-1,0,0]

    while queue:
        x, y = queue.pop(0)
        if x == row-1 and y == col-1:
            return visit[x][y]
        for i in range(4):
            movx = x + dx[i]
            movy = y + dy[i]
            if movx>=0 and movx<row and movy>=0 and movy<col:
                if visit[movx][movy] == 0 and arr[movx][movy] == 1:
                    visit[movx][movy] = visit[x][y]+1
                    queue.append((movx, movy))


if __name__ == "__main__":

    ans = 0

    row, col = map(int, input().split())

    arr = [[0 for _ in range(col)] for _ in range(row)]
    visit = [[0 for _ in range(col)] for _ in range(row)]
    tstr = ""

    for i in range(row):
        tstr = input()
        for j in range(col):
            arr[i][j] = int(tstr[j])

    ans = bfs(arr, visit, row, col)

    print(ans)


```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp


```

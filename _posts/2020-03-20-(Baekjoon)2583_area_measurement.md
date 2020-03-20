---
layout: post
title: 37. 영역 구하기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2583 : 영역 구하기](https://www.acmicpc.net/problem/2583){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Gold V

### 문제 내용

![2583_area_measurement_1](/assets/images/Baekjoon/2583_area_measurement_1.PNG)
![2583_area_measurement_2](/assets/images/Baekjoon/2583_area_measurement_2.PNG)

### 입력 1

```
5 7 3
0 2 4 4
1 1 2 5
4 0 6 2
```

### 출력 1

```
3
1 7 13
```

### 문제 이해

[단지 번호 붙이기](<http://takeaimk.tk/baekjoon/2020/03/13/(Baekjoon)2667_building_site_numbering.html>){: target="\_blank"} , [양치기 꿍](<http://takeaimk.tk/baekjoon/2020/03/11/(Baekjoon)3187_shepherd_goong.html>){: target="\_blank"} 문제와 거의 유사한, bfs 풀이 문제이다.

### 소스 코드 (Python)

```python
import sys

input = sys.stdin.readline


def area_measurement_dfs(arr, squre, M, N):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    total_count = 0
    area = []
    first_search = False

    while squre:

        x, y = squre.pop(0)
        now = []
        first_search = False

        if arr[x][y] == 1:
            now.append((x, y))
            total_count += 1
            now_count = 0
            first_search = True
        while now:
            nowx, nowy = now.pop(0)
            if arr[nowx][nowy] == 1:
                now_count += 1
                arr[nowx][nowy] = 0
                for i in range(4):
                    tempx = nowx + dx[i]
                    tempy = nowy + dy[i]
                    if tempx >= 0 and tempx < M and tempy >= 0 and tempy < N:
                        if arr[tempx][tempy] == 1:
                            now.append((tempx, tempy))
        if first_search:
            area.append(now_count)
    return total_count, area


if __name__ == "__main__":
    M, N, K = map(int, input().strip().split())

    arr = [[1 for _ in range(N)]for _ in range(M)]
    squre = []

    for _ in range(K):
        sx, sy, ex, ey = map(int, input().strip().split())
        for i in range(sy, ey):
            for j in range(sx, ex):
                arr[i][j] = 0

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                squre.append((i, j))
    count, ans = area_measurement_dfs(arr, squre, M, N)
    print(count)
    ans.sort()
    print(" ".join(map(str, ans)))

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

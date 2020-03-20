---
layout: post
title: 38. 안전 영역
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2468 : 안전 영역](https://www.acmicpc.net/problem/2468){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용

![2468_safety_area_1](/assets/images/Baekjoon/2468_safety_area_1.PNG)
![2468_safety_area_2](/assets/images/Baekjoon/2468_safety_area_2.PNG)

### 입력 1

```
5
6 8 2 6 2
3 2 3 4 6
6 7 3 3 2
7 2 5 3 6
8 9 5 2 7
```

### 출력 1

```
5
```

### 문제 이해

[단지 번호 붙이기](<http://takeaimk.tk/baekjoon/2020/03/13/(Baekjoon)2667_building_site_numbering.html>){: target="\_blank"} , [양치기 꿍](<http://takeaimk.tk/baekjoon/2020/03/11/(Baekjoon)3187_shepherd_goong.html>){: target="\_blank"}, [영역 구하기](<http://takeaimk.tk/baekjoon/2020/03/20/(Baekjoon)2583_area_measurement.html>){: target="\_blank"} 문제와 유사하지만, 약간 변형되어 있다.
일단, 가능한 물의 높이는 문제에서는 100 이하의 정수로 주지만, 우리는 굳이 모든 경우의 수에 100까지 잠기게 할 필요는 없다. 받은 높이 중 (가장 높은 곳)-1 의 경우까지만 돌려보면 된다. 어차피 그 이상은 모두 물에 잠기게 될 터이니 말이다.  
물에 잠긴 곳은 0으로 바꿔 계산하고, 매번 deepcopy를 통해 배열을 새로 복사해 와서 물의 높이에 따라 가장 많이 살아남는 경우를 구해 기존 최댓값과 비교한다. 결국 다른 문제와는 bfs를 여러 번 돌린다는 차이점이 있다.

### 소스 코드 (Python)

```python
import sys
import copy

input = sys.stdin.readline


def safety_area_dfs(arr, N, flow):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    search = []
    tarr = copy.deepcopy(arr)
    for i in range(N):
        for j in range(N):
            if tarr[i][j] <= flow:
                tarr[i][j] = 0
            else:
                search.append((i, j))

    total_count = 0
    first_search = False

    while search:

        x, y = search.pop(0)
        now = []
        first_search = False

        if tarr[x][y] != 0:
            now.append((x, y))
            total_count += 1
            # now_count = 0
            # first_search = True
        while now:
            nowx, nowy = now.pop(0)
            if tarr[nowx][nowy] != 0:
                # now_count += 1
                tarr[nowx][nowy] = 0
                for i in range(4):
                    tempx = nowx + dx[i]
                    tempy = nowy + dy[i]
                    if tempx >= 0 and tempx < N and tempy >= 0 and tempy < N:
                        if tarr[tempx][tempy] != 0:
                            now.append((tempx, tempy))
        # if first_search:
        #     area.append(now_count)
    return total_count


if __name__ == "__main__":
    N = int(input())

    arr = [[1 for _ in range(N)]for _ in range(N)]
    top = 0
    ans = 1

    for i in range(N):
        temp = (list(map(int, input().strip().split())))
        arr[i] = temp
        top = max(max(temp), top)

    for i in range(1, top):
        safety = safety_area_dfs(arr, N, i)
        ans = max(safety, ans)
    print(ans)

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

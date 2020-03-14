---
layout: post
title: 25. 유기농 배추
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.1012 : 유기농 배추](https://www.acmicpc.net/problem/1012){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용

![1012_organic_cabbage](/assets/images/Baekjoon/1012_organic_cabbage_1.PNG)  
![1012_organic_cabbage](/assets/images/Baekjoon/1012_organic_cabbage_2.PNG)

### 입력 1

```
2
10 8 17
0 0
1 0
1 1
4 2
4 3
4 5
2 4
3 4
7 4
8 4
9 4
7 5
8 5
9 5
7 6
8 6
9 6
10 10 1
5 5
```

### 출력 1

```
5
1
```

### 문제 이해

본 문제는 보통 DFS로 푸는 경우가 많다. 전체 배열을 검사하여 최초 1을 발견하면 0으로 바꾸어 주고, 상하좌우를 검사 후 1이 있을 경우 해당 위치로 이동하여 0으로 바꾸어 주는 작업을 반복하고, 인접 값이 전부 1에서 0으로 바뀌고 돌아오면 count+1을 하는 식으로 말이다.  
그러나 지난 토마토 문제[(Link)](<http://takeaimk.tk/baekjoon/2020/03/01/(Baekjoon)7576_Tomato.html>){: target="\_blank"} 의 코드를 약간만 수정한다면 이 문제에도 써먹을 수 있겠다는 생각에 BFS로 풀이하였다. 풀이법은 다음과 같다.

1. 일단 토마토를 넣은 좌표의 밭을 1로 바꿈과 동시에 좌표 값도 따로 저장
2. 좌표의 값을 하나씩 꺼내서 그 칸 값이 1인지 확인. 1이면 하단 3번을 진행하고 0이면 continue
3. count+1을 한 뒤 현재 칸을 포함 bfs로 인접 칸의 1을 전부 0으로 바꾸고 전부 바꾸면 2번으로 돌아가서 반복 수행

**주의** : 좌표 값을 `(x, y)` 값으로 주는데, 배열의 입력 순서는 `[y][x]` 이므로 값을 넣거나 꺼낼 때 둘의 자리를 바꿔주어야 한다!

### 소스 코드 (Python)

```python

def cabbage_bfs(farm, cabbage, cabbage_count, m, n):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    bug_count = 0

    for _ in range(cabbage_count, 0, -1):
        y, x = cabbage.pop()
        if farm[y][x] == 1:
            farm[y][x] = 0

            bug_count += 1

            next_cabbage = []  # 주변 배추 list
            next_cabbage.append((y, x))

            while next_cabbage:
                nowy, nowx = next_cabbage.pop()
                for i in range(4):
                    temp_y = nowy + dy[i]
                    temp_x = nowx + dx[i]
                    if temp_y >= 0 and temp_y < n and temp_x >= 0 and temp_x < m:
                        if farm[temp_y][temp_x] == 1:
                            farm[temp_y][temp_x] = 0
                            next_cabbage.append((temp_y, temp_x))

    return bug_count


if __name__ == "__main__":

    case = int(input())
    for _ in range(case):

        m, n, k = map(int, input().strip().split())
        # 주의 : m 값이 가로길이 = 열(col)이고 n 값이 세로길이 = 행(row)

        farm = [[0 for _ in range(m)] for _ in range(n)]
        cabbage = []
        cabbage_count = 0

        for i in range(k):
            # strip : 문자열 양쪽 공백을 지우기
            a, b = map(int, input().strip().split())
            # 주의 : a는 가로위치, b는 세로위치. 즉 뒤집어져 있음
            farm[b][a] = 1
            cabbage.append((b, a))
            cabbage_count += 1

        if k == 0:
            print(0)
        else:
            print(cabbage_bfs(farm, cabbage, cabbage_count, m, n))


```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

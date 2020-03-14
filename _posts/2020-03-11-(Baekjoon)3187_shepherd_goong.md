---
layout: post
title: 31. 양치기 꿍
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.3187 : 양치기 꿍](https://www.acmicpc.net/problem/3187){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver II

### 문제 내용

![3187_shepherd_goong](/assets/images/Baekjoon/3187_shepherd_goong.PNG)

### 입력 1

```
6 6
...#..
.##v#.
#v.#.#
#.k#.#
.###.#
...###
```

### 출력 1

```
0 2
```

### 입력 2

```
8 8
.######.
#..k...#
#.####.#
#.#v.#.#
#.#.k#k#
#k.##..#
#.v..v.#
.######.
```

### 출력 2

```
3 1
```

### 입력 3

```
9 12
.###.#####..
#.kk#...#v#.
#..k#.#.#.#.
#..##k#...#.
#.#v#k###.#.
#..#v#....#.
#...v#v####.
.####.#vv.k#
.......####.
```

### 출력 3

```
3 5
```

### 문제 이해

1. 양과 늑대의 수를 세면서 양과 늑대의 위치를 큐에 넣고
2. 큐에서 하나씩 빼서 해당 위치에 대해 v울타리 내에서 bfs를 수행
3. bfs를 수행하며 현재 자리가 v이거나 k이면 그 수를 count
4. bfs가 끝나면 v 수와 k 수를 비교해서 v가 k보다 많거나 같으면 총 양의 수에서 k를 빼고 k가 v보다 많으면 총 늑대의 수에서 v를 빼기
5. 큐가 비면 남은 양과 늑대의 수를 출력

---

### 소스 코드 (Python)

```python


def battle_bfs(arr, wolf_count, sheep_count, where, R, C):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    while where:

        x, y = where.pop()
        now = []

        if arr[x][y] == 'v' or arr[x][y] == 'k':
            now.append((x, y))
        twolf = 0
        tsheep = 0
        while now:
            nowx, nowy = now.pop()
            if arr[nowx][nowy] == 'v':
                twolf += 1
            elif arr[nowx][nowy] == 'k':
                tsheep += 1
            arr[nowx][nowy] = '0'
            for i in range(4):
                tempx = nowx + dx[i]
                tempy = nowy + dy[i]
                if tempx >= 0 and tempx < R and tempy >= 0 and tempy < C:
                    if arr[tempx][tempy] != '#' and arr[tempx][tempy] != '0':
                        now.append((tempx, tempy))
        if twolf >= tsheep:
            sheep_count -= tsheep
        else:
            wolf_count -= twolf
    return sheep_count, wolf_count


if __name__ == "__main__":
    R, C = map(int, input().strip().split())
    arr = [['.' for _ in range(C)] for _ in range(R)]
    wolf_count = 0
    sheep_count = 0
    where = []

    for i in range(R):  # 행 수만큼 반복
        temp = input().strip()  # strip : 문자열 양쪽 공백을 지우기
        for j in range(len(temp)):
            if temp[j] == '#':
                arr[i][j] = '#'
            elif temp[j] == 'v':
                arr[i][j] = 'v'
                wolf_count += 1
                where.append((i, j))
            elif temp[j] == 'k':
                arr[i][j] = 'k'
                sheep_count += 1
                where.append((i, j))

    if (wolf_count + sheep_count) == 0:
        print("%d %d" % (0, 0))
    else:
        sheep_count, wolf_count = battle_bfs(
            arr, wolf_count, sheep_count, where, R, C)
        print("%d %d" % (sheep_count, wolf_count))

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

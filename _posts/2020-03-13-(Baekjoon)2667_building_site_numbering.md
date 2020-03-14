---
layout: post
title: 33. 단지 번호 붙이기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2667 : 단지 번호 붙이기](https://www.acmicpc.net/problem/2667){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용

![2667_building_site_numbering](/assets/images/Baekjoon/2667_building_site_numbering.PNG)

### 입력 1

```
7
0110100
0110101
1110101
0000111
0100000
0111110
0111000
```

### 출력 1

```
3
7
8
9
```

### 문제 이해

[양치기 꿍](<http://takeaimk.tk/baekjoon/2020/03/11/(Baekjoon)3187_shepherd_goong.html>) 문제와 비슷하다.  
길게 설명하지 않고, 단지를 찾기 위해 bfs를 수행할 때마다 수를 세고, 단지 하나마다 돌 때 그 수를 세서 sort 후 출력하면 된다.

---

### 소스 코드 (Python)

```python

def building_bfs(arr, point, n):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    site_total_count = 0
    site_building = []
    first_search = False

    while point:

        x, y = point.pop(0)
        now = []
        first_search = False

        if arr[x][y] == 1:
            now.append((x, y))
            site_total_count += 1
            site_count = 0
            first_search = True
        while now:
            nowx, nowy = now.pop(0)
            if arr[nowx][nowy] == 1:
                site_count += 1
                arr[nowx][nowy] = 0
                for i in range(4):
                    tempx = nowx + dx[i]
                    tempy = nowy + dy[i]
                    if tempx >= 0 and tempx < n and tempy >= 0 and tempy < n:
                        if arr[tempx][tempy] == 1:
                            now.append((tempx, tempy))
        if first_search:
            site_building.append(site_count)
    return site_total_count, site_building


if __name__ == "__main__":
    n = int(input().strip())

    point = []
    arr = [[0 for _ in range(n)]for _ in range(n)]
    for i in range(n):
        temp = input().strip()  # strip : 문자열 양쪽 공백을 지우기
        for j in range(len(temp)):
            if temp[j] == '1':
                arr[i][j] = 1
                point.append((i, j))

    total, site = building_bfs(arr, point, n)
    print(total)
    site.sort()
    for i in range(len(site)):
        print(site[i])

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

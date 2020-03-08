---
layout: post
title: 28. 다리 만들기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2146 : 다리 만들기](https://www.acmicpc.net/problem/2146){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Gold IV

### 문제 내용

![2146_making bridge](/assets/images/Baekjoon/2146_making_bridge_1.PNG)  
![2146_making bridge](/assets/images/Baekjoon/2146_making_bridge_2.PNG)

### 입력 1

```
10
1 1 1 0 0 0 0 1 1 1
1 1 1 1 0 0 0 0 1 1
1 0 1 1 0 0 0 0 1 1
0 0 1 1 1 0 0 0 0 1
0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### 출력 1

```
3
```

### 문제 이해

1. 일단 입력받은 값 중 1의 좌표를 list에 저장
2. list에서 좌표를 하나씩 꺼내 와서 좌표가 가리키는 값이 1이면 섬 갯수 +1과 동시에 bfs를 수행하며 지나온 자리는 -1로 변경. 즉 섬 하나가 전부 -1로 변경됨.
3. 만약 bfs 수행 중 현재 좌표의 상하좌우 값 중 하나라도 0이 있다면 현재 좌표를 현재 계산 중인 섬에 대한 외곽 리스트(edge)에 추가
4. 만약 list에서 꺼내온 좌표 값이 1이 아니면 continue
5. 전부 수행 시 총 섬 갯수와 섬 별로 해안과 닿아있는 1의 좌표를 구할 수 있음 - 여기까지 BFS 사용
6. 섬 하나를 선택 후 해당 섬의 해안 좌표들에 대해 다른 섬들의 해안 좌표와 거리 계산 후 최솟값 저장
7. 이미 계산한 섬은 굳이 다시 계산하지 않아도 되므로 선택되었던 섬을 제외하고 다른 섬 선택 후 6번 반복 후 최솟값 비교 후 갱신 반복
8. n개의 섬 중 n-1번째 섬과 n번째 섬의 최단거리 비교가 끝나면 최종 최솟값을 출력

---

원래 6~8번 과정을 라인 스위핑 알고리즘을 사용해 보고자 했으나 너무 복잡해서 포기하고 전부 비교하는 방법을 사용했다. 처음에는 50%에서 시간초과가 발생하였으나 시간을 줄일 수 있는 부분은 생각나는 대로 줄인 결과 통과할 수 있었다.

---

그 외에도 이번 문제를 통해 파이썬 기법을 많이 익힐 수 있었다.

```python
#2차원 배열을 추가로 생성할 때
edge = []
...
edge.append([])
...
edge[island_count].append((nowx, nowy))

#2차원 배열 0으로 초기화 : row가 행(가로), col이 열(세로)
#arr[row][col]
#출처: https://andrew0409.tistory.com/53 [코인하는 프로그래머]
arr = [[0 for col in range(10)] for row in range(10)]

#리스트 깔끔하게 출력하기
#1차원
print(",".join(map(str, arr_name)))
#2차원
for i in range(len(arr_name)):
    print(",".join(map(str, arr_name[i])))

#입력 빠르게 받게 하기
import sys
...
input = sys.stdin.readline

#key값으로 여러 개가 묶인 튜플 sort하기
#출처: https://andrew0409.tistory.com/66 [코인하는 프로그래머]
tuples = [('kim',30), ('han',10), ('min',20), ('han',70), ('min', 90)]
def age(t):
    return t[1]
def name(t):
    return t[0]
tuples.sort(key=age)
print(tuples)
tuples.sort(key=name)
print(tuples)



```

### 소스 코드 (Python)

```python
def search_edge_bfs(allmap, land, land_count, size):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    edge = []

    island_count = -1

    for _ in range(land_count):
        x, y = land.pop()
        if allmap[x][y] == 1:
            allmap[x][y] = -1

            island_count += 1
            edge.append([])

            next_land = []
            next_land.append((x, y))

            while next_land:
                nowx, nowy = next_land.pop()
                adjacent_have_zero = False
                for i in range(4):
                    temp_x = nowx + dx[i]
                    temp_y = nowy + dy[i]
                    if temp_y >= 0 and temp_y < size and temp_x >= 0 and temp_x < size:
                        if allmap[temp_x][temp_y] == 1:
                            allmap[temp_x][temp_y] = -1
                            next_land.append((temp_x, temp_y))
                        elif allmap[temp_x][temp_y] == 0:
                            adjacent_have_zero = True

                if adjacent_have_zero:
                    edge[island_count].append((nowx, nowy))

    return edge, island_count
if __name__ == "__main__":

    size = int(input())
    allmap = [[0 for _ in range(size)] for _ in range(size)]
    land = []
    land_count = 0
    for i in range(size):
        allmap[i] = list(map(int, input().strip().split()))
        for j in range(len(allmap[i])):
            if allmap[i][j] == 1:
                land.append((i, j))
                land_count += 1

    if land_count == 0:
        print(0)
    else:
        edge, island_count = search_edge_bfs(allmap, land, land_count, size)
        minimum = size*size
        for i in range(island_count):
            for x, y in edge[i]:
                for k in range(i+1, island_count+1):
                    for cx, cy in edge[k]:
                        if abs(x-cx)+abs(y-cy) < minimum:
                            minimum = abs(x-cx)+abs(y-cy)
        print(minimum-1)
```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

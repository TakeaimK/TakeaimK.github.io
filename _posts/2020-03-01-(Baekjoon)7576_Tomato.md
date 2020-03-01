---
layout: post
title: 20. 토마토
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.7576 : 토마토](https://www.acmicpc.net/problem/7576)  

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용
![7576_tomato_1](/assets/images/Baekjoon/7576_tomato_1.PNG)  
![7576_tomato_2](/assets/images/Baekjoon/7576_tomato_2.PNG)   

### 입력 1
```
6 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 1
```
### 출력 1
```
8
```  

### 입력 2
```
6 4
0 -1 0 0 0 0
-1 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 1
```
### 출력 2
```
-1
```  

### 입력 3
```
6 4
1 -1 0 0 0 0
0 -1 0 0 0 0
0 0 0 0 -1 0
0 0 0 0 -1 1
```
### 출력 3
```
6
```  

### 입력 4
```
5 5
-1 1 0 0 0
0 -1 -1 -1 0
0 -1 -1 -1 0
0 -1 -1 -1 0
0 0 0 0 0
```
### 출력 4
```
14
```  

### 입력 5
```
2 2
1 -1
-1 1
```
### 출력 5
```
0
```  


### 문제 이해
다음과 같은 프로세스를 따른다.  
1. 토마토 창고에 있는 모든 토마토는 익어있는가? > 맞다면 0을 출력한다.
2. 토마토 창고에 있는 토마토 중 익은 토마토가 한 개도 없는가? > 맞다면 -1을 출력한다.
3. 익지 않은 토마토 갯수를 세어 놓는다.
4. 익은 토마토 좌표를 큐에 넣는다.
5. count+1을 하고, 큐에서 토마토를 꺼낸다.
6. 큐에서 꺼낸 좌표에 대해 상, 하, 좌, 우 4방향의 토마토 중 익지 않은 토마토가 있다면, 해당 토마토를 익히고 해당 토마토의 상, 하, 좌, 우 토마토 좌표를 큐에 넣는다.
7. 익지 않은 토마토 갯수를 한 개 줄이고, 익지 않은 토마토 갯수가 0이라면 count를 출력한다.
8. 익지 않은 토마토가 남아있음에도 큐에 있는 토마토를 모두 익힌 상태라면 남은 토마토는 익힐 수 없으므로 -1을 출력한다.

---

### 소스 코드 (Python)
```python

def tomato_bfs(arr, ripe_tomatos, ripe_tomato_count, not_ripe_tomatos):
    
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    changed = True
    changed_count = 0

    #초기에 익은 토마토가 하나도 없는 경우
    if ripe_tomato_count == 0:
        return -1
    

    while changed:
        next_tomatos = []   #이번 턴에 익는 토마토를 담는 list
        changed_count += 1  #반복 횟수 count
        changed = False     #만약 이번 턴에 익는 토마토가 없을 경우 이곳으로 돌아오지 않음

        #직전에 익은 토마토에 대해 모두 수행
        while ripe_tomatos:
            tomato = ripe_tomatos.pop()
            x, y = tomato
            for i in range(4):
                temp_x = x + dx[i]
                temp_y = y + dy[i]
                if temp_x >= 0 and temp_x < n and temp_y >= 0 and temp_y < m:
                    value = arr[temp_x][temp_y]
                    # 토마토를 익힌다
                    if value == 0:  #한 개라도 변화하는 토마토가 있으면
                        changed = True  #다음 search를 진행해야 하므로 true
                        not_ripe_tomatos -= 1
    
                        arr[temp_x][temp_y] = 1
                        # 다음에 체크할 토마토들
                        next_tomatos.append((temp_x, temp_y))   #tomatos가 아닌 새로운 공간에 넣고 옮겨주어야 count 가능

                        # 모든 토마토가 익은 경우
                        if not_ripe_tomatos == 0:
                            return changed_count
        '''
        하단 식에 deepcopy를 사용하지 않는 이유
         - next_tomatos를 위에서 []로 초기화하는 것은
           새로운 주소를 부여하여 공간을 할당하는 것이므로
           tomatos에 아무런 영향을 주지 않는다.
        '''
        ripe_tomatos = next_tomatos
    #만약 익지 않은 토마토가 남아있는데 더이상 진행할 수 없는 경우
    return -1
 
if __name__ == "__main__":
    m, n = map(int, input().strip().split())

    arr = []
    tomato = []
    tomato_count = 0
    notyet_count = 0
    empty_count = 0
    for i in range(n):  #열 수만큼 넣어주기
        temp = list(map(int, input().strip().split()))  #strip : 문자열 양쪽 공백을 지우기
        arr.append(temp)
 
    for i in range(n):
        for j in range(m):  
            value = arr[i][j]
            if value == 0:
                notyet_count += 1
            elif value == 1:
                tomato_count += 1
                tomato.append((i, j))
            elif value == -1:
                empty_count += 1
            else:
                print(-1)
                exit(1)
    
    #초기에 익은 토마토 수 + 빈칸 수가 총 칸 수와 같은 경우 
    if (tomato_count + empty_count) == (n*m):
        print(0)
    #토마토 익히기
    else:
        print(tomato_bfs(arr, tomato, tomato_count, notyet_count))

```  

### 소스 코드 (Java)
```java

```  

### 소스 코드 (C++)

```cpp

```


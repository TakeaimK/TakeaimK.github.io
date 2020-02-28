---
layout: post
title: 17. 숨바꼭질
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.1697 : 숨바꼭질](https://www.acmicpc.net/problem/1697)  

### 문제 난이도 (solved.ac 기준) : Silver I

### 문제 내용
![1697_hide_and_seek](/assets/images/Baekjoon/1697_hide_and_seek.PNG)  

### 입력 1
```
5 17
```
### 출력 1
```
4
```  

### 문제 이해
첫 칸을 queue에 넣고 이동을 시작한다.  
매 차례마다 +1, -1, x2로 움직이고 해당 칸을 queue에 넣는다.  
visit 배열에 이동한 번째 수, 즉 tree의 깊이를 넣는다.  
목적지에 도착하면 visit[현재 칸]을 반환한다.  
한줄요약 : bfs 문제이다.

### 소스 코드 (Python)
```python
def bfs(visit, start, end) :
    queue = []

    visit[start]=0
    queue.append(start)

    while queue:
        now = queue.pop(0)
        if now == end:
            return visit[now]
        movp = now+1
        movm = now-1
        movd = now*2
        if movp>=0 and movp<100001:
            if visit[movp] == 0:
                visit[movp] = visit[now]+1
                queue.append(movp)
        if movm>=0 and movm<100001:
            if visit[movm] == 0:
                visit[movm] = visit[now]+1
                queue.append(movm)
        if movd>=0 and movd<100001:
            if visit[movd] == 0:
                visit[movd] = visit[now]+1
                queue.append(movd)
            


if __name__ == "__main__":
    
    ans = 0
    
    subin, sister = map(int, input().split())
    
    visit = [0 for _ in range(100001)]

    ans = bfs(visit, subin, sister)

    print(ans)    


```  

### 소스 코드 (Java)
```java

```  

### 소스 코드 (C++)

```cpp

```


---
layout: post
title: 4.DFS와 BFS
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon_NO.1260_DFS와 BFS](https://www.acmicpc.net/problem/1260){: target="_blank"}  

### 문제 난이도 (solved.ac 기준) : Silver I  

### 문제 내용
![1260_DFS_BFS](/assets/images/Baekjoon/1260_DFS_BFS.PNG)  

### 입력 1
```
4 5 1
1 2
1 3
1 4
2 4
3 4
```
### 출력 1
```
1 2 4 3
1 2 3 4
```  
### 입력 2
```
5 5 3
5 4
5 2
1 2
3 4
3 1
```
### 출력 2
```
3 1 2 5 4
3 1 4 2 5
```  
### 입력 3
```
1000 1 1000
999 1000
```
### 출력 3
```
1000 999
1000 999
```  

### 문제 이해  
- DFS : Depth First Search. 
  1. 루트 노드(시작 노드)에서 시작.
  2. 탐색하지 않은 노드 하나를 선택한 뒤 한 방향으로 계속 파고들어가 진행이 불가능할 때까지 탐색
  3. 진행이 불가능해지면 직전 노드로 돌아와 다른 탐색하지 않은 노드를 찾고 다시 2번을 반복
  3. 모든 노드를 탐색하면 종료  
  - 구현 방법 : 연결리스트(Linked List)를 사용하여 각 노드에 연결된 다른 노드 번호를 연결리스트로 엮어서 기록. Stack을 사용.

- BFS : Breadth-First Search
  1. 루트 노드에서 시작
  2. 현재 노드에서 갈 수 있는 모든 분기를 한 번씩 탐색
  3. n=(2번을 반복한 횟수)로 설정 후 루트 노드에서 거리 n인 노드로 이동
  4. 2,3번을 반복
  5. 역시 모든 노드를 탐색하면 종료
  - 구현 방법 : 연결리스트(Linked List)를 사용하여 각 노드에 연결된 다른 노드 번호를 연결리스트로 엮어서 기록. Queue를 사용.  

  ![DFS_BFS](/assets/images/Baekjoon/DFS_BFS.gif)  

### 소스 코드 (Python - 1)
```Python
from collections import deque

def DFS(graph, root):   #dfs 수행 함수
    visited = []        #방문한 노드를 여기에 담음
    stack = [root]      #스택의 시작은 Root 노드가 담당

    while stack:        #스택일 빌 때까지 수행
        n = stack.pop()     #stack에서 원소 하나를 꺼냄
        if n not in visited:    #stack에서 꺼낸 원소가 visited에 없으면
            visited.append(n)   #visited에 추가
            if n in graph:      #stack에서 꺼낸 원소가 graph에 있다면
                temp = list(set(graph[n]) - set(visited))   #stack에서 꺼낸 원소의 항목을 전부 temp로 옮김
                temp.sort(reverse=True)     #stack에 넣을 때 큰 수부터 넣어야 작은 수에 대해 먼저 탐색함
                stack += temp       #stack에 temp를 전부 넣어줌
    #return " ".join(str(i) for i in visited)    #visited을 문자열로 출력하고 문자열 사이에 " " 삽입
    return visited

def BFS(graph, root):   #bfs 수행 함수
    visited = []        #방문한 노드를 여기에 담음
    queue = deque([root])   #큐의 시작은 Root 노드가 담당

    while queue:        #큐가 빌 때까지 수행
        n = queue.popleft()     #큐에서 원소 하나를 꺼냄
        if n not in visited:    #큐에서 꺼낸 원소가 visited에 없으면
            visited.append(n)   #visited에 추가
            if n in graph:      #큐에서 꺼낸 원소가 그래프에 있다면
                temp = list(set(graph[n]) - set(visited))   #큐에서 꺼낸 원소의 항목을 전부 temp로 옮김
                temp.sort()         #순서대로 정렬
                queue += temp       #큐에 temp를 전부 넣어줌
    #return " ".join(str(i) for i in visited)    #visited을 문자열로 출력하고 문자열 사이에 " " 삽입
    return visited


graph={}    #딕셔너리 형 graph 생성
#Node N, Edge M, Start Node V
N, M, V = map(int, input().split()) #각각의 변수에 입력된 값이 정수로 들어감    #노드 이름이 정수일 때
''' #노드 이름이 문자일 때 
n = input().split()
N = int(n[0])
M = int(n[1])
V = n[2]
'''

for i in range(M):
    n1, n2 = map(int, input().split())  #노드 이름이 정수일 때
    ''' #노드 이름이 문자일 때
    m=input().split()
    n1, n2 = [i for i in m]
    '''
    if n1 not in graph:     #노드가 아직 등록되지 않았다면
        graph[n1] = [n2]    #노드 등록 후 이어진 노드 추가
    elif n2 not in graph[n1]:   #노드는 있지만 이어있지 않다면
        graph[n1].append(n2)    #해당 노드에 이어진 노드 추가

    if n2 not in graph:     #무향 그래프인 경우 양방향 모두 등록
        graph[n2] = [n1]    #위와 동일함
    elif n1 not in graph[n2]:
        graph[n2].append(n1)

#print(DFS(graph, V))
#print(BFS(graph, V))
print(*DFS(graph, V))
print(*BFS(graph, V))

```  

### 소스 코드 (Python - 2)
```Python
N, M, V = map(int, input().split())
matrix = [[0] * (N + 1) for _ in range(N + 1)]
for _ in range(M):
    link = list(map(int, input().split()))
    matrix[link[0]][link[1]] = 1
    matrix[link[1]][link[0]] = 1


def dfs(current_node, row, foot_prints):
    foot_prints += [current_node]
    for search_node in range(len(row[current_node])):
        if row[current_node][search_node] and search_node not in foot_prints:
            foot_prints = dfs(search_node, row, foot_prints)
    return foot_prints


def bfs(start):
    queue = [start]
    foot_prints = [start]
    while queue:
        current_node = queue.pop(0)
        for search_node in range(len(matrix[current_node])):
            if matrix[current_node][search_node] and search_node not in foot_prints:
                foot_prints += [search_node]
                queue += [search_node]
    return foot_prints


print(*dfs(V, matrix, []))
print(*bfs(V))

```  

### 소스 코드 (Java)
```Java
import java.util.*;

public class java_1260 {    // 채점 시 Class 명을 'Main'으로 변경
    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int N = scan.nextInt();     //node num
        int M = scan.nextInt();     //edge num
        int V = scan.nextInt();     //start node
        scan.nextLine();
        
        int[][] matrix = new int[N+1][N+1];
        for(int i=0; i<M; i++){
            int a = scan.nextInt();
            int b = scan.nextInt();
            scan.nextLine();
            matrix[a][b]=1;
            matrix[b][a]=1;
        }
        boolean[] visited = new boolean[N+1];
        Arrays.fill(visited, false);
        Sub cls = new Sub();
        cls.dfs(matrix, visited, V, N);
        Arrays.fill(visited, false);
        System.out.println();
        cls.bfs(matrix, visited, V, N);

    }
    
}

class Sub{
    void dfs(int[][] matrix, boolean[] visited, int now, int N){
        visited[now] = true;
        System.out.print(now + " ");
        for(int i=1; i<=N; i++){
            if(matrix[now][i]!=0 && !visited[i]){
                dfs(matrix, visited, i, N);
            }
        }
    }


    void bfs(int[][] matrix, boolean[] visited, int now, int N){
            
        Queue<Integer> queue = new LinkedList<>();
        queue.add(now); 
        visited[now] = true; //방문한 위치는 알아야하니까, 그것을 체크하기 위해서 visit가 필요. 
        while(!queue.isEmpty()){ 
            int temp = queue.remove(); //첫번째 방문한 위치는 빼주기로 한다. 
            System.out.print(temp+" ");
            for(int k =1; k<=N; k++){ 
                if(matrix[temp][k]==1 && visited[k]==false){ 
                    queue.offer(k);
                    visited[k] = true; //true라면 방문 
                } 
            } 
        }

    }
}
```  

### 소스 코드 (C++)
```C++

```
BFS & DFS 이미지 출처 : [나무위키 - BFS](https://namu.wiki/w/BFS)  

DFS 문제 : 1260, 11724, 10451, 2667, 4963  
BFS 문제 : 2178, 7576, 2146
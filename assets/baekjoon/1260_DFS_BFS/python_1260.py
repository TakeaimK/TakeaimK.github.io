

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



"""
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
"""
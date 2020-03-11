import sys

input = sys.stdin.readline
sys.setrecursionlimit(10**6)


def coupling_elements(N, M, arr, m_list):

    count = 0
    for i in range(1, N+1):
        if arr[i] != True:
            count += 1
            dfs(i)
    return count


def dfs(x):
    visit[x] = True
    for i in m_list[x]:
        if visit[i] != True:
            dfs(i)


if __name__ == "__main__":
    N, M = map(int, input().split())
    visit = [False for _ in range(N+1)]
    m_list = [[] for i in range(N+1)]

    for i in range(M):  # 행 수만큼 반복
        x, y = map(int, input().split())  # strip : 문자열 양쪽 공백을 지우기
        m_list[x].append(y)
        m_list[y].append(x)

    print(coupling_elements(N, M, visit, m_list))

import sys

input = sys.stdin.readline


def area_measurement_bfs(arr, squre, M, N):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    total_count = 0
    area = []
    first_search = False

    while squre:

        x, y = squre.pop(0)
        now = []
        first_search = False

        if arr[x][y] == 1:
            now.append((x, y))
            total_count += 1
            now_count = 0
            first_search = True
        while now:
            nowx, nowy = now.pop(0)
            if arr[nowx][nowy] == 1:
                now_count += 1
                arr[nowx][nowy] = 0
                for i in range(4):
                    tempx = nowx + dx[i]
                    tempy = nowy + dy[i]
                    if tempx >= 0 and tempx < M and tempy >= 0 and tempy < N:
                        if arr[tempx][tempy] == 1:
                            now.append((tempx, tempy))
        if first_search:
            area.append(now_count)
    return total_count, area


if __name__ == "__main__":
    M, N, K = map(int, input().strip().split())

    arr = [[1 for _ in range(N)]for _ in range(M)]
    squre = []

    for _ in range(K):
        sx, sy, ex, ey = map(int, input().strip().split())
        for i in range(sy, ey):
            for j in range(sx, ex):
                arr[i][j] = 0

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                squre.append((i, j))
    count, ans = area_measurement_bfs(arr, squre, M, N)
    print(count)
    ans.sort()
    print(" ".join(map(str, ans)))

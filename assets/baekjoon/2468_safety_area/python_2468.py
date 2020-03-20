import sys
import copy

input = sys.stdin.readline


def safety_area_bfs(arr, N, flow):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    search = []
    tarr = copy.deepcopy(arr)
    for i in range(N):
        for j in range(N):
            if tarr[i][j] <= flow:
                tarr[i][j] = 0
            else:
                search.append((i, j))

    total_count = 0
    first_search = False

    while search:

        x, y = search.pop(0)
        now = []
        first_search = False

        if tarr[x][y] != 0:
            now.append((x, y))
            total_count += 1
            # now_count = 0
            # first_search = True
        while now:
            nowx, nowy = now.pop(0)
            if tarr[nowx][nowy] != 0:
                # now_count += 1
                tarr[nowx][nowy] = 0
                for i in range(4):
                    tempx = nowx + dx[i]
                    tempy = nowy + dy[i]
                    if tempx >= 0 and tempx < N and tempy >= 0 and tempy < N:
                        if tarr[tempx][tempy] != 0:
                            now.append((tempx, tempy))
        # if first_search:
        #     area.append(now_count)
    return total_count


if __name__ == "__main__":
    N = int(input())

    arr = [[1 for _ in range(N)]for _ in range(N)]
    top = 0
    ans = 1

    for i in range(N):
        temp = (list(map(int, input().strip().split())))
        arr[i] = temp
        top = max(max(temp), top)

    for i in range(1, top):
        safety = safety_area_bfs(arr, N, i)
        ans = max(safety, ans)
    print(ans)

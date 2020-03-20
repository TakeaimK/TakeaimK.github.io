import sys
import copy

input = sys.stdin.readline


def find_path_bfs(arr, N, node):

    search = []
    tnode = []
    ret = [0 for _ in range(N)]
    visit = [False for _ in range(N)]

    for i in range(N):
        if node[i] == 1:
            search.append(i)

    # total_count = 0
    # first_search = False

    while search:
        x = search.pop(0)
        visit[x] = True
        now = []
        # first_search = False
        now.append(x)
        while now:
            nowx = now.pop(0)
            tnode = arr[nowx]
            visit[nowx] = True
            for i in range(N):
                if tnode[i] == 1 and visit[i] == False:
                    now.append((i))
        # if first_search:
        #     area.append(now_count)
    for i in range(N):
        if visit[i] == True:
            ret[i] = 1
    return ret


if __name__ == "__main__":
    N = int(input())

    arr = [[0 for _ in range(N)]for _ in range(N)]
    ans = [[0 for _ in range(N)]for _ in range(N)]

    for i in range(N):
        temp = (list(map(int, input().strip().split())))
        arr[i] = temp

    # for i in range(N):
    #     for j in range(N):
    #         if arr[i][j] == 1:
    #             arr[j][i] = 1

    for i in range(N):
        ans[i] = find_path_bfs(arr, N, arr[i])
    for i in range(len(ans)):
        print(" ".join(map(str, ans[i])))

def bfs(arr, visit, row, col) :
    queue = []
    queue.append((0,0))
    visit[0][0] = 1

    dx = [0,0,1,-1]
    dy = [1,-1,0,0]

    while queue:
        x, y = queue.pop(0)
        if x == row-1 and y == col-1:
            return visit[x][y]
        for i in range(4):
            movx = x + dx[i]
            movy = y + dy[i]
            if movx>=0 and movx<row and movy>=0 and movy<col:
                if visit[movx][movy] == 0 and arr[movx][movy] == 1:
                    visit[movx][movy] = visit[x][y]+1
                    queue.append((movx, movy))


if __name__ == "__main__":
    
    ans = 0
    
    row, col = map(int, input().split())
    
    arr = [[0 for _ in range(col)] for _ in range(row)]
    visit = [[0 for _ in range(col)] for _ in range(row)]
    tstr = ""

    for i in range(row):
        tstr = input()
        for j in range(col):
            arr[i][j] = int(tstr[j])

    ans = bfs(arr, visit, row, col)

    print(ans)    


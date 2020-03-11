
def battle_bfs(arr, wolf_count, sheep_count, where, R, C):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    while where:

        x, y = where.pop()
        now = []

        if arr[x][y] == 'v' or arr[x][y] == 'k':
            now.append((x, y))
        twolf = 0
        tsheep = 0
        while now:
            nowx, nowy = now.pop()
            if arr[nowx][nowy] == 'v':
                twolf += 1
            elif arr[nowx][nowy] == 'k':
                tsheep += 1
            arr[nowx][nowy] = '0'
            for i in range(4):
                tempx = nowx + dx[i]
                tempy = nowy + dy[i]
                if tempx >= 0 and tempx < R and tempy >= 0 and tempy < C:
                    if arr[tempx][tempy] != '#' and arr[tempx][tempy] != '0':
                        now.append((tempx, tempy))
        if twolf >= tsheep:
            sheep_count -= tsheep
        else:
            wolf_count -= twolf
    return sheep_count, wolf_count


if __name__ == "__main__":
    R, C = map(int, input().strip().split())
    arr = [['.' for _ in range(C)] for _ in range(R)]
    wolf_count = 0
    sheep_count = 0
    where = []

    for i in range(R):  # 행 수만큼 반복
        temp = input().strip()  # strip : 문자열 양쪽 공백을 지우기
        for j in range(len(temp)):
            if temp[j] == '#':
                arr[i][j] = '#'
            elif temp[j] == 'v':
                arr[i][j] = 'v'
                wolf_count += 1
                where.append((i, j))
            elif temp[j] == 'k':
                arr[i][j] = 'k'
                sheep_count += 1
                where.append((i, j))

    if (wolf_count + sheep_count) == 0:
        print("%d %d" % (0, 0))
    else:
        sheep_count, wolf_count = battle_bfs(
            arr, wolf_count, sheep_count, where, R, C)
        print("%d %d" % (sheep_count, wolf_count))

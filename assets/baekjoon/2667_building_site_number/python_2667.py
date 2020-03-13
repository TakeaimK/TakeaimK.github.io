
def building_bfs(arr, point, n):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    site_total_count = 0
    site_building = []
    first_search = False

    while point:

        x, y = point.pop(0)
        now = []
        first_search = False

        if arr[x][y] == 1:
            now.append((x, y))
            site_total_count += 1
            site_count = 0
            first_search = True
        while now:
            nowx, nowy = now.pop(0)
            if arr[nowx][nowy] == 1:
                site_count += 1
                arr[nowx][nowy] = 0
                for i in range(4):
                    tempx = nowx + dx[i]
                    tempy = nowy + dy[i]
                    if tempx >= 0 and tempx < n and tempy >= 0 and tempy < n:
                        if arr[tempx][tempy] == 1:
                            now.append((tempx, tempy))
        if first_search:
            site_building.append(site_count)
    return site_total_count, site_building


if __name__ == "__main__":
    n = int(input().strip())

    point = []
    arr = [[0 for _ in range(n)]for _ in range(n)]
    for i in range(n):
        temp = input().strip()  # strip : 문자열 양쪽 공백을 지우기
        for j in range(len(temp)):
            if temp[j] == '1':
                arr[i][j] = 1
                point.append((i, j))

    total, site = building_bfs(arr, point, n)
    print(total)
    site.sort()
    for i in range(len(site)):
        print(site[i])

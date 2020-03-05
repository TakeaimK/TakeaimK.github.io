
def cabbage_bfs(farm, cabbage, cabbage_count, m, n):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    bug_count = 0

    for _ in range(cabbage_count, 0, -1):
        y, x = cabbage.pop()
        if farm[y][x] == 1:
            farm[y][x] = 0

            bug_count += 1

            next_cabbage = []  # 주변 배추 list
            next_cabbage.append((y, x))

            while next_cabbage:
                nowy, nowx = next_cabbage.pop()
                for i in range(4):
                    temp_y = nowy + dy[i]
                    temp_x = nowx + dx[i]
                    if temp_y >= 0 and temp_y < n and temp_x >= 0 and temp_x < m:
                        if farm[temp_y][temp_x] == 1:
                            farm[temp_y][temp_x] = 0
                            next_cabbage.append((temp_y, temp_x))

    return bug_count


if __name__ == "__main__":

    case = int(input())
    for _ in range(case):

        m, n, k = map(int, input().strip().split())
        # 주의 : m 값이 가로길이 = 열(col)이고 n 값이 세로길이 = 행(row)

        farm = [[0 for _ in range(m)] for _ in range(n)]
        cabbage = []
        cabbage_count = 0

        for i in range(k):
            # strip : 문자열 양쪽 공백을 지우기
            a, b = map(int, input().strip().split())
            # 주의 : a는 가로위치, b는 세로위치. 즉 뒤집어져 있음
            farm[b][a] = 1
            cabbage.append((b, a))
            cabbage_count += 1

        if k == 0:
            print(0)
        else:
            print(cabbage_bfs(farm, cabbage, cabbage_count, m, n))

# import sys
# import copy
# import queue

# input = sys.stdin.readline


def search_edge_bfs(allmap, land, land_count, size):

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    edge = []

    island_count = -1

    for _ in range(land_count):
        x, y = land.pop()
        if allmap[x][y] == 1:
            allmap[x][y] = -1

            island_count += 1
            edge.append([])

            next_land = []
            next_land.append((x, y))

            while next_land:
                nowx, nowy = next_land.pop()
                adjacent_have_zero = False
                for i in range(4):
                    temp_x = nowx + dx[i]
                    temp_y = nowy + dy[i]
                    if temp_y >= 0 and temp_y < size and temp_x >= 0 and temp_x < size:
                        if allmap[temp_x][temp_y] == 1:
                            allmap[temp_x][temp_y] = -1
                            next_land.append((temp_x, temp_y))
                        elif allmap[temp_x][temp_y] == 0:
                            adjacent_have_zero = True

                if adjacent_have_zero:
                    edge[island_count].append((nowx, nowy))

    return edge, island_count


# def min_bfs(edge, island_count, size):
#     area = [[0 for _ in range(size)] for _ in range(size)]
#     dx = [-1, 1, 0, 0]
#     dy = [0, 0, -1, 1]
#     minimum = size*size
#     maximum = size*size
#     # print(edge)

#     for i in range(island_count):
#         area = [[0 for _ in range(size)] for _ in range(size)]
#         for k in range(i+1, island_count+1):
#             for tx, ty in edge[k]:
#                 area[tx][ty] = maximum
#                 #print("도착해야 하는 좌표 : " + str(tx) + " " + str(ty))

#         for x, y in edge[i]:

#             debug = False

#             tarea = copy.deepcopy(area)
#             tarea[x][y] = 0
#             point = queue.Queue()
#             temp = 0
#             point.put((x, y))

#             # if x == 7 and y == 4:
#             #     debug = True
#             if debug:
#                 print("출발위치 : " + str(x) + " " + str(y))
#             while point and temp == 0:
#                 nowx, nowy = point.get()

#                 for q in range(4):
#                     temp_x = nowx + dx[q]
#                     temp_y = nowy + dy[q]
#                     if temp_y >= 0 and temp_y < size and temp_x >= 0 and temp_x < size:

#                         if tarea[temp_x][temp_y] == maximum:
#                             temp = tarea[nowx][nowy]
#                             if debug:
#                                 print("도착위치 : " + str(nowx) + " " + str(nowy))
#                                 print("이동거리 : " + str(temp))
#                             break
#                         elif tarea[temp_x][temp_y] == 0:
#                             tarea[temp_x][temp_y] = tarea[nowx][nowy] + 1
#                             point.put((temp_x, temp_y))
#                         else:
#                             continue
#                         if debug:
#                             print("현재 탐색위치 : " + str(temp_x) + " " + str(temp_y))
#                             print("현재 탐색값 : " + str(tarea[temp_x][temp_y]))
#             if minimum > temp:
#                 minimum = temp
#         if debug:
#             print("최솟값 : " + str(minimum))
#     return minimum

    #             for k in range(i+1, island_count+1):
    #                 for l in range(len(edge[k])):
    #                     cx, cy = edge[k][l]
    #                     if abs(x-cx)+abs(y-cy) < min:
    #                         min = abs(x-cx)+abs(y-cy)


# def findx(t):
#     return t[0]


if __name__ == "__main__":

    size = int(input())
    allmap = [[0 for _ in range(size)] for _ in range(size)]
    land = []
    land_count = 0
    for i in range(size):
        allmap[i] = list(map(int, input().strip().split()))
        for j in range(len(allmap[i])):
            if allmap[i][j] == 1:
                land.append((i, j))
                land_count += 1

    if land_count == 0:
        print(0)
    else:
        edge, island_count = search_edge_bfs(allmap, land, land_count, size)
        minimum = size*size

    # if land_count != 0:
    #     for i in range(island_count+1):
    #         edge[i].sort(key=findx)
    #         # print(edge[i])
    #         for j in range(len(edge[i])):
    #             x, y = edge[i][j]
    #             for k in range(i+1, island_count+1):
    #                 for l in range(len(edge[k])):
    #                     cx, cy = edge[k][l]
    #                     if abs(x-cx)+abs(y-cy) < min:
    #                         min = abs(x-cx)+abs(y-cy)
    # print(min-1)
    # print(min_bfs(edge, island_count, size))

        for i in range(island_count):
            for x, y in edge[i]:
                for k in range(i+1, island_count+1):
                    for cx, cy in edge[k]:
                        if abs(x-cx)+abs(y-cy) < minimum:
                            minimum = abs(x-cx)+abs(y-cy)
        print(minimum-1)

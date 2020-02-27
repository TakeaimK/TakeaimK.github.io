import sys
import copy
sys.setrecursionlimit(10**6)

def maze_runner(arr, row, col, nr, nc) :
    a = 10001
    b = 10001
    c = 10001
    d = 10001
    min = 10001

    if(nr == row and col == nc):  
        return 1
    else:
        tarr = copy.deepcopy(arr)
        tarr[nr][nc] = 0
        if(arr[nr+1][nc] == 1):
            a = maze_runner(tarr, row, col, nr+1, nc)
            if(min>a):
                min = a
        if(arr[nr-1][nc] == 1):
            b = maze_runner(tarr, row, col, nr-1, nc)
            if(min>b):
                min = b
        if(arr[nr][nc+1] == 1):
            c = maze_runner(tarr, row, col, nr, nc+1)
            if(min>c):
                min = c
        if(arr[nr][nc-1] == 1):
            d = maze_runner(tarr, row, col, nr, nc-1)
            if(min>d):
                min = d
        return min+1


if __name__ == "__main__":
    
    ans = 0
    
    row, col = map(int, input().split())
    
    arr = [[0 for _ in range(col+2)] for _ in range(row+2)]
    tstr = ""

    for i in range(1,row+1):
        tstr = input()
        for j in range(1,col+1):
            arr[i][j] = int(tstr[j-1])

    ans = maze_runner(arr, row, col, 1, 1)

    print(ans)    


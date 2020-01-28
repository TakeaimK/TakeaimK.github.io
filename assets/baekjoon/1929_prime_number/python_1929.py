import math

start, end = map(int, input().split())


for i in range(start, end+1):
    for j in range(2, round(math.sqrt(i))+1):
        #print("i = %d" %i)
        if(i%j == 0):
            break
    else:
        if(i>1):
            print(i)
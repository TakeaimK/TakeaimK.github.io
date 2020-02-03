arr = []
min = int(1000001)
max = int(-1000001)

num = int(input())

#temp = input()
#arr = temp.split()
arr = list(map(int, input().split()))   #arr 안의 항목을 정수로 변환하여 list로 재생성

for i in range(num):
    if(arr[i]>max):
        max = arr[i]
    if(arr[i]<min):
        min = arr[i]

print("%d %d" %(min, max))



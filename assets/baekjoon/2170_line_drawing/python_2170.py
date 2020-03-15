import sys

input = sys.stdin.readline

if __name__ == "__main__":

    num = int(input())

    arr = []

    for _ in range(num):
        a, b = map(int, input().split())
        arr.append((a, b))
    arr.sort(key=lambda ar: ar[0])

    ans = 0
    start, end = arr[0]

    for i in range(1, len(arr)):
        if end < arr[i][0]:
            ans += (end - start)
            start, end = arr[i]
        else:
            if end < arr[i][1]:
                end = arr[i][1]
    ans += (end-start)
    print(ans)

# import sys

# input = sys.stdin.readline

# if __name__ == "__main__":

#     num = int(input())

#     arr = []

#     for _ in range(num):
#         a, b = map(int, input().split())
#         can_append = True
#         for i in range(len(arr)):
#             x, y = arr[i]
#             # print(x)
#             # print(y)
#             if x < a and a < y and y < b:
#                 arr[i] = (x, b)
#                 can_append = False
#                 #print("case 1 : " + str(arr[i]))
#             elif a < x and x < b and b < y:
#                 arr[i] = (a, y)
#                 can_append = False
#                 #print("case 2 : "+str(arr[i]))
#             elif a < x and y < b:
#                 arr[i] = (a, b)
#                 can_append = False
#                 #print("case 3 : "+str(arr[i]))
#             elif x < a and b < y or x == a and y > b or x < a and y == b:
#                 can_append = False
#                 #print("case 4 : "+str(arr[i]))
#         if can_append:
#             arr.append((a, b))
#             #print("case 5 : " + str(arr[len(arr)-1]))
#     ans = 0
#     for i in range(len(arr)):
#         # print(arr[i])
#         x, y = arr[i]
#         ans += (y-x)
#     print(ans)

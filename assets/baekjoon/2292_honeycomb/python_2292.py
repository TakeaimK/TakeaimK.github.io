if __name__ == "__main__":
    num = int(input())
    temp = 1
    i = 1
    k = 1
    while True:
        if num <= temp:
            print(i)
            break
        else:
            temp = k*6+1
            i += 1
            k += i


# if __name__ == "__main__":
#     num = int(input())

#     ans = num//6 + 1
#     if num % 6 == 0 or num % 6 == 1:
#         ans += 1
#     print(ans)

if __name__ == "__main__":

    lst = list(map(int, input().strip().split()))
    lst[2] = lst[2]-lst[0]
    lst[3] = lst[3]-lst[1]

    print(min(lst))

if __name__ == "__main__":

    n, row, col = map(int, input().split())

    # if (row + col) % 2 == 0:
    #     for i in range(n):
    #         if i % 2 == 0:
    #             print("v." * (n // 2) + 'v' * (n % 2))
    #         else:
    #             print(".v" * (n // 2) + '.' * (n % 2))

    # else:
    #     for i in range(n):
    #         if i % 2 == 1:
    #             print("v." * (n // 2) + 'v' * (n % 2))
    #         else:
    #             print(".v" * (n // 2) + '.' * (n % 2))

    if row % 2 == 0:
        if col % 2 == 0:
            for i in range(1, n+1):
                for j in range(1, n+1):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                    else:
                        if j % 2 == 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                print("")
        else:
            for i in range(1, n+1):
                for j in range(1, n+1):
                    if i % 2 == 0:
                        if j % 2 != 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                    else:
                        if j % 2 != 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                print("")

    else:
        if col % 2 == 0:
            for i in range(n):
                for j in range(n):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                    else:
                        if j % 2 == 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                print("")
        else:
            for i in range(n):
                for j in range(n):
                    if i % 2 == 0:
                        if j % 2 != 0:
                            print(".", end='')
                        else:
                            print("v", end='')
                    else:
                        if j % 2 != 0:
                            print("v", end='')
                        else:
                            print(".", end='')
                print("")

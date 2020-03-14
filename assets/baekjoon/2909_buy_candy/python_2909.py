if __name__ == "__main__":

    price, zero = map(int, input().strip().split())

    zero = int(str(1) + str(0)*zero)
    temp = price % zero
    if temp >= zero//2:
        print((price//zero) * zero + 1*zero)
    else:
        print((price//zero) * zero)

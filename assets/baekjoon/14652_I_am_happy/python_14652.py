if __name__ == "__main__":

    N, M, K = map(int, input().strip().split())

    print("%d %d" % (K//M, K % M))

if __name__ == "__main__":

    Ai = int(input())
    A = list(map(int, input().strip().split()))

    Mi = int(input())
    M = list(map(int, input().strip().split()))

    answer = [0 for _ in range(Mi)]
    A.sort()

    for i in range(Mi):
        low = 0
        high = Ai-1
        temp = M[i]
        while True:
            pointer = (low+high)//2

            if temp == A[pointer]:
                answer[i] = 1
                break
            elif temp > A[pointer]:
                low = pointer+1
            elif temp < A[pointer]:
                high = pointer-1
            if low > high:
                break
    for t in answer:
        print(t)

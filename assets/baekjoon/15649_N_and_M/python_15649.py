from itertools import chain, permutations  # 순열
# 조합 라이브러리 사용 시 combinations 사용

if __name__ == "__main__":

    N, M = map(int, input().strip().split())

    arr = [i for i in range(1, N+1)]

    # 모든 부분적 순열 집합을 모두 구한다
    powerset = list(chain.from_iterable(permutations(arr, r)
                                        for r in range(1, len(arr)+1)))

    for i in range(len(powerset)):
        if len(powerset[i]) == M:
            for j in range(len(powerset[i])):
                print(powerset[i][j], end='')
                print(" ", end='')
            print()

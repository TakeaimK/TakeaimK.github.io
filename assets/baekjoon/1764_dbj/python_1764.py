import sys
input = sys.stdin.readline

if __name__ == "__main__":
    n, m = map(int, input().split())
    d = set()
    count = 0
    ans = []
    for _ in range(n):
        t = input().strip()
        d.add(t)
    for _ in range(m):
        t = input().strip()
        if t in d:
            count += 1
            ans.append(t)
    
    
    ans.sort()
    print(count)
    for t in ans:
        print(t)


# N, M = map(int, input().split())
# a = set()
# b = set()
# for i in range(N):
#     a.add(input())
# for i in range(M):
#     b.add(input())
# l = list(a&b)
# print(len(l))
# for e in sorted(l):
#     print(e)
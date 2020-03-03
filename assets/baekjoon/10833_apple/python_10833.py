if __name__ == "__main__":
    
    run = int(input())
    ans = 0

    for _ in range(run):
        a, b = map(int, input().split())
        ans += b%a

    print(ans)



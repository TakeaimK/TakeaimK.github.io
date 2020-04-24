import sys
input = sys.stdin.readline

if __name__ == "__main__":
    num = str(input().strip())
    visit = [True for _ in range(10)]
    ans = ""
    exc = False
    if int(num) > 9876543210:
        print(9876543210)
        exit()
    for now in range(len(num)):
        if visit[int(num[now])]:
            visit[int(num[now])] = False
            ans += str(num[now])
        else:
            temp = now
            rng = len(num)-len(ans)-1
            exc = True
            break
    
    #visit[num[temp]] = False
    if exc:
        again = 1
        while True:
            low = int(num[temp])-again
            high = int(num[temp])+again
            if low >= 0 and visit[low]:
                visit[low] = False
                ans += str(low)
                #temp = low
                if rng > 0:
                    for i in range(9, -1, -1):
                        if visit[i]:
                            visit[i] = False
                            ans = ans + str(i)
                            rng -= 1
                            if rng<=0:
                                break;
                break
            elif high < 10 and visit[high]:
                visit[high] = False
                ans += str(high)
                #temp = high
                if rng > 0:
                    for i in range(10):
                        if visit[i]:
                            visit[i] = False
                            ans = ans + str(i)
                            rng -= 1
                            if rng<=0:
                                break;
                break
            again+=1
        # if temp < 5 and rng > 0:
        #     for i in range(9, -1, -1):
        #         if visit[i]:
        #             visit[i] = False
        #             ans = ans + str(i)
        #             rng -= 1
        #             if rng<=0:
        #                 break;
        # elif temp >= 5 and rng > 0:
        #     for i in range(10):
        #         if visit[i]:
        #             visit[i] = False
        #             ans = ans + str(i)
        #             rng -= 1
        #             if rng<=0:
        #                 break;
    print(ans.strip())
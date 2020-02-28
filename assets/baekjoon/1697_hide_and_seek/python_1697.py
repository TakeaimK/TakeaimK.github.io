def bfs(visit, start, end) :
    queue = []

    visit[start]=0
    queue.append(start)

    while queue:
        now = queue.pop(0)
        if now == end:
            return visit[now]
        movp = now+1
        movm = now-1
        movd = now*2
        if movp>=0 and movp<100001:
            if visit[movp] == 0:
                visit[movp] = visit[now]+1
                queue.append(movp)
        if movm>=0 and movm<100001:
            if visit[movm] == 0:
                visit[movm] = visit[now]+1
                queue.append(movm)
        if movd>=0 and movd<100001:
            if visit[movd] == 0:
                visit[movd] = visit[now]+1
                queue.append(movd)
            


if __name__ == "__main__":
    
    ans = 0
    
    subin, sister = map(int, input().split())
    
    visit = [0 for _ in range(100001)]

    ans = bfs(visit, subin, sister)

    print(ans)    


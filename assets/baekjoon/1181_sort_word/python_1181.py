if __name__ == "__main__":

    rng = int(input())
    words = []
    maxlen = 0

    for _ in range(rng):
        string = input()


        words.append((len(string),string))

        if len(string) > maxlen:
            maxlen = len(string)

    words.sort(key=lambda wd: wd[0])
    words.append((51, ""))

    i=0
    while(i < rng):
        temp = []
        while(True):
            if words[i][0] == words[i+1][0]:
                temp.append(words[i][1])
                i+=1
            else:
                temp.append(words[i][1])
                break
        tset = set(temp)
        temp = list(tset)
        temp.sort()
        for p in temp:
            print(p)
        i+=1

    

import copy

def date():
    man = input()
    woman_num = int(input())
    arr = []
    n_arr = []
    

    tLOVE = [0, 0, 0, 0]

    for i in range(len(man)):
            if man[i] == 'L':
                tLOVE[0] += 1
            elif man[i] == 'O':
                tLOVE[1] += 1
            elif man[i] == 'V':
                tLOVE[2] += 1
            elif man[i] == 'E':
                tLOVE[3] += 1
            else:
                continue

    for i in range(woman_num):
        name = input()
        n_arr.append(name)

        LOVE = copy.deepcopy(tLOVE)
        
        for j in range(len(name)):
            if name[j] == 'L':
                LOVE[0] += 1
            elif name[j] == 'O':
                LOVE[1] += 1
            elif name[j] == 'V':
                LOVE[2] += 1
            elif name[j] == 'E':
                LOVE[3] += 1
            else:
                continue
        value = 0
        value = ((LOVE[0] + LOVE[1]) * (LOVE[0] + LOVE[2]) * (LOVE[0] + LOVE[3]) * (LOVE[1] + LOVE[2]) * (LOVE[1] + LOVE[3]) * (LOVE[2] + LOVE[3])) % 100
        arr.append(value)

    choose = 0
    date_list = []
    for i in range(woman_num):
        choose = max(choose, arr[i])

    for i in range(woman_num):
        if arr[i] == choose:
            date_list.append(n_arr[i])

    date_list.sort()
    return date_list[0]

if __name__ == "__main__":

    answer = ""

    answer = date()

    print(answer)
    

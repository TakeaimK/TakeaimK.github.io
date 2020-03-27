import sys
input = sys.stdin.readline

if __name__ == "__main__":
    
    while True:
        temp = input().strip()
        if temp == "#":
            exit()
        temp = temp.lower()
        find = temp[0]
        string = temp[1:].strip()

        count = 0

        for i in range(len(string)):
            if find == string[i]:
                count += 1
        print(find + " " + str(count))

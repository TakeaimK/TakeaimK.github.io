if __name__ == "__main__":
    
    newstr = ""

    many = input()
    for _ in range(int(many)):
        temp = input().split()
        repeat = temp[0]
        string = temp[1]

        for i in range(len(string)):    #string의 길이만큼
            for _ in range(int(repeat)):    #문자열의 i번째 문자를 repeat번 만큼 이어붙인다
                newstr+=string[i]      #문자열에도 연산자로 이어붙이기가 가능

        print(newstr)
        newstr=""

        




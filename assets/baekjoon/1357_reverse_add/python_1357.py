def reverse(string):
    temp = ""
    for i in range(len(string)):
        temp += string[len(string)-i-1]
    return temp


if __name__ == "__main__":
    num1, num2 = map(str, input().strip().split())
    rev1 = int(reverse(num1))
    rev2 = int(reverse(num2))
    print(int(reverse(str(rev1+rev2))))

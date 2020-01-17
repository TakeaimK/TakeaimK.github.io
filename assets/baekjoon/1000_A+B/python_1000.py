str = input()       #공백 포함 입력 -> string
num = str.split()      #공백 단위로 문자열 분리
print(int(num[0]) + int(num[1]))    #문자열을 정수형으로 바꿔서 덧셈 후 출력
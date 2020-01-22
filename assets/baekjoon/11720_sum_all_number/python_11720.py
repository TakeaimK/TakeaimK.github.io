
i = int(input())
string = input()       #일단 문자열로 입력받음
num = 0

for j in range(i):      #0부터 i-1까지
    num += int(string[j])   #문자열 한 자리씩 더하기

print(num)  #결과 출력
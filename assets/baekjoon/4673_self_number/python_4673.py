def non_self_number(num):
    total=num
    if(num>=10000):  #수가 10000이 넘으면
        total+=(num//10000)  #만의 자릿수를 total에 더함
        num=(num%10000)     #num에서 만의 자릿수 제거
    if(num>=1000):  #수가 1000이 넘으면
        total+=(num//1000)  #천의 자릿수를 total에 더함
        num=(num%1000)     #num에서 천의 자릿수 제거
    if(num>=100):  #수가 100이 넘으면
        total+=(num//100)  #백의 자릿수를 total에 더함
        num=(num%100)     #num에서 백의 자릿수 제거    
    if(num>=10):  #수가 10이 넘으면
        total+=(num//10)  #십의 자릿수를 total에 더함
        num=(num%10)     #num에서 십의 자릿수 제거
    total+=num  #일의 자릿수를 total에 더함
    return total

arr=[0 for _ in range(100000)]

for i in range(1, 10001):
    arr[non_self_number(i)]=1
    if(arr[i]==0):
        print(i)
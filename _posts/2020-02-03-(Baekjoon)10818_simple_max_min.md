---
layout: post
title: 9. 최댓값과 최솟값
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.10818 : 최솟값과 최댓값](https://www.acmicpc.net/problem/2739){: target="_blank"}  

### 문제 난이도 (solved.ac 기준) : Bronze III  

### 문제 내용
![10818_최댓값과_최솟값](/assets/images/Baekjoon/10818_simple_max_min.PNG)  

### 입력 1
```
5
20 10 35 30 7
```
### 출력 1
```
7 35
```  

### 문제 이해
배열에 숫자들을 넣고, 순차적으로 탐색하며 최솟값과 최댓값을 찾는다.  
다만 주의사항은 초기 최솟값은 가능한 가장 큰 값보다 1 큰 1,000,001을 넣는다.  
최댓값은 가능한 가장 작은 값보다 더 작은 -1,000,001을 넣는다.  

### 소스 코드 (Python)
```python
arr = []
min = int(1000001)
max = int(-1000001)

num = int(input())

#temp = input()
#arr = temp.split()
arr = list(map(int, input().split()))   #arr 안의 항목을 정수로 변환하여 list로 재생성

for i in range(num):
    if(arr[i]>max):
        max = arr[i]
    if(arr[i]<min):
        min = arr[i]

print("%d %d" %(min, max))


```  


### 소스 코드 (Java)
```java
import java.util.Scanner;

public class java_10818{    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        int num = scan.nextInt();
        scan.nextLine();
        int max = -1000001;
        int min = 1000001;
        int temp;

        for(int i=0; i<num; i++){
            temp = scan.nextInt();
            if(temp>max){
                max = temp;
            }
            if(temp<min){
                min = temp;
            }
        }
        System.out.println(min + " " + max);

    }
    
}
```  

### 소스 코드 (C++)

```cpp

```


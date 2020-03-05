---
layout: post
title: 5. 소수 구하기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon_NO.1929_Prime_Number](https://www.acmicpc.net/problem/1929){: target="_blank"}  

### 문제 난이도 (solved.ac 기준) : Silver I  

### 문제 내용
![1260_DFS_BFS](/assets/images/Baekjoon/1929_prime_number.PNG)  

### 입력 1
```
3 16
```
### 출력 1
```
3
5
7
11
13
```  

### 문제 이해  
- 소수 (Prime number)
  - N이라는 자연수를 표현할 때, 1 x N의 형태로만 표현할 수 있는 수
  - 반대 개념으로 합성수(N이라는 자연수 표현 시 A x B로 표현이 가능)가 있다.
  
#### 1. 간단한 방법 (Python, Java, C++)  
A x B = N이 나오는 합성수를 걸러내면 된다.  
즉, N을 A로 나누었을 때 B로 몫이 떨어진다는 소리이고, 나머지가 나오지 않는다는 것이다.  
예를 들어, 14가 소수인지 판별하는 방법은, 14를 13부터 2까지 차례대로 나누어 나머지가 나오는지 확인한다. 
이 때 7로 나누면 나머지가 0이므로 14는 합성수이다.  

위 방법을 사용하면 쉽게 소수를 구할 수 있지만, 조금 더 머리를 써 보도록 하자.
35는 합성수이다. 그런데 소수임을 판별하기 위해서 34부터 나누기 시작하면 7에 도달해야 합성수임을 알 수 있다.  
5 x 7 = 35이고, 7 x 5 = 35이다. 같은 수가 좌우가 바뀌어도 동일한 곱셈의 성질을 이용한다.  
즉, 작은 수 부분만 탐색해서 시간을 단축시킬 수 있다. 그러면 이 작은 수 부분을 어떻게 걸러낼 것인가?  
간단한 방법으로는 수를 반으로 나누어 나머지를 확인하는 방법이 있다. 하지만 곱셈에서는 더 좋은 방법이 있다.  
바로 **제곱근(Root)**를 활용하는 것이다. N을 곱셈으로 표현할 수 있는 가장 작은 두 수는 N의 제곱근이다.  
__따라서 N의 제곱근에서 소숫점 아래 부분을 잘라낸 수부터 2까지 나누어 나머지가 나오지 않는 수__ 가 소수이다.  

#### 2. 에라토스테네스의 체 사용 (C++)
하지만 위 방법은 이중 for문을 사용하므로 시간이 매우 오래 걸리게 된다. (시간복잡도 O(n^2))  
여기서 에라토스테네스의 체를 사용하면 for문을 최소화할 수 있다.
2부터 N까지의 배수는 모두 합성수이다. 따라서 배수를 모두 제거한 후 출력하는 방식을 사용한다.

### 소스 코드 (Python)
```python
import math

start, end = map(int, input().split())


for i in range(start, end+1):
    for j in range(2, round(math.sqrt(i))+1):
        #print("i = %d" %i)
        if(i%j == 0):
            break
    else:
        if(i>1):
            print(i)

```  


### 소스 코드 (Java)
```java
import java.util.Scanner;
import java.math.*;

public class java_1929 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
        int start = scan.nextInt();
        int end = scan.nextInt();
        boolean set;

        for(int i=start; i<=end; i++){
            set=true;
            for (int j=2; j<=Math.floor(Math.sqrt(i)); j++){
                if(i%j == 0){
                    set=false;
                    break;
                }
            }
            if(set && i>1){
                System.out.println(i);
            }
        }  
    }
}
```  

### 소스 코드 (C++)
- 다음 코드 부분은 속도가 느린 C++의 cin, cout을 C의 printf, scanf로 변경시켜 준다. 시간초과 발생 시 사용해 보자.  
단, c의 getchar() 등과 동시에 사용할 수 없다.
```cpp
ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
```

- 간단한 방법

```cpp
#include <iostream>
#include <cmath>
 
using namespace std;
 
int main() {

    ios_base :: sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int start, end;
    cin >> start >> end;
    bool set;
 
    for (int i = start; i <= end; i++) {
        
        set=true;
        
        for (int j = 2 ; j <= floor(sqrt(i)); j++){
            if(i%j == 0){
                set=false;
                break;
            }
        }
        
        if(set && i>1){
            cout<<i<<'\n';
        }
        
    }
 
    return 0;
}

```
- 에라토스테네스의 체

```cpp
#include <iostream>
#include <vector>
 
using namespace std;
 
int main() {

 
    int start, end;
    cin >> start >> end;
    vector<bool> isPrime(end + 1, true);
 
    isPrime[0] = false;
    isPrime[1] = false;
    for (int i = 2; i <= end; i++) {
        if (isPrime[i]) {
           
            for (int j = 2 * i; j <= end; j += i)
                isPrime[j] = false;
        }
    }
 
    for(int i = start; i <= end; i++)
        if(isPrime[i])
            cout << i << endl;
 
    return 0;
}
```

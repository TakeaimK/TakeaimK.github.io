---
layout: post
title: 16. 곱셈
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2588 : 곱셈](https://www.acmicpc.net/problem/2588)  

### 문제 난이도 (solved.ac 기준) : Bronze IV

### 문제 내용
![2588_multiple](/assets/images/Baekjoon/2588_multiple.PNG)  

### 입력 1
```
472
385
```
### 출력 1
```
2360
3776
1416
181720
```  

### 문제 이해
곱셈의 원리를 알고 있다면 간단하게 풀 수 있다.
각 언어에 따라 조금씩 접근 방법이 다르지만, 어렵지 않다.

### 소스 코드 (Python)
```python
if __name__ == "__main__":
    
    num1 = input()
    num2 = input()

    num1 = int(num1)
    print(num1*int(num2[2]))
    print(num1*int(num2[1]))
    print(num1*int(num2[0]))
    print(num1*int(num2))


```  

### 소스 코드 (Java)
```java
import java.util.Scanner;

public class java_2588 {    // 채점 시 Class 명을 'Main'으로 변경

    public static void main(String[] args) {
        
        Scanner scan = new Scanner(System.in);
       
        int num1 = scan.nextInt();
        String num2 = scan.next();

        System.out.println(num1*Character.getNumericValue(num2.charAt(2)));
        System.out.println(num1*Character.getNumericValue(num2.charAt(1)));
        System.out.println(num1*Character.getNumericValue(num2.charAt(0)));
        System.out.println(num1*Integer.parseInt(num2));
       
    }
    
}
```  

### 소스 코드 (C++)

```cpp


```


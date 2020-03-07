---
layout: post
title: 27. 뒤집힌 덧셈
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.1357 : 뒤집힌 덧셈](https://www.acmicpc.net/problem/1357){: target="_blank"}  

### 문제 난이도 (solved.ac 기준) : Bronze I

### 문제 내용
![1357_reverse_add](/assets/images/Baekjoon/1357_reverse_add.PNG)  

### 입력 1
```
123 100
```
### 출력 1
```
223
```  

### 문제 이해
정수를 문자열로 받아 뒤집어준 뒤 다시 정수로 변환하여 더하고  
문자열로 바꿔서 뒤집어 준 다음 다시 정수로 바꾸어 출력한다.

### 소스 코드 (Python)
```python
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

```

### 소스 코드 (Java)
```java

```  

### 소스 코드 (C++)

```cpp

```


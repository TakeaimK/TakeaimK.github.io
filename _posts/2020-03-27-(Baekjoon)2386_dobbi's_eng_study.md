---
layout: post
title: 40. 도비의 영어 공부
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2386 : 도비의 영어 공부](https://www.acmicpc.net/problem/2386){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze II

### 문제 내용

![2386_dobby's_eng_study](/assets/images/Baekjoon/2386_dobby's_eng_study.PNG)

### 입력 1

```
g Programming Contest
n New Zealand
x This is quite a simple problem.
#
```

### 출력 1

```
g 2
n 2
x 0
```

### 문제 이해

이 문제를 풀면서 마주칠 수 있는 난관을 정리해 보았다.  
1. 대문자로 된 경우는 어떻게 찾지? -> lower로 전부 소문자화 시키기
2. 맨 첫 글자와 뒤쪽 문장은 띄어쓰기로 구분하기 난감한데... -> 문자열 슬라이싱

### 소스 코드 (Python)

```python
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

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

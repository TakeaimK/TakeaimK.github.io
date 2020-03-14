---
layout: post
title: 28. 벌집
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.14652 : 벌집](https://www.acmicpc.net/problem/2292){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze II

### 문제 내용

![2292_honeycomb](/assets/images/Baekjoon/2292_honeycomb.PNG)

### 입력 1

```
13
```

### 출력 1

```
3
```

### 문제 이해

무언가 어렵게 꼬아 놓았지만 생각보다 단순하다.  
위 그림에서 1에서 출발하여 한 바퀴를 돈다고 가정했을 때, 4시 방향 값이 해당 바퀴 값 중 가장 큰 값이다. 즉, 1, 17, 19, 37, ...인 것이다.  
또한 해당 바퀴 안에 있는 곳은 가는 거리가 모두 동일할 것이다.  
무언가 느낌이 오지 않는가?  
1칸 : 1 = 6 _ 0 + 1  
2칸 : 7 = 6 _ (0+1=1) + 1  
3칸 : 19 = 6 _ (0+1+2=3) + 1  
4칸 : 37 = 6 _ (0+1+2+3=6) + 1  
5칸 : 61 = 6 \* (0+1+2+3+4=10) + 1
...  
즉, 6에 곱해지는 값은 누적합이다.
위 방법을 코드로 구현해 보았다.

### 소스 코드 (Python)

```python
if __name__ == "__main__":
    num = int(input())
    temp = 1
    i = 1
    k = 1
    while True:
        if num <= temp:
            print(i)
            break
        else:
            temp = k*6+1
            i += 1
            k += i
```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

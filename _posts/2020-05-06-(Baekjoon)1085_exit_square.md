---
layout: post
title: 44. 직사각형 탈출
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.1085 : 직사각형 탈출](https://www.acmicpc.net/problem/1085){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze III

### 문제 내용

![1085_exit_square](/assets/images/Baekjoon/1085_exit_square.PNG)

### 입력 1

```
6 2 10 3
```

### 출력 1

```
1
```

### 문제 이해

가장 가까운 사각형의 외곽을 알아내는 방법을 필요로 하는 문제이다.  
의외로 간단한데, x값과 y값, (w-x)값과 (h-y)값 중 가장 작은 값이 정답이다.

### 소스 코드 (Python) - 나의 풀이

```python
if __name__ == "__main__":

    lst = list(map(int, input().strip().split()))
    lst[2] = lst[2]-lst[0]
    lst[3] = lst[3]-lst[1]

    print(min(lst))

```

### 소스 코드 (Go)

```go
package main

import(
    "fmt"
)

func main(){

    var arr [4]int

    for i:=0; i<4; i++{
        fmt.Scan(&arr[i])
    }


    arr[2] = arr[2]-arr[0]
    arr[3] = arr[3]-arr[1]

    ans := arr[0]

    for i:=1; i<4; i++{
        if arr[i]<ans{
            ans = arr[i]
        }
    }
    fmt.Println(ans)
}
```

---
layout: post
title: 36. 선 긋기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.2170 : 선 긋기](https://www.acmicpc.net/problem/2170){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Gold V

### 문제 내용

![2170_line_drawing](/assets/images/Baekjoon/2170_line_drawing.PNG)

### 입력 1

```
4
1 3
2 5
3 5
6 7
```

### 출력 1

```
5
```

### 문제 이해

문제가 꽤나 빡세다. 많은 시행착오 끝에 해결하였다.  
처음에는 입력을 받으면 리스트에 넣고, 매번 입력을 받을 때마다 리스트에서 비교하여 포함 관계인지, 한쪽만 더 긴지, 아니면 떨어져 있는지 확인하여 해당 경우에 맞게 넣는 방법을 사용하였다. 그러나 매우 비효율적인 과정에, 앞뒤로 비교하는 과정에서 시간을 많이 잡아먹기도 하고, 테스트 케이스가 많아질수록 시간이 매우 오래 걸리게 되었다. 따라서 시간초과 발생 후 다른 방법을 찾아야만 했다.  
두 번째로 해결한 방법은, 일단 입력을 받은 뒤 시작 지점을 기준으로 정렬하였다. 가장 앞에 있는 출발지점을 기준으로 해당 선의 시작부분과 끝 부분을 start, end로 정의 후 두 번째 선분에 대해 비교하였다. 비교 과정은 다음과 같다.

1. 현재 있는 선분의 end보다 다음 선분의 start가 더 크다면 기존 선분의 길이를 ans에 누적 저장 후 현재의 start, end 값을 다음 선분의 start, end 값으로 교체
2. 위 경우에 해당하지 않는다 -> 현재 있는 선분의 end보다 다음 선분의 end가 더 크다면 현재의 end값을 다음 선분의 end값으로 교체
3. 마지막 선분까지 수행 후, 마지막으로 남은 start와 end 값을 ans에 누적 저장
4. ans 값 출력

특히 Python으로 풀 때, `input = sys.stdin.readline`을 사용하지 않으면 시간초과가 발생한다. 입력 함수에 대한 시간 비교는 다음 글을 참조하면 좋다.

> [입력 속도 비교 - Beakjoon](https://www.acmicpc.net/blog/view/56)

또한 리스트의 첫 번째 튜플의 값으로 정렬하기 위해 다음과 같은 람다 함수를 사용하였다.

```python
arr.sort(key=lambda ar: ar[0])
```

---

### 소스 코드 (Python)

```python
import sys

input = sys.stdin.readline

if __name__ == "__main__":

    num = int(input())

    arr = []

    for _ in range(num):
        a, b = map(int, input().split())
        arr.append((a, b))
    arr.sort(key=lambda ar: ar[0])

    ans = 0
    start, end = arr[0]

    for i in range(1, len(arr)):
        if end < arr[i][0]:
            ans += (end - start)
            start, end = arr[i]
        else:
            if end < arr[i][1]:
                end = arr[i][1]
    ans += (end-start)
    print(ans)


```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

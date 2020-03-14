---
layout: post
title: 35. 수 찾기
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.1920 : 수 찾기](https://www.acmicpc.net/problem/1920){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver IV

### 문제 내용

![1920_find_number](/assets/images/Baekjoon/1920_find_number.PNG)

### 입력 1

```
5
4 1 5 2 3
5
1 3 7 9 5
```

### 출력 1

```
1
1
0
0
1
```

### 문제 이해

매우 간단한 방법으로는, 앞에서부터 찾는 값과 같은지 비교하는 방법이 있다. 즉, 매 수가 나올 때마다 앞부터 차례대로 돌아가며 찾는 방법인데, 이게 10만개의 수를 10만번 탐색할 수 있다.(10^6 \* 10^6 = 10^12, 약 1조) 예제는 단순히 5개의 수 중에서 5개를 찾지만, 훨씬 더 많은 경우의 수를 돌려본다는 이야기이다. for문을 사용하여 순차 탐색을 사용하면 단순하지만 시간 초과가 발생할 확률이 매우 높다.  
시간 초과가 발생할 경우 그 시간을 줄이는 방법에는 하드웨어 자원을 추가로 투입하여(메모리 사용 증가) 해결하는 방법과 알고리즘을 개선하여 해결하는 방법이 있다. 당연히 여기서는 알고리즘으로 개선하는 방법을 사용한다.  
원리는 간단하다. 해당 수가 있는지 없는지만 알면 되기에, 주어지는 정수의 순서는 중요치 않다. 그 말은 오름차순으로 정렬한 뒤 수가 있을 수 있는 범위를 좁혀나가며 찾는 방법이 더 빠를 확률이 높다는 것이다.  
여기서 등장한 방법이 이분 탐색으로, 원리는 다음과 같다.

1. 수가 들어있는 배열 A를 sort한다.
2. 찾아야 하는 수를 x라 가정하면, A 배열의 가운데 있는 수인지 비교한다.
3. 만약 x가 A의 가운데 있는 수보다 크다면, A 배열의 처음부터 가운데 사이에는 x가 존재하지 않으므로, 탐색 범위를 가운데부터 끝까지로 조정 후 조정된 범위에서 가운데 있는 수인지 비교한다. 반대로 x가 A의 가운데 있는 수보다 작다면, 탐색 범위를 처음부터 가운데까지로 조정하고 조정된 범위에서 가운데 있는 수인지 비교한다. x가 A의 가운데 있는 수와 동일하다면, x가 있음을 표시한다.
4. x를 찾을 때까지 3을 반복 작업하며, 만약 찾지 못하는 경우, 즉 범위가 사라진다면 x는 없음을 표시한다.

위 작업을 반복하면 훨씬 빠르게 답을 얻을 수 있다.

---

### 소스 코드 (Python)

```python
if __name__ == "__main__":

    Ai = int(input())
    A = list(map(int, input().strip().split()))

    Mi = int(input())
    M = list(map(int, input().strip().split()))

    answer = [0 for _ in range(Mi)]
    A.sort()

    for i in range(Mi):
        low = 0
        high = Ai-1
        temp = M[i]
        while True:
            pointer = (low+high)//2

            if temp == A[pointer]:
                answer[i] = 1
                break
            elif temp > A[pointer]:
                low = pointer+1
            elif temp < A[pointer]:
                high = pointer-1
            if low > high:
                break
    for t in answer:
        print(t)


```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

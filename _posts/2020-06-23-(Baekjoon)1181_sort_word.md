---
layout: post
title: 45. 단어 정렬
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.1181 : 단어 정렬](https://www.acmicpc.net/problem/1181){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Silver V

### 문제 내용

![1181_sort_word](/assets/images/Baekjoon/1181_sort_word.PNG)

### 입력 1

```
13
but
i
wont
hesitate
no
more
no
more
it
cannot
wait
im
yours
```

### 출력 1

```
i
im
it
no
but
more
wait
wont
yours
cannot
hesitate
```

### 문제 이해

### 소스 코드 (Python)

```python
if __name__ == "__main__":

    rng = int(input())
    words = []
    maxlen = 0

    for _ in range(rng):
        string = input()


        words.append((len(string),string))

        if len(string) > maxlen:
            maxlen = len(string)

    words.sort(key=lambda wd: wd[0])
    words.append((51, ""))

    i=0
    while(i < rng):
        temp = []
        while(True):
            if words[i][0] == words[i+1][0]:
                temp.append(words[i][1])
                i+=1
            else:
                temp.append(words[i][1])
                break
        tset = set(temp)
        temp = list(tset)
        temp.sort()
        for p in temp:
            print(p)
        i+=1

    

```

### 소스 코드 (Golang)

```go
package main

import (
	"fmt"
	"sort"
)

type ByLength []string

func (s ByLength) Len() int {
	return len(s)
}
func (s ByLength) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}
func (s ByLength) Less(i, j int) bool {
	return len(s[i]) < len(s[j])
}

func main() {

	var rng int
	fmt.Scan(&rng)

	arr := make([]string, rng)

	gg := true
	var tmps string
	for i := 0; i < rng; i++ {
		gg = true
		fmt.Scan(&tmps)
		for _, s := range arr {
			if tmps == s {
				gg = false
				break
			}
		}
		if gg {
			arr[i] = tmps
		}

	}
	//fmt.Println(arr)

	sort.Sort(ByLength(arr))

	for _, s := range arr {
		fmt.Printf("%s\n", s)
	}
}

```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

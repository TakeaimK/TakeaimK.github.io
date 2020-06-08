---
layout: post
title: (Go) Generator
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

괴제 전체 source code는 아래 링크에 있습니다.

> [Github Source Code - Make Generator using Golang Concurrency](https://github.com/TakeaimK/Study_Goroutine_Channel){: target="\_blank"}

---

# 제너레이터 기본형

```go
package main

import "fmt"

func IntegerGenerator(n int) <-chan int {
	next := 0
	intStream := make(chan int)

	go func() {
		defer close(intStream)
		for next < n {
			next++
			intStream <- next
		}
	}()
	return intStream
}

func main() {
	for i := range IntegerGenerator(10) {
		fmt.Println(i)
	}
}
```

main에서 제너레이터 호출 > 제너레이터에서 채널 생성 > 고루틴 생성과 동시에 defer로 채널 close > 제너레이터는 채널을 반환 > 고루틴에서 원하는 값 생성 후 채널로 전송 > main의 for문에서 값을 받아 출력 > 채널이 close되면 자동으로 for문도 종료

---

# ex1. 주어진 배열의 n개의 모든 조합을 생성하는 제너레이터 작성

## 제너레이터 부분

- string 슬라이스 채널 생성 후 `Combinations()`에 채널과 슬라이스, 조합 별 요소 수를 넘긴다.

```go
func CombinationGenerator(fruit []string, n int) <-chan []string {
	combStream := make(chan []string)

	go func() {
		defer close(combStream)
		Combinations(combStream, fruit, n)
	}()
	return combStream
}

func main() {
	for i := range CombinationGenerator([]string{"사과", "배", "복숭아", "포도", "귤"}, 2) {
		fmt.Println(i)
	}
}

```

## Combination()

- 조합을 만드는 코드는 [original source](https://github.com/mxschmitt/golang-combinations/blob/master/combinations.go#L32)를 응용하였다.
- 하나의 조합이 만들어질 때마다 채널로 전송한다.
- 만약 0개의 요소 수를 요청받으면, 빈 문자열 슬라이스를 채널로 보내고 종료한다.

```go
func Combinations(ch chan []string, set []string, n int) {
	length := uint(len(set))

	if n == 0{
		ch <- []string{}
		return
	}

	if n > len(set) {
		n = len(set)
	}

	// Go through all possible combinations of objects
	// from 1 (only first object in subset) to 2^length (all objects in subset)
	for subsetBits := 1; subsetBits < (1 << length); subsetBits++ {
		if n > 0 && bits.OnesCount(uint(subsetBits)) != n {
			continue
		}

		var subset []string

		for object := uint(0); object < length; object++ {
			// checks if object is contained in subset
			// by checking if bit 'object' is set in subsetBits
			if (subsetBits>>object)&1 == 1 {
				// add object to subset
				subset = append(subset, set[object])
			}
		}
		// send subset to channel
		ch <- subset
	}
}
```

---

# ex2. n bit 이진 그레이 코드를 순서대로 출력하는 제너레이터 작성

## 제너레이터 부분

- main에서 n bit Gray Code를 요청받으면, `printGray()`에서 그레이 코드로 변환 후 `printCode()`에서 값을 받아 채널로 전송한다.

```go
func GrayBinaryGenerator(n int) <-chan []int {
	GrayCodeStream := make(chan []int)

	go func() {
		defer close(GrayCodeStream)

		arr := make([]int, n)
		printGray(arr, n, 0, 0, GrayCodeStream)

	}()
	return GrayCodeStream
}

func main() {
	for i := range GrayBinaryGenerator(3) {
		fmt.Println(i)
	}
}
```

## printGray(), printCode()

- 재귀를 사용한다.

```go
func printCode(arr []int, len int, ch chan []int) {

	snd := make([]int, len)
	for i := 0; i < len; i++ {
		snd[i] = arr[i]
	}
	ch <- snd
}

func printGray(arr []int, n, index, reverse int, ch chan []int) {
	if index == n {
		printCode(arr, n, ch)
		return
	}

	arr[index] = reverse
	printGray(arr, n, index+1, 0, ch)
	arr[index] = 1 - reverse
	printGray(arr, n, index+1, 1, ch)
}

```

---

# ex3. n개의 원반을 이동하는 하노이 탑 제너레이터 작성

## 제너레이터 부분

- 2의 크기를 가지는 string 배열 채널 생성 후 `Move()`에 채널과 원판 갯수, 기둥을 넘긴다.

```go
func HanoiGenerator(n int, from, to, by string) <-chan [2]string {
	HanoiStream := make(chan [2]string)

	go func() {
		defer close(HanoiStream)

		Move(HanoiStream, n, from, to, by)

	}()
	return HanoiStream
}

func main() {
	for move := range HanoiGenerator(5, "A", "B", "C") {
		fmt.Println(move[0], " ->", move[1])
	}
}
```

## Move()

- 재귀를 이용한 하노이 탑 옮기기 방법을 사용하였다. (Discovery Go - 47p 참조)

```go
func Move(ch chan [2]string, n int, from, to, by string) {
	if n <= 0 {
		return
	}
	Move(ch, n-1, from, by, to)
	ans := [2]string{from, to}
	ch <- ans
	Move(ch, n-1, by, to, from)
}
```

---

# ex4. 주어진 파일에서 모든 단어를 나온 순서대로 출력하는 제너레이터 작성

## 제너레이터 부분

- 파일 Open 이후 `ReadString(' ')`으로 공백을 기준하여 읽어온 후, 채널로 전송한다.

```go
func AllwordsGenerator(filename string) <-chan string {
	WordStream := make(chan string)

	go func() {
		defer close(WordStream)

		fo, err := os.Open(filename)
		if err != nil {
			panic(err)
		}
		defer fo.Close()

		reader := bufio.NewReader(fo)

		for {
			line, err := reader.ReadString(' ')

			if err == io.EOF {
				WordStream <- line
				break
			}

			if err != nil {
				break
			}
			WordStream <- line
		}
		//data, _ := ioutil.ReadFile(filename)
		//temp := string(data)
		//ans := strings.Split(temp, " ")
		//
		//for _, word := range ans {
		//	WordStream <- word
		//}

	}()
	return WordStream
}

func main() {
	for w := range AllwordsGenerator("./test.txt") {
		fmt.Println(w)
	}
}

```

---

읽어주셔서 감사합니다!

---
layout: post
title: (Go) 6. 동시성
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

> [Github Source Code - Gotour](https://github.com/TakeaimK/Gotour){: target="\_blank"}

# A tour of Go

A tour of Go는 Golang의 특징을 공부할 수 있는 학습 사이트이다.
한국어 사이트와 영어 사이트가 있으며, 내용은 거의 동일하다.

> [gotour - 한국어](https://go-tour-kr.appspot.com/#63){: target="\_blank"}  
> [gotour - 영어](https://tour.golang.org/concurrency/1){: target="\_blank"}

---

## 고루틴 (Goroutines)

```
_고루틴_은 Go 런타임에 의해 관리되는 경량 쓰레드입니다.

go f(x, y, z)
위의 코드는 새로운 고루틴을 시작시킵니다.

f(x, y, z)
현재의 고루틴에서 f , x , y , z 가 평가(evaluation)되고, 새로운 고루틴에서 f 가 수행(execution)됩니다.

고루틴은 동일한 주소 공간에서 실행되므로, 공유되는 자원으로의 접근은 반드시 동기화 되어야 합니다. [[http://golang.org/pkg/sync/][sync]] 패키지가 이를 위해 유용한 기본 기능을 제공합니다. Go 에서는 그외에도 다양한 기본 기능을 제공하니 크게 필요치 않을 테지만요. (다음 슬라이드를 보세요.)
```

```go
package main

import (
    "fmt"
    "time"
)

func say(s string) {
    for i := 0; i < 5; i++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s)
    }
}

func main() {
    go say("world")
    say("hello")
}


```

<내용 추가>

---

## 채널 (Channels)

```
채널은 채널 연산자 <- 를 이용해 값을 주고 받을 수 있는, 타입이 존재하는 파이프입니다.

ch <- v    // v 를 ch로 보냅니다.
v := <-ch  // ch로부터 값을 받아서
           // v 로 넘깁니다.
(데이터가 화살표 방향에 따라 흐릅니다.)

맵이나 슬라이스처럼, 채널은 사용되기 전에 생성되어야 합니다:

ch := make(chan int)
기본적으로, 송/수신은 상대편이 준비될 때까지 블록됩니다. 이런 특성이 고루틴이 명시적인 락이나 조건 없이도 동기화 될 수 있도록 돕습니다.
```

```go
package main

import "fmt"

func sum(a []int, c chan int) {
    sum := 0
    for _, v := range a {
        sum += v
    }
    c <- sum // send sum to c
}

func main() {
    a := []int{7, 2, 8, -9, 4, 0}

    c := make(chan int)
    go sum(a[:len(a)/2], c)
    go sum(a[len(a)/2:], c)
    x, y := <-c, <-c // receive from c

    fmt.Println(x, y, x+y)
}


```

<내용 추가>

---

```
채널은 _버퍼링_될 수 있습니다. make 에 두번째 인자로 버퍼 용량을 넣음으로써 해당 용량만큼 버퍼링되는 채널을 생성할 수 있습니다:

ch := make(chan int, 100)
버퍼링되는 채널로의 송신은 버퍼가 꽉 찰 때까지 블록됩니다. 수신측은 버퍼가 빌 때 블록됩니다.

예제를 수정해서 버퍼를 넘치게 해보고 어떻게 동작하는지 확인해 보세요.
```

```go
package main

import "fmt"

func main() {
    c := make(chan int, 2)
    c <- 1
    c <- 2
    fmt.Println(<-c)
    fmt.Println(<-c)
}


```

<내용 추가>

---

```
데이터 송신측은 더이상 보낼 값이 없다는 것을 알리기 위해 채널을 close 할 수 있습니다. 수신측은 다음과 같이 수신 코드에 두번째 인자를 줌으로써 채널이 닫혔는지 테스트 할 수 있습니다.

v, ok := <-ch
채널이 이미 닫혔고 더이상 받을 값이 없다면 ok 는 false 가 됩니다.

for i := range c 반복문은 채널이 닫힐 때까지 계속해서 값을 받습니다.

주의: 송신측만 채널을 닫을 수 있습니다. 수신측에선 불가능합니다. 이미 닫힌 채널에 데이터를 보내면 패닉이 일어납니다.

또하나의 주의: 채널은 파일과 다릅니다; 항상 닫을 필요는 없습니다. 채널을 닫는 행위는 오로지 수신측에게 더이상 보낼 값이 없다고 말해야 할때만 행해지면 됩니다. range 루프를 종료시켜야 할 때처럼요.
```

```go
package main

import (
    "fmt"
)

func fibonacci(n int, c chan int) {
    x, y := 0, 1
    for i := 0; i < n; i++ {
        c <- x
        x, y = y, x+y
    }
    close(c)
}

func main() {
    c := make(chan int, 10)
    go fibonacci(cap(c), c)
    for i := range c {
        fmt.Println(i)
    }
}



```

<설명 추가>

---

## 셀릭트 (Select)

```
select 구문은 고루틴이 다수의 통신 동작으로부터 수행 준비를 기다릴 수 있게 합니다.

select 는 case 구문으로 받는 통신 동작들 중 하나가 수행될 수 있을 때까지 수행을 블록합니다. 다수의 채널이 동시에 준비되면 그 중 하나를 무작위로 선택합니다.
```

```go
package main

import "fmt"

func fibonacci(c, quit chan int) {
    x, y := 0, 1
    for {
        select {
        case c <- x:
            x, y = y, x+y
        case <-quit:
            fmt.Println("quit")
            return
        }
    }
}

func main() {
    c := make(chan int)
    quit := make(chan int)
    go func() {
        for i := 0; i < 10; i++ {
            fmt.Println(<-c)
        }
        quit <- 0
    }()
    fibonacci(c, quit)
}

```

<설명 추가>

---

## 에러 (error)

```
select 의 default 케이스는 현재 수행 준비가 완료된 케이스가 없을 때 수행됩니다.

블로킹 없이(비동기적인) 송/수신을 하고자 할 때 default 케이스를 사용하세요.

select {
case i := <-c:
	// i를 사용
default:
	// c로부터의 수신은 블록된 상태
}
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    tick := time.Tick(1e8)
    boom := time.After(5e8)
    for {
        select {
        case <-tick:
            fmt.Println("tick.")
        case <-boom:
            fmt.Println("BOOM!")
            return
        default:
            fmt.Println("    .")
            time.Sleep(5e7)
        }
    }
}

```

<내용 추가>

---

```
노드(leaf)들에 있는 값들의 정렬 순열는 같지만 생김새가 다른 이진트리가 있을 수 있습니다. 예를들어, 다음 그림의 두 이진 트리를 정렬 순열는 1, 1, 2, 3, 5, 8, 13 으로 같습니다.

대부분의 프로그래밍 언어에서 두 이진 트리가 같은 순열인지를 검사하는 함수의 구현은 복잡합니다. 이제 고의 동시성과 채널을 사용한 단순한 방법으로 해결해 봅시다.

이 예제는 다음의 Tree 구조체가 정의된 tree 패키지를 사용합니다.

type Tree struct {
	Left  *Tree
	Value int
	Right *Tree
}

1. Walk 함수를 구현하세요.

2. Walk 함수를 테스트 해 보세요.

함수 `tree.New(k)`는 k , 2k , 3k , ..., 10k 의 값을 가지는, 무작위로 구성된 이진트리를 만들어 냅니다.

채널 ch 를 만들고, 작성한 Walk 함수의 인자로 넣어 줍니다.

go Walk(tree.New(1), ch)
이제 채널에서 10개의 값을 읽어 봅니다. 읽힌 값은 1, 2, 3, ..., 10 이어야 합니다.

3. Walk 함수를 사용해 두 트리 t1 과 t2 이 값은 값들을 가지고 있는지 비교하는 Same 함수를 구현해 보세요.

4. Same 함수를 테스트 해 보세요.

`Same(tree.New(1),`tree.New(1))`의 수행결과는 true, `Same(tree.New(1),`tree.New(2))`의 수행 결과는 false 이어야 합니다.
```

```go
package main

import "code.google.com/p/go-tour/tree"

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan int)

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool

func main() {
}

```

<코드 및 내용 추가>

---

```
이 연습에서는 고의 동시성 기능을 사용해 웹 크롤러를 병렬화 해 볼 것입니다.

Crawl 함수를 고쳐서, 같은 URL을 두번 가져오는 중복을 피하면서 URL들을 병렬로 패치하게 고쳐보세요.
```

```go
package main

import (
    "fmt"
)

type Fetcher interface {
    // Fetch returns the body of URL and
    // a slice of URLs found on that page.
    Fetch(url string) (body string, urls []string, err error)
}

// Crawl uses fetcher to recursively crawl
// pages starting with url, to a maximum of depth.
func Crawl(url string, depth int, fetcher Fetcher) {
    // TODO: Fetch URLs in parallel.
    // TODO: Don't fetch the same URL twice.
    // This implementation doesn't do either:
    if depth <= 0 {
        return
    }
    body, urls, err := fetcher.Fetch(url)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Printf("found: %s %q\n", url, body)
    for _, u := range urls {
        Crawl(u, depth-1, fetcher)
    }
    return
}

func main() {
    Crawl("http://golang.org/", 4, fetcher)
}

// fakeFetcher is Fetcher that returns canned results.
type fakeFetcher map[string]*fakeResult

type fakeResult struct {
    body string
    urls []string
}

func (f *fakeFetcher) Fetch(url string) (string, []string, error) {
    if res, ok := (*f)[url]; ok {
        return res.body, res.urls, nil
    }
    return "", nil, fmt.Errorf("not found: %s", url)
}

// fetcher is a populated fakeFetcher.
var fetcher = &fakeFetcher{
    "http://golang.org/": &fakeResult{
        "The Go Programming Language",
        []string{
            "http://golang.org/pkg/",
            "http://golang.org/cmd/",
        },
    },
    "http://golang.org/pkg/": &fakeResult{
        "Packages",
        []string{
            "http://golang.org/",
            "http://golang.org/cmd/",
            "http://golang.org/pkg/fmt/",
            "http://golang.org/pkg/os/",
        },
    },
    "http://golang.org/pkg/fmt/": &fakeResult{
        "Package fmt",
        []string{
            "http://golang.org/",
            "http://golang.org/pkg/",
        },
    },
    "http://golang.org/pkg/os/": &fakeResult{
        "Package os",
        []string{
            "http://golang.org/",
            "http://golang.org/pkg/",
        },
    },
}

```

<코드 및 내용 수정>

---

```
우선 Go 문서 사이트에서 시작하는 것이 좋습니다. 여기에서 레퍼런스, 튜토리얼, 비디오 등의 자료를 볼 수 있습니다.

고 코드를 구성하기와 고로 작업하는 방법을 배우려면, 이 스크린캐스트를 보거나, 고 코드 작성 방법를 읽어 보세요.

표준 라이브러리에 대한 도움이 필요하면, 패키지 레퍼런스를 살펴보세요. 고 언어 자체에 대해서는 언어 스펙이 도움이 되며, 아마 꽤 쉽게 스펙문서를 읽을 수 있음에 놀라게 될 것입니다.

더 나아가 고의 동시성(concurrency) 모델을 살펴보려면 코드워크, 통신으로 메모리 공유하기를 보세요.

코드워크, First Class Functions in Go에서는 고의 함수 타입에 관련된 흥미로운 관점을 제공합니다.

공식 블로그, Go 에는 유익한 기사들이 많이 있습니다.

공식 사이트 golang.org를 방문해 더 살펴보세요.

번역: 한국 Go 언어 커뮤니티(GDG Korea Golang)
```

---

읽어주셔서 감사합니다!

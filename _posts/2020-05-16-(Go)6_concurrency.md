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

고루틴은 동일한 주소 공간에서 실행되므로, 공유되는 자원으로의 접근은 반드시 동기화 되어야 합니다. sync 패키지가 이를 위해 유용한 기본 기능을 제공합니다. Go 에서는 그외에도 다양한 기본 기능을 제공하니 크게 필요치 않을 테지만요. (다음 슬라이드를 보세요.)
```

[Golang - sync](http://golang.org/pkg/sync/)

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

쓰레드의 실행은 OS가 우선순위를 결정하여 실행하고, 따라서 hello와 world가 실행할 때마다 순서가 일정하지 않고 뒤죽박죽되어 나온다.

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

import (
    "fmt"
    //"time"
    )

func sum(a []int, c chan int) {
    sum := 0
    for _, v := range a {
        sum += v
    }
    c <- sum // send sum to c
}

func main() {
    a := []int{7, 2, 8, -9, 4, 0}

    c := make(chan int, 3)
    go sum(a[:len(a)/2], c)	//17
    go sum(a[len(a)/2:], c)	//-5
    go sum(a[:], c)			//12
    //time.Sleep(100 * time.Millisecond)
    x, y, z := <-c, <-c, <-c// receive from c

    fmt.Println(x, y, z)
}

```

여기서 의아했던 것은, PC에서 돌려봤을 때 결과가 매번 달라졌다. `17 -5 12`, `12 17 -5`, `12 -5 17` 등 ~~경우의 수 구하기~~ 여러 가지 케이스가 발생했다. 곰곰히 생각을 해 보았는데, 바로 뒤에 나올 버퍼를 적용하지 않고 3개의 응답을 기다리는 게 되는데, 하나의 채널을 공유하며 채널이 사용 중일 때는 나머지 스레드가 기다린다. 이때, 고루틴이 실행되어 채널에 들어가는 순서가 항상 일정하지 않다. 스레드는 순차지향적이지 않고 병렬적으로 실행되는 개념이기 때문이다. 따라서 어떤 것이 먼저 x에 들아갈지 명확히 단정지을 수 없다.

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
    fmt.Println("Warning!") //출력됨
    c <- 3	//fatal error: all goroutines are asleep - deadlock!
    fmt.Println(<-c)
    fmt.Println(<-c)
}


```

만약 추가로 `c <-3`을 넣는다면, 무서운 오류를 볼 수 있다. 전 예제와 달리 하나의 함수에서 채널 버퍼를 초과하여 채널에 데이터를 욱여넣으면, 모든 고루틴을 종료시켜 버린다. 그리고, deadlock(교착 상태) 메세지를 뿜는다! 버퍼에서 데이터를 빼내야 새로운 데이터를 넣는데, 빼는 과정이 없고 추가로 넣으려고 시도만 한다. 혹시 후에 고루틴으로 빼내주는 경우를 만들어 테스트를 진행해 보았다.

```go
package main

import "fmt"

func out(ch chan int){
    fmt.Println(<-ch)
}

func main() {
    c := make(chan int, 2)
    c <- 1
    c <- 2
    fmt.Println("Warning!")

    c <- 3	//fatal error: all goroutines are asleep - deadlock!

    go out(c)   //진행되지 않음

    fmt.Println(<-c)
    fmt.Println(<-c)
    fmt.Println("Warning!")    //출력 안 됨
}

```

만약, 고루틴이 c를 채널에 추가하기 전에 넣는다면 정상적으로 실행됨을 알 수 있다.

```go
package main

import "fmt"

func out(ch chan int){
    fmt.Println(<-ch)   //1
}

func main() {
    c := make(chan int, 2)
    c <- 1
    c <- 2
    fmt.Println("Warning!")

    go out(c)
    c <- 3

    fmt.Println(<-c)    //2
    fmt.Println(<-c)    //3
    fmt.Println("Warning!")
}

```

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

오직 수신 측에서만 종료시킬 수 있다는 점을 주의해야 한다!

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

여러 개의 채널에서 값이 들어올 때, select 구문으로 채널에서 데이터가 들어올 때 작업할 수 있다. 마치 switch와 유사한 형태이다.

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

import (
    "code.google.com/p/go-tour/tree"
	"fmt"
)

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan int) {
	inorder(t, ch)
	close(ch)
}

func inorder(t *tree.Tree, ch chan int) {
	value := t.Value

	if t.Left != nil {
		inorder(t.Left, ch)
	}

	ch <- value
	if t.Right != nil {
		inorder(t.Right, ch)
	}
}

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool {
	ch1 := make(chan int, 10)
	ch2 := make(chan int, 10)
	go Walk(t1, ch1)
	go Walk(t2, ch2)

	for i := range ch1 {
		if i != <-ch2 {
			return false
		}
	}

	return true
}

func main() {
	fmt.Println(Same(tree.New(1), tree.New(1)))
	fmt.Println(Same(tree.New(1), tree.New(2)))
}

```

<추후 설명 추가>

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

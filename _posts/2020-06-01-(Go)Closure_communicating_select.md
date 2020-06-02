---
layout: post
title: (Go) Closure, share memory by communicating, Select 개념
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

> [Github Source Code - Make Generator using Golang Concurrency](https://github.com/TakeaimK/Study_Goroutine_Channel){: target="\_blank"}

---

# 클로저의 개념

클로저, 영어로는 Closure이다. ~~(Closer가 아니다)~~  
Java나 Python에는 없는 개념으로, 생소하다. 기본적인 Golang의 문법을 소개하고 학습하는 사이트인 [A Tour of Go - function closures](https://tour.golang.org/moretypes/25)에는 아래와 같이 적혀 있다.

```
Go functions may be closures. A closure is a function value that references variables from outside its body. The function may access and assign to the referenced variables; in this sense the function is "bound" to the variables.

For example, the adder function returns a closure. Each closure is bound to its own sum variable.
```

```
Go의 함수는 클로저일 수 있습니다. 클로저는 몸체 외부의 변수를 참조하는 함수 값입니다. 함수는 참조된 변수에 접근하여 할당할 수 있습니다. 이런 의미에서 함수는 변수에 "바운드"됩니다.
예를 들어, adder 함수는 클로저를 반환합니다. 각각의 클로저는 자신만의 sum 변수를 가집니다.
```

위 말만 들어서는 무슨 소린지 잘 이해가 안 된다. 그래서 조금 더 영문 문서를 뒤적여 보았다. 그러다가 [What is a Closure?](https://www.calhoun.io/what-is-a-closure/)라는 사이트에 잘 정리가 되어 있어서 읽고 몇몇 사이트를 더 조사한 뒤 정리해 보았다.

우선, "익명 함수"(Anonymous function)에 대해 알아야 한다. 개념은 간단하다. 함수로 동작하되 이름이 없어 선언되며 거의 동시에 실행되는 함수이다. Golang에서는 함수를 값처럼 취급할 수 있다. 따라서, 아래 코드처럼 돌릴 수도 있다.

```go
package main

import "fmt"

var DoStuff func() = func() {
  // Do stuff
}

func main() {
  DoStuff()

  DoStuff = func() {
    fmt.Println("Doing stuff!")
  }
  DoStuff() //Doing stuff!

  DoStuff = func() {
    fmt.Println("Doing other stuff.")
  }
  DoStuff() //Doing other stuff.
}
```

여기서 "클로저"(Closure)는 함수 외부에 선언된 변수를 참조하는 특수한 유형의 익명 함수이다. 클로저가 동작하는 방식은 대략 아래 코드와 비슷하다. (아래 코드는 클로저는 아니다! 함수 외부에 선언된 변수를 가져오는 예시일 뿐이다)

```go
package main

import "fmt"

func main() {
  n := 0
  counter := func() int {
    n += 1
    return n
  }
  fmt.Println(counter())    //1
  fmt.Println(counter())    //2
}
```

위 코드에서 n은 main이 가진 값이고, 익명 함수에서 가져다가 +1을 시킨 다음 return한다. 이 때 n값은 0이 아닌 1로 저장되어 다음 익명 함수를 부를 때 n값을 기존과 같은 값으로 가져온다. 이제 진짜 클로저를 만나 보자.

```go
package main

import "fmt"

func main() {
  counter := newCounter()
  fmt.Println(counter())    //1
  fmt.Println(counter())    //2
}

func newCounter() func() int {
  n := 0
  return func() int {
    n += 1
    return n
  }
}
```

`newCounter()`라는 함수는 무려 함수, 정확히는 익명 함수를 리턴한다. 이 익명 함수는 newCounter가 가지는 n이라는 변수를 참조하여 +1을 한 뒤 이 값을 리턴하고, 이 값이 `newCounter()`의 최종 리턴 값이 되었다. 그런데 위 main코드에서 실행한 것과 마찬가지로, `newCounter()`의 n 값이 저장되어 있다가 계속해서 증가하는 모습을 볼 수 있다. 분명 newCounter의 n은 지역 변수처럼 작동할 텐데, 어떻게 유지될 수 있을까?  
잘 살펴보면, `counter = newCounter()`가 있다. counter라는 변수에 newCounter라는 함수를 할당한 것이다. 즉, counter는 함수 타입의 변수이다. 이렇게 counter라는 함수 값이 newCounter의 n을 유지하는 모양이 된다. 만일, `cnt := newCounter()`라 한 뒤, `fmt.Println(cnt())`를 수행한다면 n값은 0으로 돌아간 뒤 다시 수행할 것이다.

**클로저 한줄요약 : 함수 밖에 존재하는 변수를 접근하거나 수정하는 함수 값이며, 변수에 익명함수를 반환하면서 사용.**

---

# "메모리 공유를 통해 통신하지 말고 통신을 통해 메모리를 공유하라" 의미 파악 및 정리

일단, 영어 원문 문장을 찾고, Go blog에서 관련 글을 찾아보았다.

> [Do not communicate by sharing memory; instead, share memory by communicating.](https://blog.golang.org/codelab-share)

보통, 스레드를 사용하여 작업 시 공유 자원이 있기 마련이고, 무결성 보장 및 비정상적인 데이터 기록 등을 방지하기 위해 lock을 사용하여 하나의 작업만 공유 자원을 사용할 수 있도록 구성한다.  
그러나 Golang에서는 lock을 사용하는 대신, 스레드 간에 채널을 사용하는 것을 권장하고 있다. sync를 import시켜서 사용하는 Mutex와 달리 채널은 기본으로 제공하고 있다. 왜 굳이 범용적으로 사용하는 lock을 사용하지 않고, 채널을 통해 데이터를 주고받을 수 있도록 하는 것일까?  
원문 문장을 하나씩 뜯어서 분석한 글을 참조해서 해석해 보았다.

1. Do not communicate : 다른 곳에서 수정되는 메모리를 읽음으로써 다른 스레드의 상태 변경을 다른 스레드에서 알 수 있음. 즉, 같은 메모리의 일부를 두 개 이상의 스레드에서 접근함으로서 통신함을 지양하라는 의미.
2. by sharing memory : 여러 스레드에서 수정하여 읽을 수 있는 메모리 부분이 있음을 의미
3. instead, share memory : 각각의 고루틴이 가진 메모리 공간에서 각 데이터 구조에 맞게 수정한 뒤 채널을 통해 값이나 포인터를 다른 고루틴에 보내 데이터의 소유권을 부여할 수 있음을 의미. 즉, 직접적으로 데이터를 공유하는 공간이 없이 각 고루틴이 소유하는 메모리의 일부만 접근이 가능.
4. by communicating. : 직접 접근으로 공유하는 방식이 아닌, 하나의 고루틴이 가진 메모리 일부의 소유권을 다른 고루틴으로 넘기는 방식을 사용함을 의미. 즉, 메세지를 전달하는 방식으로 통신을 지향한다는 의미.

즉, 저 내용을 정리하면 다음과 같다.

**공유 메모리와 복잡하고 오류가 발생하기 쉬운 원시적인 동기화를 사용하여 스레드 간 통신을 과대하게 만들지 말고, 대신 고루틴 간의 메시지 전달을 사용하여 변수 및 데이터를 순차적으로 사용할 수 있다.**

---

# Select 구문 개념 정리

Select문은 switch와 비슷한 모양새를 가진다. 다만 동시성 프로그래밍에 사용되며, 두 개 이상의 채널에서 메세지를 기다려야 하는 경우 사용한다. 이 select 문은 아래와 같은 특징을 가진다.

- case는 switch와 다르게 순차적인 것이 아니라, 채널에 신호를 수신받으면 동작한다.
- 모든 case가 계산되며, select문 안에 함수가 있다면 select 수행 시 즉시 호출된다. 채널이 준비되어 있지 않더라도 말이다.

```go
select{
  case n := <-ch1:
    //Do
  case n := <-ch2:
    //Do
  case c3 <- f():
    //c3의 준비와 관계 없이 f() 호출
}
```

- 입출력이 가능한 case가 있다면 그 중 하나를 선택하여 해당 case의 코드를 수행한다.
- 동시에 두 채널에 신호가 여러 번 도착할 경우, 최대한 균등하게 배분하여 처리한다.

```go
c1 := make(chan interface{}); close(c1)
c2 := make(chan interface{}); close(c2)
var c1Count, c2Count int
for i := 1000; i >= 0; i-- {
    select {
        case <-c1:
            c1Count++
        case <-c2:
            c2Count++
        }
    }
fmt.Printf("c1Count: %d\nc2Count: %d\n", c1Count, c2Count)
//c1Count와 c2Count는 비슷한 Count를 가짐
```

- 준비된 채널이 없는 경우, 즉 모든 case에 입출력이 없는 상태일 경우 default를 사용하여 대기할 수 있다.

```go
start := time.Now()
var c1, c2 <-chan int
select {
    case <-c1:
    case <-c2:
    default:
      fmt.Printf("In default after %v\n\n", time.Since(start))
      //In default after 1.421µs
}

```

- 일정 시간만 채널과 통신을 기다리고자 하면 `time.After(wait time)` 함수를 사용한다. 이 함수는 wait time만큼 기다린 후 채널을 반환한다.

```go
var c <-chan int
select {
    case <-c:
    case <-time.After(5 * time.Second):
        fmt.Println("Timed out.")
        return
}
```

- for문을 사용하여 무한루프 안에 넣는다면 지속적인 통신도 가능하다.

즉, Select는 여러 개의 고루틴에서 채널을 통해 보낸 메시지를 받아 처리할 때 유용하다.

---

읽어주셔서 감사합니다!

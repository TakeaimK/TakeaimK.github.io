---
layout: post
title: (Go) 3. 흐름 제어
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

> [Github Source Code - Gotour](https://github.com/TakeaimK/Gotour){: target="\_blank"}

# A tour of Go

A tour of Go는 Golang의 특징을 공부할 수 있는 학습 사이트이다.
한국어 사이트와 영어 사이트가 있으며, 내용은 거의 동일하다.

> [gotour - 한국어](https://go-tour-kr.appspot.com/#6){: target="\_blank"}  
> [gotour - 영어](https://tour.golang.org/flowcontrol/1){: target="\_blank"}

---

## 반복문 (For)

```
Go 언어는 반복문이 for 밖에 없습니다.

기본적인 for 반복문은 C와 Java 언어와 거의 유사합니다. 다른점은 소괄호 ( )가 필요하지 않다는 것입니다.

하지만 실행문을 위한 중괄호 { } 는 필요합니다
```

```go
package main

import "fmt"

func main() {
	sum1 := 0
	sum2 := 0
    for i := 0; i < 10; i++ {
        sum1 += i
	}
	//sum2 = i*(i+1)/2	//i는 for문을 나오면 해제됨
	fmt.Println(sum1)
	fmt.Println(sum2)
}

```

Golang의 for문은 C++,Java와 유사하다. 특징도 비슷한데, for문 안에서 선언된 변수는 for문을 나가면 해제되어 사용할 수 없다.

---

```
C와 Java에서 처럼 전.후 처리를 제외하고 조건문만 표현할 수도 있습니다.

이전의 예제에서 처럼 조건문만 표시하면 C언어에서 while 을 사용하듯 for 를 사용할 수 있습니다.
```

```go
package main

import "fmt"

func main() {
	sum := 1
	rng := 5
    for sum < 1000 && rng > 0 {
		sum += sum
		rng--
    }
    fmt.Println(sum)
}


```

굳이 반복문을 while, do-while, for 세 가지로 만들 필요 없이 for 하나로 모든 역할을 수행한다.  
또한, and 및 or을 `&&` 및 `||` 기호를 사용하는 부분은 C++과 유사하다.

---

```
for에서 조건문을 생략하면 무한 루프를 간단하게 표현할 수 있습니다.
```

```go
package main

import "fmt"

func main() {
	i := 0
    for {
		i++
		if i == 10{
			break
		}
	}
	fmt.Println(i)
}

```

while(true) 기능을 구현하기는 더욱 간단하다. Golang에서 for문에 조건을 제시하지 않으면 기본적으로 true 상태가 된다.  
조건문을 넣어 break로 탈출하는 방식 역시 가능하다.

---

## 조건문 (if)

```
if 문은 C와 Java와 비슷합니다. 조건 표현을 위해 ( ) 는 사용하지 않습니다. 하지만 실행문을 위한 { } 는 반드시 작성해야합니다.

(For문과 비슷하죠?)
```

```go
package main

import (
    "fmt"
    "math"
)

func sqrt(x float64) string {
    if x < 0 {
        return sqrt(-x) + "i"
    }
    return fmt.Sprint(math.Sqrt(x))
}

func main() {
	fmt.Println(sqrt(2), sqrt(-4))

	var temp float64
	fmt.Scan(&temp)
	if temp < 0{
		fmt.Println(math.Sqrt(math.Abs(temp)),"i")
	}else if{
		fmt.Println(math.Sqrt(math.Abs(temp)))
	} else{    //개행 후 else 입력 시 에러 발생
        
	}
}

```

Go의 조건문은 C++ 등과 유사해 보이지만, 한 가지 차이점이 있다. **조건문의 결과가 무조건 Bool 형식**이어야 한다.  
또한, else if, else 문을 지원하지만, **직전 블럭의 닫는 괄호와 같은 라인에 위치**해야 한다.

---

```
for 처럼 if 에서도 조건문 앞에 짧은 문장을 실행할 수 있습니다.

예제에서는 조건을 비교하기 전에 `v := math.Pow(x,n)` 을 실행했습니다.

짧은 실행문을 통해 선언된 변수는 if 안쪽 범위(scope) 에서 만 사용할 수 있습니다.

(예제 코드의 pow 함수에서 return 전에 v 를 사용해보세요.)
```

```go
package main

import (
    "fmt"
    "math"
)

func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
		//v += 1 //<=가능함!
        return v
    }
    return lim
}

func main() {
    fmt.Println(
        pow(3, 2, 10),
        pow(3, 3, 20),
    )
}


```
`math.Pow(x,y)`는 x의 y승을 계산해 주는 함수이다. 조건문 안에서 계산하여 세미콜론으로 문장을 구분지어 비교가 가능하다.


---

```
if 에서 짧은 명령문을 통해 선언된 변수는 else 블럭 안에서도 사용할 수 있습니다.
```

```go
package main

import (
    "fmt"
    "math"
)

func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
        return v
    } else {
        fmt.Printf("%g >= %g\n", v, lim)
    }
    // can't use v here, though
    return lim
}

func main() {
    fmt.Println(
        pow(3, 2, 10),
        pow(3, 3, 20),
    )
}


```

```
함수와 루프의 사용법을 익히는 간단한 연습으로, 제곱근 함수를 뉴턴의 방법(Newton's method)을 이용하여 구현합니다.

여기서 뉴턴의 방법이란 초기값 z를 선택한 후에 다음의 공식을 이용하여 반복적으로 Sqrt(x) 함수의 근사값을 찾아가는 방법을 말합니다:

z = z - (z * z - x) / (2 * z)

처음에는 계산을 10번만 반복하여 여러분이 작성한 함수가 다양한 값들 (1, 2, 3, ...)에 대하여 얼마나 정확한 값을 찾아내는지 확인합니다.

그 다음에는, 루프의 조건을 수정하여 값이 더이상 바뀌지 않을 때 (혹은 아주 작은 차이가 발생할 때) 루프를 종료하도록 합니다. 이렇게 하면 반복문의 실행 횟수가 어떻게 달라지는지 확인합니다. 결과값이 math.Sqrt 함수의 값과 얼마나 비슷한가요?

힌트: 실수(floating point)값을 선언하고 초기화 하려면, 실수값을 표현하는 문법을 사용하거나 변환 함수를 사용합니다:
z := float64(1)
z := 1.0
```

```go
package main

import (
    "fmt"
)

func Sqrt(x float64) float64 {
}

func main() {
    fmt.Println(Sqrt(2))
}

```

---

## 조건문 (Switch)

```
A switch statement is a shorter way to write a sequence of if - else statements. It runs the first case whose value is equal to the condition expression.

Go's switch is like the one in C, C++, Java, JavaScript, and PHP, except that Go only runs the selected case, not all the cases that follow. In effect, the break statement that is needed at the end of each case in those languages is provided automatically in Go. Another important difference is that Go's switch cases need not be constants, and the values involved need not be integers.
```

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}


```

```
Switch cases evaluate cases from top to bottom, stopping when a case succeeds.

(For example,

switch i {
case 0:
case f():
}
does not call f if i==0.)

Note: Time in the Go playground always appears to start at 2009-11-10 23:00:00 UTC, a value whose significance is left as an exercise for the reader.
```

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("When's Saturday?")
	today := time.Now().Weekday()
	switch time.Saturday {
	case today + 0:
		fmt.Println("Today.")
	case today + 1:
		fmt.Println("Tomorrow.")
	case today + 2:
		fmt.Println("In two days.")
	default:
		fmt.Println("Too far away.")
	}
}

```

```
Switch without a condition is the same as switch true.

This construct can be a clean way to write long if-then-else chains.
```

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}
}


```

---

## 지연 실행 (Defer)

상수는 const 키워드와 함께 변수처럼 선언합니다.  
상수는 문자(character), 문자열(string), 부울(boolean), 숫자 타입 중의 하나가 될 수 있습니다.

```go
package main

import "fmt"

const Pi = 3.14

func main() {
    const World = "안녕"
    fmt.Println("Hello", World)
    fmt.Println("Happy", Pi, "Day")

    const Truth = true
    fmt.Println("Go rules?", Truth)
}

```

숫자형 상수는 정밀한 값(values) 을 표현할 수 있습니다.  
타입을 지정하지 않은 상수는 문맥(context)에 따라 타입을 가지게 됩니다.  
예를 들어, 아래 주석 부분은 동작하지 않습니다.

```go
package main

import "fmt"

const (
    Big   = 1 << 100	//2^100
  	Small = Big >> 99	//2^(100-99) = 2^1 = 2
	  intMax = 1<<63 -1
)

func needInt(x int) int { return x*10 + 1 }
func needFloat(x float64) float64 {
    return x * 0.1
}

func main() {
	  fmt.Println(Small)
	  //fmt.Println(Big)	//overflows int error 발생
	  fmt.Println(intMax)
    fmt.Println(needInt(Small))
    fmt.Println(needFloat(Small))
	  fmt.Println(needFloat(Big))
	  //fmt.Println(needInt(Big))	//역시 overflows int error 발생
}

```

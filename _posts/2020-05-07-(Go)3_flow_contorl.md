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

> [gotour - 한국어](https://go-tour-kr.appspot.com/#16){: target="\_blank"}  
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

if에서 선언된 조건문에 사용된 변수는, else에서도 활용이 가능하다. if와 else는 서로 뗄 수 없는 관계이며, 그래서 if 블록 다음 else를 바로 붙여 적어야 하게 만들었다는 느낌을 받는다.

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
    "math"
)

func Sqrt1(x float64, r int) float64 {
    z := float64(1)

    for i:=0; i<r; i++{
        z = z-(z*z-x)/(2*z)
    }
    return z
}

func Sqrt2(x float64) float64{
    z := float64(1)

    for {
        result := z-(z*z-x)/(2*z)

        if float64(result) == float64(z) {
                return result
        }
        z = result
    }
}

func main() {
    var num float64
    var rng int
    fmt.Print("Sqrt number : ")
    fmt.Scan(&num)
    fmt.Print("range : ")
    fmt.Scan(&rng)
    fmt.Println(Sqrt1(num, rng))
    fmt.Println(Sqrt2(num))
    fmt.Println(math.Sqrt(num))
}

```

뉴턴-랩슨의 방법에 대해서 자세히 알고 싶다면 [제곱근 구하기 - 바빌로니아, 뉴턴-랩슨 방법](https://dowhati1.tistory.com/m/31?category=722279){: target="\_blank"} 링크를 참조하자.  
우선 제곱근을 구할 수를 입력받고, Sqrt1 함수에서 반복할 횟수를 입력받는다. 그러면 (1)뉴턴-랩슨 방법에서 지정된 횟수만큼 돌린 값, (2)컴퓨터 계산으로 동일하다고 판단될 때까지 반복하며 돌린 값, (3)`math.Sqrt`를 사용한 값 순서로 출력한다.  
결과는 다음과 같다.

```
Sqrt number : 10
range : 1
5.5
3.1622776601683795
3.1622776601683795

Sqrt number : 10
range : 2
3.659090909090909
3.1622776601683795
3.1622776601683795

Sqrt number : 10
range : 3
3.196005081874647
3.1622776601683795
3.1622776601683795

Sqrt number : 10
range : 4
3.1624556228038903
3.1622776601683795
3.1622776601683795

Sqrt number : 10
range : 5
3.162277665175675
3.1622776601683795
3.1622776601683795

Sqrt number : 10
range : 6
3.1622776601683795
3.1622776601683795
3.1622776601683795
```

10의 제곱근을 구하고자 한다면, 6회를 돌려야 동일하게 나온다는 것을 알 수 있다. 무한루프를 돌린 값과 `math.Sqrt` 값은 같다. 즉, math 라이브러리에 있는 sqrt 함수와 거의 동일하다.  
실제 `math.Sqrt`는 다음과 같다.
[Source file src/math/sqrt.go](https://golang.org/src/math/sqrt.go)

---

## 조건문 (Switch) - Eng ver에만 존재

```
Switch 문은 if-else 문의 순서를 작성하는 더 짧은 방법이다. 값이 조건식과 같은 첫 번째 경우를 실행한다.
Go의 스위치는 C, C++, Java, Javascript, PHP의 Switch와 같으나, break 문이 필요 없이 선택된 항목에 대해서만 실행된다.
또 다른 중요한 점은, Switch의 case 값이 꼭 상수가 아니어도 되고, 관련 값은 정수가 아니어도 된다.
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

Go 언어의 switch는 break문이 필요 없다. 알아서 case에 걸리면 해당 case만 실행하고 switch문을 탈출한다. 더욱이, case 자리에 문자열이나 함수의 결과값이 들어가도 된다!

---

```
switch문은 위에서 아래로 훑으며 case에 걸리면 나머지 case는 진행하지 않는다.

(예를 들어,

switch i {
case 0:
case f():
}
i==0이면 f는 부르지 않음)

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

만약 토요일에 본 프로그램을 작동시킨다면 Today가 나올 것이다. 만약 오늘이 토요일이라면 Today가 출력되고 그 아래로 진행하지 않는다.  
또한, default 값도 설정이 가능하다는 것을 알 수 있다.

---

```
조건이 없는 switch는 true와 동일하다.
이 구조는 긴 if-then-else 체인을 쓰는 것보다 깔끔한 방법이 될 수 있다.
```

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	fmt.Println(t.Hour())	//22
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")	//출력됨
	}
}



```

이 부분이 매우 충격적이고 신선하다. if문을 사용하는 것보다 너무나도 깔끔하다! 사실 switch문은 생각보다 잘 쓰이지 않는 편인데, case가 상수여야 하는 조건이 생각보다 크다. 그런데 case 자리에 t.Hour()과 상수를 비교해서 참이면 출력시키는 참신한 방법으로 코드를 간결하게 만들어 준다.

---

## 지연 실행 (Defer) - Eng ver에만 있음

Defer(지연문)은 함수가 return될 때까지 해당 구문의 실행을 연기합니다. 지연된 호출 인수는 즉시 계산되지만, 함수가 return될 때까지 기다립니다.

```go
package main

import "fmt"

func main() {
	defer fmt.Println("world")

	fmt.Println("hello")
}


```

지연 구문은 Java 등에서 finally와 같이 함수 실행 이후 마지막으로 실행되는 구문이다. 해당 함수가 실행을 마칠 때까지 기다리는데, 위 구문에서는 hello가 먼저 출력되고, main이 종료되는 시점에 world를 출력한다.

---

```
지연되는 구문은 Stack에 push된다. LIFO(Last-In-First-Out) 방식으로 꺼내온다.
```

```go
package main

import "fmt"

func main() {
	fmt.Println("counting")

	for i := 0; i < 10; i++ {
		defer fmt.Println(i)
	}

	fmt.Println("done")
}


```

위 프로그램의 출력 결과는 우선 counting이 출력된다. 후에 0부터 9까지 stack에 쌓이게 되고, done을 출력한다. main이 끝나는 시점에서 stack에서 LIFO로 꺼내오게 되고, 9부터 1까지 역순으로 출력된다.  
이걸 어디에 쓸까 생각해 보았는데, 파일을 열고 작업할 때 어떠한 문제가 생기더라도 미리 close를 걸어두면 파일이 안전하게 닫히지 않을까 추측해 보았다. 즉, 꼭 마무리되어야 할 작업이 있다면 defer를 사용하지 않을까 싶다.

---

읽어주셔서 감사합니다!

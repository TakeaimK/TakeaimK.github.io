---
layout: post
title: (Go) 2. 패키지, 변수, 함수
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

> [Github Source Code - Gotour](https://github.com/TakeaimK/Gotour){: target="\_blank"}

# A tour of Go

A tour of Go는 Golang의 특징을 공부할 수 있는 학습 사이트이다.
한국어 사이트와 영어 사이트가 있으며, 내용은 거의 동일하다.

> [gotour - 한국어](https://go-tour-kr.appspot.com/#1){: target="\_blank"}  
> [gotour - 영어](https://tour.golang.org/welcome/1){: target="\_blank"}

---

## 패키지 (Package)

```
모든 Go 프로그램은 패키지로 구성되어 있습니다.
프로그램은 main 패키지에서부터 실행을 시작합니다.
이 프로그램은 `"fmt"`와 "math" 패키지를 import 해서 사용하고 있습니다.
**패키지 이름은 디렉토리 경로의 마지막 이름을 사용**하는 것이 규칙입니다.
예를 들어 "path/filepath" 를 사용한다면 패키지명은 filepath 입니다.
```

```go
package main

import (
    "fmt"
    "math"
)

func main() {
	fmt.Println("Happy", math.Pi, "Day");
	fmt.Println(math.Abs(-123));
}

```

---

## 임포트 (import)

```
이 코드에서는 여러개의 "package" 를 소괄호로 감싸서 import를 표현합니다. 주석과 같이 import 문장을 여러번 사용할 수 도 있습니다.
```

```go
package main

import (
    "fmt"
    "math"
)
/*
import "fmt"
import "math"
*/

func main() {
	fmt.Println("Now you have %g problems.", math.Nextafter(2, 3))
	//Nextafter(x,y) : x보다 y가 클 경우 표현할 수 있는 x보다 큰 실수
	fmt.Printf("20에 Root를 씌운 값은 %f 입니다.", math.Sqrt(20))
}

```

---

## 익스포트 (Exported names)

```
패키지를 Import 하면 패키지가 외부로 export 한 것들(메서드나 변수, 상수 등)에 접근할 수 있습니다.
Go에서는 첫 문자가 대문자로 시작하면 그 패키지를 사용하는 곳에서 접근할 수 있는 exported name이 됩니다.
예를 들어 Foo 와 FOO 는 외부에서 참조할 수 있지만 foo 는 참조 할 수 없습니다.
아래 예문에서 주석은 동작하지 않습니다.
```

```go
package main

import (
    "fmt"
    "math"
)

func main() {
	//fmt.Println(math.pi)
	fmt.Println(math.Pi)
}

```

---

## 함수 (Function)

```
함수는 매개변수(인자)를 가질 수 있습니다.
예를 들어 add 라는 함수는 두개의 int 타입 매개변수를 받습니다.
C, C++, Java 언어와 다르게 매개변수의 타입은 변수명 뒤에 명시합니다.
타입을 뒤에 놓는 이유는 코드를 자연스럽게 읽기 위해서입니다.
```

```go
package main

import "fmt"

func add(x int, y int) int {
    return x + y
}

func add_a_to_b(a int, b int) int{
	x:=b+1
	return b*x/2
}

func main() {
	fmt.Println(add(42, 13))
	fmt.Print(add_a_to_b(1,10))
}

```

```
두 개 이상의 매개변수가 같은 타입(type)일 때, 같은 타입을 취하는 마지막 매개변수에만 타입을 명시하고 나머지는 생략할 수 있습니다.
```

```go
package main

import "fmt"

func add(x, y int) int {
    return x + y
}

func add_a_to_b(a, b int) int{
	x:=b+1
	return b*x/2
}

func main() {
	fmt.Println(add(42, 13))
	fmt.Print(add_a_to_b(1,10))
}

```

```
하나의 함수는 여러 개의 결과를 반환할 수 있습니다.
```

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
    return y, x
}

func main() {
    a, b := swap("hello", "world")
    fmt.Println(a, b)
}

```

```
함수는 매개변수를 취합니다. Go에서 함수는 여러 개의 결과를 반환할 수 있습니다. 반환 값에 이름을 부여하면 변수처럼 사용할 수도 있습니다.
결과에 이름을 붙히면, 반환 값을 지정하지 않은 return 문장으로 결과의 현재 값을 알아서 반환합니다.
```

```go
package main

import "fmt"

func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return
}

func money(total int)(a,b,c int){
	a = total/1000
	total %= 1000
	b = total/100
	total %= 100
	c = total/10
	return
}

func main() {
	fmt.Println(split(17))

	var temp int
	fmt.Print("만원 이하의 돈을 입력하세요")
	//a,b,c := money(fmt.Scanln(&temp)) => error(too many arguments)
	fmt.Scanln(&temp)
	a,b,c := money(temp)
	//fmt.Print("천원 : %d장, 백원 : %d개, 십원 : %d개 입니다.", a,b,c)
	fmt.Printf("천원 : %d장, 백원 : %d개, 십원 : %d개 입니다.", a,b,c)
}

```

---

## 변수 (Variables)

```
변수를 선언을 위해 var 을 사용합니다.
함수의 매개변수처럼 타입은 문장 끝에 명시합니다.
```

```go
package main

import "fmt"

var x, y, z int
var c, python, java bool
var golang float32

func main() {
	fmt.Println(x, y, z, c, python, java)
	fmt.Scanln(&golang)
	fmt.Printf("You typed %f \n", golang)
}

```

```
변수 선언과 함께 변수 각각을 초기화를 할 수 있습니다.
초기화를 하는 경우 타입(type)을 생략할 수 있습니다. 변수는 초기화 하고자 하는 값에 따라 타입이 결정됩니다.
```

```go
package main

import "fmt"

var x, y, z int = 1, 2, 3
var c, python, java = true, false, "no!"

func main() {
	fmt.Println(x, y, z, c, python, java)

	var i = 100
	var s = "Kakao Enterprise"

	fmt.Println("나는",i,"% 자신감을 충전했다.")
	fmt.Print(s)
}

```

```
함수 내에서 := 을 사용하면 var 과 명시적인 타입(e.g. int, bool) 을 생략할 수 있습니다.
그러나 함수 밖에서는 := 선언을 사용할 수 없습니다.
```

```go
package main

import "fmt"

func main() {
	var x, y, z int = 1, 2, 3
	w := 8	//함수 안에서만 사용 가능!
    c, python, java := true, false, "no!"
	s := "iPhone"

	fmt.Println(x, y, z, c, python, java)

	fmt.Printf("Apple %s %d", s, w)
}

```

---

## 상수 (Constants)

```
상수는 const 키워드와 함께 변수처럼 선언합니다.
상수는 문자(character), 문자열(string), 부울(boolean), 숫자 타입 중의 하나가 될 수 있습니다.
```

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

```
숫자형 상수는 정밀한 값(values) 을 표현할 수 있습니다.
타입을 지정하지 않은 상수는 문맥(context)에 따라 타입을 가지게 됩니다.
예를 들어, 아래 주석 부분은 동작하지 않습니다.
```

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

---

읽어주셔서 감사합니다!

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

## 학습 진행 방식

- gotour 설명과 기본 예제 코드를 기본으로 삼고, 추가 코드를 간단하게 작성하기도 한다.
- 예제문을 분석하고, 내가 바라본 특징에 대해 기술한다.

---

## 패키지 (Package)

```
모든 Go 프로그램은 패키지로 구성되어 있습니다.
프로그램은 main 패키지에서부터 실행을 시작합니다.
이 프로그램은 `"fmt"`와 "math" 패키지를 import 해서 사용하고 있습니다.
패키지 이름은 디렉토리 경로의 마지막 이름을 사용하는 것이 규칙입니다.
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

우선, 패키지에 대해 설명하고 있다.  
Java 등의 언어에서도 패키지로 코드를 묶어 관리한다. 주목해야 할 점은, **go 프로그램을 실행하는 핵심은 main패키지의 main함수**라는 것이다.  
만약, main패키지의 이름을 바꾸게 되면 `package name must be main`라는 오류를 출력한다.

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
	//"net/http"
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

import 아래 주석 처리로 된 부분이 기존 다른 언어의 import와 약간 유사하다. 저 방식으로도 작동한다.  
하지만 대부분의 경우 여러 개의 패키지를 import하는데, 각각 import를 반복해서 적어줘야 하는 불편함이 있다. Golang은 이러한 불편함을 해결하기 위해 위와 같은 방법을 사용한 것으로 보인다.  
또 다른 특징은, 사용하지 않는 패키지를 import하는 경우, 에러를 발생시킨다. 위 코드에서 `net/http`를 import하고 사용하지 않는다면, `imported and not used: "net/http"`라는 에러를 출력하고, 컴파일되지 않는다. 사용하지 않는 패키지는 import에서 제거해 주어야 한다.

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

[0.Go?](<http://takeaimk.tk/language-go/2020/05/05/(Go)0_Go_preview.html>){: target="\_blank"} 게시글에 설명한 Go의 특징 중, `대문자로 시작하면 Public, 소문자로 시작하면 private 역할을 수행` 이라는 내용이 있었다.  
만약, `math.pi`라고 접근하게 된다면, math 패키지 내에서만 접근할 수 있는 함수를 main 패키지에서 접근을 시도하게 되는데, 원천적으로 막아놓는다. main함수도 다른 패키지에서 불러올 수 없도록 소문자로 시작한다.

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

func add2(a int, b int) {
	fmt.Println(a+b)
}

func ret777 () int{
	return 777
}

func main() {
	fmt.Println(add(42, 13))	//55
	add2(6,4)					//10
	fmt.Println(ret777())		//777
	fmt.Println(ret777)			//0x49dd50
}

```

Golang의 function의 특징은, (1)함수라는 것을 밝히고 (2)함수의 이름을 알리고 (3)이 함수의 매개변수는 어떠한 것이 있으며 (4)리턴 타입은 이것이다 순서로 기술된다.  
몇 가지 함수를 추가로 만들어 테스트해 보았는데, 함수의 특징을 알 수 있었다.

1. `func add(x int, y int) int`에서 매개변수를 받을 때도 변수명-타입 순으로 기술한다.
2. `func add2(a int, b int)`에서 리턴 값이 없으면 리턴 타입은 적지 않아도 작동한다.
3. `func ret777 () int`에서 매개변수가 없을 땐 빈 괄호를 적어준다.
4. `fmt.Println(ret777)`를 실행시키면, 함수가 위치한 주소값으로 추정되는 값이 출력된다!

---

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

위 함수의 매개변수에서 int를 반복해서 먹어야 하는 불편함을 해소하기 위해 같은 타입은 콤마 형태로 이어 서술한다.

---

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

역시 여러 개의 반환 값을 가지면 괄호로 묶어 돌려줄 수 있다.  
뒤에 나오지만, main 함수의 a, b 선언 부분이 인상적인데, Python처럼 변수의 타입을 지정하지 않고 `:=`을 사용하여 바로 값을 넣어줄 수 있으며, 알아서 a, b라는 변수의 타입이 지정된다.

---

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

학습하면서 신기했던 부분 중 하나이다. **미리 return할 변수를 함수 생성 시 선언하고, return만 입력하면 알아서 값을 반환**시킬 수 있다. 굳이 함수 내부에서 return하기 위해 변수를 선언하느라 코드 한 줄 더 적을 필요가 없다!

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

var(
	a int
	b string
)

func main() {
	fmt.Println(x, y, z, c, python, java)
	fmt.Println(a,b)
	fmt.Scanln(&golang)
	fmt.Printf("You typed %f \n", golang)
}


```

변수는 variable의 앞 3글자를 따서 var로 통칭한다. 가능한 타입은 자료형 파트에서 나오므로 일단 넘어가기로 하고, 다른 언어에서 지원하는 int, bool 등의 자료형이 존재함을 알 수 있다.  
또한 import와 마찬가지로 **`var()` 형태로 여러 개의 변수를 한 번에 묶어 선언**할 수 있다. 또한, 아무런 값을 넣지 않는다면 **초기 값은 int는 0으로, string은 빈 값으로, bool은 false로 초기화**된다.
또한 `fmt` 패키지에 있는 `Scanln` 함수를 가져다 사용해 보았다. Scan에 관련된 사용법은 [콘솔 입력 함수 사용하기 - 언제나휴일](http://ehpub.co.kr/%EA%B5%AC%EA%B8%80-go-%ED%95%98%EC%9E%90-25-%ED%91%9C%EC%A4%80-%EC%9E%85%EB%A0%A5-%ED%95%A8%EC%88%98-scanln-scan-scanf-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0/){: target="\_blank"} 사이트를 참고하였다.

---

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

x,y,z와 다르게, 아래 c,python,java에서는 bool과 string 타입을 선언하지 않았지만, 변수의 내용에 따라 알아서 지정되는 것을 알 수 있다.  
또한 `fmt.Println("나는",i,"% 자신감을 충전했다.")`라는 코드를 추가해 보았는데, string 사이에 i라는 int 형 변수를 콤마(,)를 사용하여 추가할 수 있다.

---

```
함수 내에서 := 을 사용하면 var 과 명시적인 타입(e.g. int, bool) 을 생략할 수 있습니다.
그러나 함수 밖에서는 := 선언을 사용할 수 없습니다.
```

```go
package main

import "fmt"

var s = "galaxy S"

func main() {
	var x, y, z int = 1, 2, 3
	w := 8	//함수 안에서만 사용 가능!
    c, python, java := true, false, "no!"
	s := "iPhone"

	fmt.Println(x, y, z, c, python, java)

	fmt.Printf("Apple %s %d", s, w)		//Apple iPhone 8
}

```

위에서 한 번 언급한 기호 `:=`가 등장했다. :=는 해당 함수 내에서 변수를 선언할 때 좀 더 편리하게 사용할 수 있는데, 전역변수가 아닌 해당 함수에서 사용하는 변수임을 확실하게 알리는 효과도 있다.  
또한 지역 변수가 더 높은 우선순위를 가진다. 위 `fmt.Printf("Apple %s %d", s, w)`를 출력하면 상단에 선언한 `var s = "galaxy S"` 가 아닌, `s := "iPhone"`를 우선하여 가져와 출력한다. (그래도 이름이 동일하게 변수를 선언하는 건 좋은 습관은 아닌 것 같다...)

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

    test := "World!"
    fmt.Println("Hello", test)
    test = "세상!"
    fmt.Println("Hello", test)
    //World = "Hi"

}

```

상수는 변하지 않는 고정된 값으로, 변경할 수 없다. 위 코드에서 `test`는 변경되어 출력되지만, `World`를 변경하려 하면 `cannot assign to World` 오류와 함께 에러가 출력된다.

---

```
숫자형 상수는 정밀한 값(values) 을 표현할 수 있습니다.
타입을 지정하지 않은 상수는 문맥(context)에 따라 타입을 가지게 됩니다.
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

상수도 역시 import와 마찬가지로 **`const()` 의 형태로 여러 개를 묶어 선언**할 수 있다.  
64bit 시스템에서 int는 8바이트의 크기를 가진다는 점도 인상적이다. 따라서 2^63-1을 초과하는 수는 에러가 발생하게 된다.

---

### 참고 링크

> [Go언어 배우기 - 패키지](https://medium.com/@yhmin84/a-tour-of-go%EB%A1%9C-%EB%B0%B0%EC%9A%B0%EA%B8%B0-1-%ED%8C%A8%ED%82%A4%EC%A7%80-package-%EC%99%80-%EC%9E%84%ED%8F%AC%ED%8A%B8-import-a91e9db1c135){: target="\_blank"}  
> [Go 표현 범위에 따라 원하는 정수 형식 사용 - 언제나휴일](http://ehpub.co.kr/%EA%B5%AC%EA%B8%80-go-%ED%95%98%EC%9E%90-6-%ED%91%9C%ED%98%84-%EB%B2%94%EC%9C%84%EC%97%90-%EB%94%B0%EB%9D%BC-%EC%9B%90%ED%95%98%EB%8A%94-%EC%A0%95%EC%88%98-%ED%98%95%EC%8B%9D-%EC%82%AC%EC%9A%A9/){: target="\_blank"}

읽어주셔서 감사합니다!

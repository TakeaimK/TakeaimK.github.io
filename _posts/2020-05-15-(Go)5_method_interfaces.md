---
layout: post
title: (Go) 5. 메소드와 인터페이스
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

> [Github Source Code - Gotour](https://github.com/TakeaimK/Gotour){: target="\_blank"}

# A tour of Go

A tour of Go는 Golang의 특징을 공부할 수 있는 학습 사이트이다.
한국어 사이트와 영어 사이트가 있으며, 내용은 거의 동일하다.

> [gotour - 한국어](https://go-tour-kr.appspot.com/#50){: target="\_blank"}  
> [gotour - 영어](https://tour.golang.org/methods/1){: target="\_blank"}

---

## 메소드 (Methods)

```
Go에는 클래스가 없습니다. 하지만 메소드를 구조체(struct)에 붙일 수 있습니다.

메소드 리시버(method receiver) 는 func 키워드와 메소드의 이름 사이에 인자로 들어갑니다.
```

```go
package main

import (
    "fmt"
    "math"
)

type Vertex struct {
    X, Y float64
}

func (v *Vertex) Abs() float64 {
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
    v := &Vertex{3, 4}
    fmt.Println(v.Abs())
}


```

<내용 추가>

---

```
사실 메소드는 구조체(struct) 뿐 아니라 아무 타입(type)에나 붙일 수 있습니다.

다른 패키지에 있는 타입이나 기본 타입들에 메소드를 붙이는 것은 불가능합니다.
```

```go
package main

import (
    "fmt"
    "math"
)

type MyFloat float64

func (f MyFloat) Abs() float64 {
    if f < 0 {
        return float64(-f)
    }
    return float64(f)
}

func main() {
    f := MyFloat(-math.Sqrt2)
    fmt.Println(f.Abs())
}

```

<내용 추가>

---

```
메소드는 이름이 있는 타입 또는 이름이 있는 타입의 포인터와 연결할 수 있습니다.

방금 두 개의 Abs 메소드를 보았는데, 하나는 *Vertex 라는 포인터 타입의 메소드고, 다른 하나는 MyFloat 값 타입의 메소드 입니다.

포인터 리시버를 사용하는 이유는 두 가지 입니다. 첫째, 메소드가 호출될 때 마다 값이 복사되는 것(큰 구조체 타입인 경우 값이 복사되는 것은 비효율적이죠)을 방지하기 위함 입니다. 다른 이유는 메소드에서 리시버 포인터가 가르키는 값을 수정하기 위함 입니다.

*Vertex 타입의 리시버 대신 Vertex 를 사용하도록 메소드 Abs 와 Scale 의 선언부분을 바꿔 보세요.

v 를 Vertex 타입으로 받으면 Scale 메소드가 더 이상 동작하지 않습니다. Scale 은 v 를 바꾸는데, v 가 (포인터가 아닌) 값 타입이기 때문에 Vertex 타입인 복사본에 작업을 하기 때문에 원래의 값은 바뀌지 않습니다.

Abs 의 경우는 다릅니다. 여기서는 v 를 읽기만 하기 때문에, (포인터가 가르키는) 원래의 값이건 복사본이건 상관이 없게 됩니다.
```

```go
package main

import (
    "fmt"
    "math"
)

type Vertex struct {
    X, Y float64
}

func (v *Vertex) Scale(f float64) {
    v.X = v.X * f
    v.Y = v.Y * f
}

func (v *Vertex) Abs() float64 {
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
    v := &Vertex{3, 4}
    v.Scale(5)
    fmt.Println(v, v.Abs())
}

```

<내용 추가>

---

## 인터페이스 (Interface)

```
인터페이스는 메소드의 집합으로 정의됩니다.

그 메소드들의 구현되어 있는 타입의 값은 모두 인터페이스 타입의 값이 될 수 있습니다.
```

```go
package main

import (
    "fmt"
    "math"
)

type Abser interface {
    Abs() float64
}

func main() {
    var a Abser
    f := MyFloat(-math.Sqrt2)
    v := Vertex{3, 4}

    a = f  // a MyFloat implements Abser
    a = &v // a *Vertex implements Abser
    a = v  // a Vertex, does NOT
    // implement Abser

    fmt.Println(a.Abs())
}

type MyFloat float64

func (f MyFloat) Abs() float64 {
    if f < 0 {
        return float64(-f)
    }
    return float64(f)
}

type Vertex struct {
    X, Y float64
}

func (v *Vertex) Abs() float64 {
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}


```

<설명 추가>

---

```
타입이 인터페이스의 메소드들을 구현하면 인터페이스를 구현한 게 됩니다.

이를 위해 명시적으로 선언할 게 없습니다.

암시적 인터페이스는 인터페이스를 정의한 패키지로 부터 구현 패키지를 분리(decouple)해 줍니다. 다른 의존성 또한 없음은 물론입니다.

이 특징은 상세하게 인터페이스를 정의하게 독려합니다. 모든 구현을 찾아 새 인터페이스 이름으로 태그할 필요가 없기 때문입니다.

패키지 io에 Reader 와 Writer 가 정의되어 있습니다. 따로 정의할 필요가 없습니다.
```

```go
package main

import (
    "fmt"
    "os"
)

type Reader interface {
    Read(b []byte) (n int, err error)
}

type Writer interface {
    Write(b []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}

func main() {
    var w Writer

    // os.Stdout implements Writer
    w = os.Stdout

    fmt.Fprintf(w, "hello, writer\n")
}

```

<설명 추가>

---

## 에러 (error)

```
에러 문장(string)으로 자신을 표현할 수 있는 것은 모두 에러입니다. 이 아이디어는 문자열(string)을 반환하는 하나의 메소드 Error 로 구성된 내장 인터페이스 타입 error 에서 나왔습니다.

type error interface {
	Error() string
}
fmt 패키지의 다양한 출력 루틴들은 error 의 출력을 요청받았을 때 자동으로 이 메소드를 호출합니다.
```

```go
package main

import (
    "fmt"
    "time"
)

type MyError struct {
    When time.Time
    What string
}

func (e *MyError) Error() string {
    return fmt.Sprintf("at %v, %s",
        e.When, e.What)
}

func run() error {
    return &MyError{
        time.Now(),
        "it didn't work",
    }
}

func main() {
    if err := run(); err != nil {
        fmt.Println(err)
    }
}


```

<내용 추가>

---

```
당신의 Sqrt 함수를 이전 연습에서 복사하고 error 값을 반환하도록 수정하십시오.

Sqrt 함수는 복소수를 지원하지 않기 때문에, 음수가 주어지면 nil 이 아닌 에러 값을 반환해야 합니다.

새로운 타입을 만드십시오.

type ErrNegativeSqrt float64
and make it an error by giving it a 그리고 아래 메소드를 구현함으로써 그 타입이 error 가 되게 하십시오.

func (e ErrNegativeSqrt) Error() string
이는 ErrNegativeSqrt(-2).Error() 가 "cannot Sqrt negative number: -2" 를 반환하는 그러한 메소드입니다.

Note: Error 메소드 내에서 fmt.Print(e) 를 호출하면 이 프로그램을 무한루프에 빠질 것입니다. e 를 바꿈으로써 이 문제를 피할 수 있습니다. 왜 그럴까요?

음수가 주어졌을 때 ErrNegativeSqrt 값을 반환하도록 당신의 Sqrt 함수를 바꾸십시오.
```

```go
package main

import (
    "fmt"
)

type ErrNegativeSqrt float64

func (e ErrNegativeSqrt) Error() string{

}

func Sqrt(f float64) (float64, error) {
    return 0, nil
}

func main() {
    fmt.Println(Sqrt(2))
    fmt.Println(Sqrt(-2))
}

```

<코드 및 내용 추가>

---

## 웹 서버 (Web Server)

```
Package http 는 http.Handler 를 구현한 어떠 값을 사용하여 HTTP 요청(requests)을 제공합니다.

package http

type Handler interface {
	ServeHTTP(w ResponseWriter, r *Request)
}
이 예제에서, Hello 라는 타입은 http.Handler 를 구현합니다.

이 코드를 로컬에서 실행하고, http://localhost:4000/ 에 접속해보세요.
```

[http.Handler](https://golang.org/pkg/net/http/)

```go
package main

import (
    "fmt"
    "net/http"
)

type Hello struct{}

func (h Hello) ServeHTTP(
    w http.ResponseWriter,
    r *http.Request) {
    fmt.Fprint(w, "Hello!")
}

func main() {
    var h Hello
    http.ListenAndServe("localhost:4000", h)
}

```

<내용 추가>

---

```
아래 나오는 타입을 구현하고 그 타입의 ServeHTTP 메소드를 정의하십시오. 그 메소드를 당신의 웹 서버에서 특정 경로를 처리할 수 있도록 등록하십시오.

type String string

type Struct struct {
	Greeting string
	Punct    string
	Who      string
}
예컨대, 당신은 아래와 같이 핸들러를 등록할 수 있어야 합니다.

http.Handle("/string", String("I'm a frayed knot."))
http.Handle("/struct", &Struct{"Hello", ":", "Gophers!"})
```

```go
package main

import (
    "net/http"
)

func main() {
    // your http.Handle calls here
    http.ListenAndServe("localhost:4000", nil)
}

```

<코드 및 내용 추가>

---

## 이미지 (Image)

```
Package image 는 Image 인터페이스를 정의합니다.

package image

type Image interface {
	ColorModel() color.Model
	Bounds() Rectangle
	At(x, y int) color.Color
}
(모든 세부사항에 대한 것은 아래 문서 를 참고하십시오.)

또한, color.Color 와 color.Model 는 인터페이스이지만, 미리 정의된 구현체인 color.RGBA 와 color.RGBAModel 을 사용함으로써 그 인터페이스를 무시할 수 있습니다.
```

[image.Image](https://golang.org/pkg/image/#Image)

```go
package main

import (
    "fmt"
    "image"
)

func main() {
    m := image.NewRGBA(image.Rect(0, 0, 100, 100))
    fmt.Println(m.Bounds())
    fmt.Println(m.At(0, 0).RGBA())
}

```

<내용 수정>

---

```
이전의 연습에서 당신이 작성한 그림 생성기를 기억하십니까? 다른 생성기를 만들어봅시다. 하지만 이번에는 데이터의 슬라이스 대신에 image.Image 의 구현체를 반환할 것입니다.

당신 자신의 Image 타입을 정의하시고, 필수 함수들 을 구현하신 다음, pic.ShowImage 를 호출하십시오.

Bounds 는 image.Rect(0, 0, w, h) 와 같은 image.Rectangle 을 반환해야 합니다.

ColorModel 은 color.RGBAModel 을 반환해야 합니다.

At 은 하나의 컬러를 반환해야 합니다; 지난 그림 생성기에서 값 v 는 color.RGBA{v, v, 255, 255} 와 같습니다.
```

```go
package main

import (
    "code.google.com/p/go-tour/pic"
    "image"
)

type Image struct{}

func main() {
    m := Image{}
    pic.ShowImage(m)
}

```

<코드 및 내용 수정>

---

```
슬라이스의 zero value는 nil 입니다.

nil 슬라이스는 길이와 최대 크기가 0입니다.

(슬라이스에 대해 더 알고 싶다면 다음 글을 읽어보세요.)
```

[Slices: usage and internals](https://blog.golang.org/slices-intro){: target="\_blank"}

```go
package main

import "fmt"

func main() {
    var z []int
    fmt.Println(z, len(z), cap(z))
    if z == nil {
        fmt.Println("nil!")
	}

	var a []int
	var b []int = make([]int, 0)
	var c []int = []int{}

	fmt.Println(a, b, c) // [] [] []

	fmt.Println(a == nil) // true
	fmt.Println(b == nil) // false
	fmt.Println(c == nil) // false
}

```

변수를 만들었으나 아무것도 할당하지 않은 경우, 즉 make를 수행하지도 않고 내부 요소에 대한 어떠한 항목도 없는 경우 nil slice가 된다.  
다만, 위 코드에서 b와 c는 길이와 용량이 0이지만 nil slice가 아니다. 정말 선언하고 아무것도 취하지 않아야 nil이 된다.

---

```
어떤 식으로든 스트림을 수정하여 다른 io.Reader 를 감싸는 io.Reader 는 흔한 패턴입니다.

예컨대, gzip.NewReader 함수는 io.Reader (gzip으로 압축된 데이터의 스트림) 를 가지고, io.Reader (압축 해제된 데이터의 스트림) 를 구현한 `*gzip.Reader`를 반환합니다.

ROT13 치환 암호화를 모든 알파벳 문자에 적용함으로써 스트림을 수정하며 io.Reader 를 구현하고 io.Reader 로 부터 읽는 rot13Reader 를 구현하십시오.

rot13Reader 타입은 당신을 위해 제공됩니다. 이 타입의 Read 함수를 구현함으로써 io.Reader 을 만들어 보십시오.
```

```go
package main

import (
    "io"
    "os"
    "strings"
)

type rot13Reader struct {
    r io.Reader
}

func main() {
    s := strings.NewReader(
        "Lbh penpxrq gur pbqr!")
    r := rot13Reader{s}
    io.Copy(os.Stdout, &r)
}


```

<내용 추가>

---

읽어주셔서 감사합니다!

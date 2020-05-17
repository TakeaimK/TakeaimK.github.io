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

구조체 포인터 타입을 가지는 메소드 형태로 구조체에 엮인 함수를 만들 수 있다.

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

굳이 구조체가 아니더라도 직접 만든 자료형에도 가능하다.

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

전 챕터에서 구조체 자체를 넘기는 것과 구조체 포인터를 넘기는 것의 차이와 동일한 문제이다. 만약 위 Scale 메소드의 앞부분을 `(v Vertex)라고 선언한다면, 해당 메소드는 값을 계산하고 종료되는 순간 값이 사라진다.  
Scale 메소드는 구조체 내부 값을 변경해 주는 메소드이기 때문에 값이 유지되어야 하고, Abs 메소드는 return되어 돌아오는 값이므로 무관하다.

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

메소드의 모음을 인터페이스라고 한다. 나는 이 개념이 왜 존재하는가 잘 이해되지 않았다. 그래서 여러 사이트를 찾아봤고, 개념과 사용처에 관한 사이트를 몇 개 찾았다. 아래 사이트를 참고하여 공부하였다.  
[Golang 인터페이스 사용하기 - 인터페이스 선언과 사용](http://pyrasis.com/book/GoForTheReallyImpatient/Unit32)  
[Go 인터페이스 - 인터페이스 매개변수, 빈 인터페이스](http://golang.site/go/article/18-Go-%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4)  
[Go 메소드와 인터페이스 - 상속과 유사한 방법으로 사용](https://kamang-it.tistory.com/entry/Go16%EB%A9%94%EC%86%8C%EB%93%9C%EC%99%80-%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4)

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

예외처리 등의 방식을 사용하지 않고 대신 에러 타입에 대해 인터페이스 형태로 정의해 놓았다. 위 예제보다 error를 사용하는 방법에 대한 좋은 글을 찾아보았다.  
[Go-에러 처리](http://golang.site/go/article/19-Go-%EC%97%90%EB%9F%AC%EC%B2%98%EB%A6%AC)  
[Go-error 예제](https://joinc.co.kr/w/man/12/golang/error)

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
    "math"
)

type ErrNegativeSqrt float64

func (e ErrNegativeSqrt) Error() string{
    return fmt.Sprintf("cannot Sqrt negative number: %f", e)
}

func Sqrt(f float64) (float64, error) {
    if f < 0 {
        return 0, ErrNegativeSqrt(f)
    }
    return math.Sqrt(f), nil
}

func main() {
    //fmt.Println(Sqrt(2))
    //fmt.Println(Sqrt(-2))
    if ans, err := Sqrt(2); err!=nil{
        fmt.Println(err)
    } else{
        fmt.Println(ans)
    }
    if ans, err := Sqrt(-2); err!=nil{
        fmt.Println(err)
    } else{
        fmt.Println(ans)
    }
}


```

Sqrt 메소드에 양수가 들어가면, `math.Sqrt(f)`로 값이 계산되어 출력된다. 그러나 음수가 들어가게 되면, error로 ErrNegativeSqrt 자료형이 들어가게 된다. 이 때, ErrNegativeSqrt는 error type에 대응할 Error 메소드를 가지고 있고, 이 Error 메소드가 작동하게 된다. 그리고, 이 결과 반환된 값이 nil, 즉 비어있지 않으면서 Error 메소드에서 return한 string이 출력되게 된다.

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

http 패키지를 제공하여 비교적 쉽게 웹 서버를 구축할 수 있다. http 요청이 들어오면 Hello!라는 글씨를 응답해 준다.

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
    "fmt"
    "net/http"
)

type String string

type Struct struct {
	Greeting string
	Punct    string
	Who      string
}

type k struct{

}

func (s String) ServeHTTP(w http.ResponseWriter,r *http.Request) {
    fmt.Fprint(w, s)
}

func (t *Struct) ServeHTTP(w http.ResponseWriter,r *http.Request) {
    fmt.Fprint(w, t.Greeting, t.Punct, t.Who)
}

func (str k) ServeHTTP(w http.ResponseWriter,r *http.Request) {
    fmt.Fprint(w, "Hello, World!")
}

func main() {
    // your http.Handle calls here
    http.Handle("/", k{})
    http.Handle("/string", String("I'm a frayed knot."))
    http.Handle("/struct", &Struct{"Hello", ":", "Gophers!"})
    http.ListenAndServe("localhost:4000", nil)
}

```

생각보다 웹 서버 구현이 어렵지 않았다. 우선, Listen되는 주소로 접속 시 해당 경로를 Handle한다. 그리고 http.Handle에서 값을 주면, ServeHTTP에서 값을 받아 처리한다.

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
    fmt.Println(m.Bounds()) //(0,0)-(100,100)
    fmt.Println(m.At(0, 0).RGBA())  //0 0 0 0
}

```

이미지를 처리하기 위해 image를 import시킨다.

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
    //"golang.org/x/tour/pic"
    "image"
    "image/color"
)

type Image struct{
    w int
	h int
}

func (img Image) ColorModel() color.Model {
    return color.RGBAModel
}

func (img Image) Bounds() image.Rectangle {
    return image.Rect(0, 0, img.w , img.h)
}

func (img Image) At(x, y int) color.Color {
    return color.RGBA{uint8(x), uint8(y), 255, 255}
}


func main() {
    m := Image{256,256}
    pic.ShowImage(m)
}


```

일단, 필수 함수에 대해 알아보기 위해 image에 있는 interface 항목을 살펴보자.

```go
type Image interface {
    // ColorModel returns the Image's color model.
    ColorModel() color.Model
    // Bounds returns the domain for which At can return non-zero color.
    // The bounds do not necessarily contain the point (0, 0).
    Bounds() Rectangle
    // At returns the color of the pixel at (x, y).
    // At(Bounds().Min.X, Bounds().Min.Y) returns the upper-left pixel of the grid.
    // At(Bounds().Max.X-1, Bounds().Max.Y-1) returns the lower-right one.
    At(x, y int) color.Color
}
```

위 3가지는 필수적으로 구현해야 한다는 것을 알 수 있다. 따라서, 저 3가지를 잘 보고 알맞게 구현하면 된다.

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

ROT-13은 알파벳을 13글자씩 밀어내고, z가 넘어가면 다시 a부터 시작하는 방식으로 순환하여 문자를 바꾼다. <해결중>

---

읽어주셔서 감사합니다!

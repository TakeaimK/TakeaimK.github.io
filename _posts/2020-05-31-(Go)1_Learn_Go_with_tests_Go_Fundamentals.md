---
layout: post
title: (Go) (Learn With Go Tests) 1. Go Fundamentals
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

> [Github Source Code - Learn Go with Tests](https://github.com/TakeaimK/Learn_Go_with_Tests){: target="\_blank"}

# Learn Go with Tests

Learn Go with Tests는 코드 테스트 기반으로 Golang을 학습할 수 있다.  
나는 테스트 기반으로 작업한다는 것이 매우 생소했다. 디버그라 함은 코드 중간에 콘솔 print 넣고 돌려보고, 잘 돌아가면 "잘 작동하네" 하고 말았던 것이 대부분이다.

그러나 이 Learn Go with Tests는 그 습관부터 바로잡는다. 일단, 기능보다 테스트 코드를 먼저 짠다(!). 이게 무슨 뜻이냐면, 두 수를 덧셈하는 프로그램을 만들고 싶다면

1. 일단 1과 2를 넣고, 3을 원하는 테스트 케이스를 짠 다음 실행시킨다. 당연히 아직 덧셈 기능을 가진 메소드가 없기 때문에 에러가 발생한다.
2. 그때서야 비로소 실제로 덧셈하는 기능을 가진 메소드를 작성하여 돌린다.
3. 이후, 덧셈 메소드에서 중복되는 부분은 메소드로 만들어 직관적이고 재사용 가능하도록 개선하는 등의 리팩토링을 거친다.  
   이제 위 과정을 마무리했으면 새로운 테스트 케이스를 추가한다. 3.5와 4.5를 더하는 케이스를 추가하면, 기존 메소드는 정수 덧셈에 맞춰 만들어졌기 때문에 에러가 발생한다. 그러면 실수에서 덧셈도 가능하게 만들고, 리팩토링한다. 이 과정을 반복하여 여러 테스트 케이스에 대응하는 모듈 or 프로그램을 작성한다.

이 과정이 매우 지루하고, 답답하고, 눈이 빠질 것 같이 아플 수도 있다. ~~제가 그랬습니다~~ 그러나 후반부로 갈수록 프로그램이 매우 복잡해지고, 왜 테스트 케이스가 필요한지 알 수 있게 된다. 따라서 본 글도 기본 문법보다 테스트를 돌릴 때 유용한 것 위주로 정리해 보았다.

다만, 모든 내용이 영문이다. 정말 좋은 내용이라 한국어판도 있었으면 좋겠다.

> [gotour - 영어](https://quii.gitbook.io/learn-go-with-tests/){: target="\_blank"}

---

## Hello, World

[Hello_world Final Code](https://github.com/TakeaimK/Learn_Go_with_Tests/tree/master/Go_Fundamentals/Hello_world)

### 핵심 내용

- 테스트 코드는 xxx_test.go로 작성이 관례
- 테스트 함수는 `Test`로 시작이 관례
- 테스트 함수는 `t *testing.T` 하나의 매개변수만 가짐
- 에러 발생 시 `t.Errorf("got %q want %q", got, want)`와 같이 작성
- 고정되는 문자열 상수 등은 `const englishHelloPrefix = "Hello, "`와 같이 작성
- 테스트 실행은 해당 경로의 터미널에서 `go test` 입력

---

## Integers

[Integers Final Code](https://github.com/TakeaimK/Learn_Go_with_Tests/tree/master/Go_Fundamentals/Integers)

### 핵심 내용

- `go test -v`로 Test function의 결과를 각각 볼 수 있음
- test.go에서 got, want 방식을 아래처럼 시도해 볼 수 있음. `// Output : 6` 제거 시 test되지 않음.

```go
func ExampleAdd() {
	sum := Add(1, 5)
	fmt.Println(sum)
	// Output: 6
}
```

- 코드 예제를 godoc에 추가해 볼 수 있으며, `godoc -http=:6060`로 실행하고 `http://localhost:6060/pkg/`로 접속하여 확인 가능

---

## Iteration

[Iteration Final Code](https://github.com/TakeaimK/Learn_Go_with_Tests/tree/master/Go_Fundamentals/Iteration)

### 핵심 내용

- `go test -bench=.`를 입력하여 테스트의 실행 시간을 벤치마크해 볼 수 있음 (Powershell : `go test -bench="."`)

---

## Arrays and slices

[Arrays and slices Final Code](https://github.com/TakeaimK/Learn_Go_with_Tests/tree/master/Go_Fundamentals/Arrays_and_slices)

### 핵심 내용

- `range` 문을 사용해 특정 배열이나 슬라이스의 항목을 순차적으로 꺼낼 수 있으며, 인덱스와 값 순서대로 넘어온다. 아래와 같이 `_`를 사용하여 값을 받지 않을 수 있다.

```go
func Sum(numbers [5]int) int {
    sum := 0
    for _, number := range numbers {
        sum += number
    }
    return sum
}
```

- `go test -cover`로 테스트 코드에 포함되지 않은 영역을 식별할 수 있음. 다만 100% 커버리지가 목표가 되어서는 안 됨.

---

## Struct, method and interfaces

[Struct, method and interfaces Final Code](https://github.com/TakeaimK/Learn_Go_with_Tests/tree/master/Go_Fundamentals/Struct_method_and_interfaces)

### 핵심 내용

- interface로 메소드의 입력 값과 반환 값의 타입을 명확하게 명시할 수 있음
- 구조체의 특정 영역에 대해 테스트하고자 할 때는 아래 코드에서 `go test -run TestArea/Rectangle`를 입력한다.

```go
func TestArea(t *testing.T) {

    areaTests := []struct {
        name    string
        shape   Shape
        hasArea float64
    }{
        {name: "Rectangle", shape: Rectangle{Width: 12, Height: 6}, hasArea: 72.0},
        {name: "Circle", shape: Circle{Radius: 10}, hasArea: 314.1592653589793},
        {name: "Triangle", shape: Triangle{Base: 12, Height: 6}, hasArea: 36.0},
    }

    for _, tt := range areaTests {
        // using tt.name from the case to use it as the `t.Run` test name
        t.Run(tt.name, func(t *testing.T) {
            got := tt.shape.Area()
            if got != tt.hasArea {
                t.Errorf("%#v got %g want %g", tt.shape, got, tt.hasArea)
            }
        })

    }

}
```

---

## Pointers & errors

[Pointers and errors Final Code](https://github.com/TakeaimK/Learn_Go_with_Tests/tree/master/Go_Fundamentals/Pointers_and_errors)

### 핵심 내용

- error는 `errors.New(string)`의 형태로 생성할 수 있음
- 에러 체크는 `go get -u github.com/kisielk/errcheck` 후 `errcheck .`로 실행한다.

---

읽어주셔서 감사합니다!

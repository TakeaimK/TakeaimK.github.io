---
layout: post
title: (Go) Context
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

괴제 전체 source code는 아래 링크에 있습니다.

> [Github Source Code - Pipeline](https://github.com/TakeaimK/Study_Goroutine_Channel){: target="\_blank"}

---

# Context?

- 일단, 저 단어는 "맥락, 문맥"이라는 의미를 가진다. 사전적 정의와 별개로, Context switching 등의 용어에도 사용될 만큼 처음 접하는 단어는 아니다.
- 컴퓨터공학에서 맥락이란, 어떤 프로그램의 흐름을 정상적으로 이어나갈 수 있도록 돕는 장치를 말한다.
- Golang에서 Context는 패키지 형태로 제공되며, 주로 Goroutine의 생명 주기를 제어하기 위해 사용한다. 앞서 이야기했지만, 고루틴은 종료될 때까지 가비지 컬렉션에서 건드리지 않는다. 즉, 직접 종료시켜 주어야 하는데, 이 때 컨텍스트를 활용하면 종료가 필요한 고루틴들을 한 번에 필요한 범위만큼 종료시킬 수 있다. 또한 타이머를 걸어 지정한 시간이 지나면 종료시킬 수도 있다.

---

## Context 패키지 살펴보기

![flow_chart](/assets/images/Go/Context/context_flow_chart.PNG)  

-type Context interface
```go
// A Context carries a deadline, cancelation signal, and request-scoped values
// across API boundaries. Its methods are safe for simultaneous use by multiple
// goroutines.
type Context interface {
    // Done returns a channel that is closed when this Context is canceled
    // or times out.
    Done() <-chan struct{}

    // Err indicates why this context was canceled, after the Done channel
    // is closed.
    Err() error

    // Deadline returns the time when this Context will be canceled, if any.
    Deadline() (deadline time.Time, ok bool)

    // Value returns the value associated with key or nil if none.
    Value(key interface{}) interface{}
}
```

- 컨텍스트 생성(종료 없는 컨텍스트) : `context.Background`
```go
func Background() Context

```
- 컨텍스트 값 추가 : `context.WithValue`
```go
func WithValue(parent Context, key, val interface{}) Context
```

- 컨텍스트 값 가져오기 : `Value`
```go
type Context interface {
	Value(key interface{}) interface{}
}
```

- 컨텍스트 취소 : `context.WithCancel`
```go
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
```

- 컨텍스트 취소 타이머 : `context.WithDeadline` or `context.WithTimeout`
```go
func WithDeadline(parent Context, d time.Time) (Context, CancelFunc)
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
```

---

## Context 예제 - 값 추가

### main.go
```go
// 컨텍스트 생성
ctx := context.Background()

// 컨텍스트에 값 추가
// context.WithValue 함수를 사용하여 새로운 컨텍스트를 생성함
ctx = context.WithValue(ctx, "user_A", currentUser)

// 함수 호출시 컨텍스트를 파라미터로 전달
authorizeFunc(ctx)
```

### authorizeFunc.go
```go
func myFunc(ctx context.Context) error {
	//User type이 있다고 가정
	var noWUser User

	// 컨텍스트에서 값을 가져옴
	if v := ctx.Value("user_A"); v != nil {
		// 타입 확인(type assertion)
		u, ok := v.(User)
		if !ok {
			return errors.New("Not authorized")
		}
		currentUser = u
	} else {    //만약 context에 값이 존재하지 않으면 nil return	
		return errors.New("Not authorized")
	}

	// nowUser를 사용

	return nil
}
```

---

## Context 예제 - 종료신호(Cancel)

 - 컨텍스트에 종료 신호를 보내어 만일 작업이 끝나기 전의 고루틴을 강제로 종료시켜야 하는 경우의 예제이다.

 ### main.go
 ```go
ctx, cancel := context.WithCancel(context.Background())

go func() {
	// 고루틴 강제 종료 상황 시
	if stop{
        cancel()
	}	
}()

// jobCount 만큼 여러개의 고루틴을 만들어 longFuncWithCtx 수행
var wg sync.WaitGroup
for i := 0; i < jobCount; i++ {
	wg.Add(1)

	go func() {
		defer wg.Done()
		result, err := longFuncWithCtx(ctx)		
		if err != nil {
			//
		}
	}()
}
wg.Wait()
 ```

 ### longFuncWithCtx.go
 ```go
 func longFuncWithCtx(ctx context.Context) (string, error) {
	done := make(chan string)

	go func() {
		done <- longFunc()
	}()

	select {
	case result := <-done:    //정상적인 종료
		return result, nil
	case <-ctx.Done():        //컨텍스트로부터 done 신호를 받은 경우
		return "Fail", ctx.Err()
	}
}
 ```

 ### longFunc.go
 ```go
 func longFunc() string {
	<-time.After(time.Second * 3) // long running job
	return "Success"
}
 ```
---

## Context 예제 - 예약 취소(Timeout & Deadline)

- 두 가지 방식이 있다. `context.WithDeadline`은 두 번째 인자로 `time.Time`이 있는데, 지정된 시간이 되면 컨텍스트에 취소 신호가 전달되고, `context.WithTimeout`을 사용하면 두 번째 인자로 `time.Duration`이 있고, 두 번째 인자로 받은 시간만큼이 지나면 취소 신호가 전달된다.
- `Deadline()` 메소드로 컨텍스트 취소 신호가 전달될 때까지 남은 시간을 확인할 수 있다.

```go
ctx, cancel := context.WithTimeout(context.Background(), maxDuration)

go func() {
	// 고루틴을 종료해야 할 상황이 되면 cancel 함수 실행
	cancel()
}()

start := time.Now()
result, err := longFuncWithCtx(ctx)
fmt.Printf("duration:%v result:%s\n", time.Since(start), result)
```

---

읽어주셔서 감사합니다!

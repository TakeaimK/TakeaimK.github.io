---
layout: post
title: (Go) Pipeline
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

괴제 전체 source code는 아래 링크에 있습니다.

> [Github Source Code - Pipeline](https://github.com/TakeaimK/Study_Goroutine_Channel){: target="\_blank"}

---

# Pipeline

[Go Blog - Pipeline](https://blog.golang.org/pipelines)

**"파이프라인"** 이라는 용어는 Computer Science를 공부해 본 적이 있다면 한번쯤 접해보았을 단어이다. 아래 그림처럼 CPU 등의 연산 장치에서 데이터를 처리할 때, 병렬로 여러 개의 명령어를 처리하여 속도를 향상시키는 기법이다.  
![CS-Pipeline](/assets/images/Go/Pipeline/CS_Pipeline.jpg)

Golang에서 파이프라인에 대한 명확한 정의는 없지만, 앞서 배운 채널 여러 개를 연결하며 각 단계는 goroutines 그룹으로 이루어져 있다.  
이게 무슨 말인고 하니, 파이프라인이라 불리는 것들의 특징은 다음과 같다.

> - 매개변수로 in채널을 받아 값을 수신
> - 채널에서 받은 값을 계산하여 새로운 값 생성
> - 새로 생성된 값을 out채널로 전송

위와 같은 순서로 돌아간다. "Talk is cheap. Show me the code"를 외치는 분들을 위해 코드로 예시를 들어본다.

```go
func gen(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func sq(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

func main() {
    // Set up the pipeline and consume the output.
    for n := range sq(sq(gen(2, 3))) {
        fmt.Println(n) // 16 then 81
    }
}
```

우선, 정수 배열을 차례대로 출력하는 `gen()`이라는 제네레이터에 수를 넣고, 제네레이터는 하나씩 수를 꺼내어 채널에 전송합니다. `sq()`에서 이 값을 받아 자기 자신을 곱하고, 이 과정을 한번 더 반복합니다.

---

읽어주셔서 감사합니다!

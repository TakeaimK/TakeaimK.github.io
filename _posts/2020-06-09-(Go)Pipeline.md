---
layout: post
title: (Go) Pipeline
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

괴제 전체 source code는 아래 링크에 있습니다.

> [Github Source Code - Pipeline](https://github.com/TakeaimK/Study_Goroutine_Channel/tree/master/pipeline){: target="\_blank"}

교육내용 예제 응용 코드는 하단에 있습니다.

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

## squaring_numbers

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

- 우선, 정수 배열을 차례대로 출력하는 `gen()`이라는 제네레이터에 수를 넣고, 제네레이터는 하나씩 수를 꺼내어 채널에 전송한다. `sq()`에서 이 값을 받아 자기 자신을 곱하고, 이 과정을 한번 더 반복한다.
- 즉, n에서는 `sq()`의 채널을 받게 되고, 세 번의 채널을 거쳐 돌아오는 값을 출력한다.

---

## Fan-out, fan-in

```
채널이 닫혀도 여러 함수가 동일한 채널에서 읽을 수 있고(Fan-out), 함수가 여러 입력에서 읽고 모든 입력이 닫히면 닫힌 단일 채널에 입력 채널을 다중화하여 모두 닫을 때까지 진행할 수 있다(Fan-in)
```

- ...라고 공식 블로그에서 설명하지만, 이게 도통 무슨 소리인지 모르겠어서 조금 더 검색해서 추가해 보았다.
- 쉽게 말하자면, 회전문이다. Fan-out은 특정 채널을 통해 Input이 들어왔을 때 여러 개의 goroutine을 생성해 task를 분산 처리하는 것이며, fan-in은 처리된 결과들을 내뱉는 채널들을 하나로 취합하는 `merge`과정을 거쳐 생성된 하나의 채널에서 output을 뽑아낸다.

![CS-Pipeline](/assets/images/Go/Pipeline/fan-out_fan-in.png)

- 아래 코드는 fan-in 예시이다. 두 채널에서 들어온 결과값을 취합하여 출력한다.

```go
func main() {
    in := gen(2, 3)

    // Distribute the sq work across two goroutines that both read from in.
    c1 := sq(in)
    c2 := sq(in)

    // Consume the merged output from c1 and c2.
    for n := range merge(c1, c2) {
        fmt.Println(n) // 4 then 9, or 9 then 4
    }
}
```

- 두 채널 중 먼저 입력이 들어오는 채널에 대해 n으로 값을 출력하는 `merge()` 코드를 살펴보자.

```go
func merge(cs ...<-chan int) <-chan int {
var wg sync.WaitGroup
out := make(chan int)

// Start an output goroutine for each input channel in cs.  output
// copies values from c to out until c is closed, then calls wg.Done.
output := func(c <-chan int) {
	for n := range c {
		out <- n
	}
	wg.Done()
}
wg.Add(len(cs))
for _, c := range cs {
	go output(c)
}

// Start a goroutine to close out once all the output goroutines are
// done.  This must start after the wg.Add call.
go func() {
	wg.Wait()
	close(out)
}()
return out
}
```

- `sync.WaitGroup()`은 모든 고루틴이 종료될 때까지 대기해야 할 때 사용한다.

> • func (wg *WaitGroup) Add(delta int): WaitGroup에 대기 중인 고루틴 개수 추가  
> • func (wg *WaitGroup) Done(): 대기 중인 고루틴의 수행이 종료되는 것을 알려줌  
> • func (wg \*WaitGroup) Wait(): 모든 고루틴이 종료될 때까지 대기

- 즉, `Done()`을 수행하면 `Wait()` 부분에서 기다리다 종료시킨다.

---

## Stopping short

- 파이프라인에는 다음과 같은 규칙이 있다.

> 모든 송신이 완료되면 출력 채널을 닫는다  
> 채널이 닫혀도 입력 채널에서는 값을 계속 수신

- 만약, goroutine에서 생성된 값을 아직 출력 채널에 전부 보내지 않은 상태에서 수신 측이 return한다면, 나머지 값은 보내지지 못하고 무한정 대기한다. 이 자원은 가비지 컬렉터가 회수하지 않는다. goroutine 스택의 Heap 참조는 가비지 컬렉션이 건들지 않기 때문이다.

```go
 // Consume the first value from the output.
    out := merge(c1, c2)
    fmt.Println(<-out) // 4 or 9
    return
    // Since we didn't receive the second value from out,
    // one of the output goroutines is hung attempting to send it.
}
```

- 채널에 버퍼를 부여하여 goroutine으로 매번 송신 채널에서 받을 때마다 전송하는 방법 대신 송신 채널의 크기를 채널에 들어오는 입력 값의 크기와 동일하게 버퍼를 부여한 후 전부 넣고 하나씩 꺼내서 쓸 수 있도록 만들 수 있다.

```go
func gen(nums ...int) <-chan int {
    out := make(chan int, len(nums))
    for _, n := range nums {
        out <- n
    }
    close(out)
    return out
}
```

---

## Explicit cancellation

- 위 상황에서 모든 데이터를 전송하지 않고 수신 측이 종료한다면, 메모리 자원이 회수되지 못한다. 이런 일이 발생하지 않도록 goroutine을 명시적으로 종료시켜 나머지 자원이 모두 회수될 수 있도록 해야 한다.

```go
func gen(nums ...int) <-chan int {
	out := make(chan int, len(nums))
	for _, n := range nums {
		out <- n
	}
	close(out)
	return out
}

func sq(done <- chan struct{},in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			select {
			case out <- n * n:
			case <-done:
				return
			}
		}
	}()
	return out
}

func merge(done <-chan struct{}, cs ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)

	// Start an output goroutine for each input channel in cs.  output
	// copies values from c to out until c is closed or it receives a value
	// from done, then output calls wg.Done.
	output := func(c <-chan int) {
		defer wg.Done()
		for n := range c {
			select {
			case out <- n:
			case <-done:
				return
			}
		}
		wg.Done()
	}
	wg.Add(len(cs))
	for _, c := range cs {
		go output(c)
	}

	// Start a goroutine to close out once all the output goroutines are
	// done.  This must start after the wg.Add call.
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

func main() {
	done := make(chan struct{})
	defer close(done)

	in := gen(2, 3)

	// Distribute the sq work across two goroutines that both read from in.
	c1 := sq(done, in)
	c2 := sq(done, in)

	// Consume the first value from output.
	out := merge(done, c1, c2)
	fmt.Println(<-out) // 4 or 9

}

```

- 파이프라인 구성의 기본은 아래와 같다.

> 모든 송신이 완료되면 출력 채널을 닫는다  
> 채널이 닫히거나 발신자가 차단 해제될 때까지 입력 채널에서는 값을 계속 수신

- 파이프라인은 전송되는 모든 값에 대해 충분한 버퍼가 있는지 확인하거나 수신자가 채널을 포기할 수 있을 때 발신자에게 명시적으로 신호를 보내 발신자의 차단을 해제한다.

---

## Digesting a tree

- 디렉토리의 md5 file checksum을 출력하는 프로그램을 제작한다. 먼저, 스레드를 사용하지 않는 `serial.go` 코드를 작성한다.

```go
// MD5All reads all the files in the file tree rooted at root and returns a map
// from file path to the MD5 sum of the file's contents.  If the directory walk
// fails or any read operation fails, MD5All returns an error.
func MD5All(root string) (map[string][md5.Size]byte, error) {
   m := make(map[string][md5.Size]byte)
   err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
       if err != nil {
           return err
       }
       if !info.Mode().IsRegular() {
           return nil
       }
       data, err := ioutil.ReadFile(path)
       if err != nil {
           return err
       }
       m[path] = md5.Sum(data)
       return nil
   })
   if err != nil {
       return nil, err
   }
   return m, nil
}

func main() {
   // Calculate the MD5 sum of all files under the specified directory,
   // then print the results sorted by path name.
   m, err := MD5All(os.Args[1])
   if err != nil {
       fmt.Println(err)
       return
   }
   var paths []string
   for path := range m {
       paths = append(paths, path)
   }
   sort.Strings(paths)
   for _, path := range paths {
       fmt.Printf("%x  %s\n", m[path], path)
   }
}
```

- 다음으로, 두 단계의 파이프라인을 사용하는 `parallel.go`를 작성한다.
- 우선, 파일경로, sum, 에러를 가지는 구조체를 만들고, `MD5ALL()`에서 `sumFiles()`을 호출한다. 이곳에서 스레드를 생성하여 파이프라인을 구성한다. `filepath.Walk()` 함수는 첫 번째 매개변수로 전달된 path의 파일과 디렉터리를 모두 순회하고, 두 번째 매개변수로 전달된 함수를 수행한다. 이렇게 순회한 경로를 기반으로, `md5.Sum(data)`를 돌려 채널로 전송한다. 그러면 다시 `MD5ALL()`에서 값을 받아 처리하는 방식이다.

```go
package main

import (
	"crypto/md5"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"sort"
	"sync"
)

type result struct {
	path string
	sum  [md5.Size]byte
	err  error
}

func sumFiles(done <-chan struct{}, root string) (<-chan result, <-chan error) {
	// For each regular file, start a goroutine that sums the file and sends
	// the result on c.  Send the result of the walk on errc.
	c := make(chan result)
	errc := make(chan error, 1)
	go func() {
		var wg sync.WaitGroup
		err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.Mode().IsRegular() {
				return nil
			}
			wg.Add(1)
			go func() {
				data, err := ioutil.ReadFile(path)
				select {
				case c <- result{path, md5.Sum(data), err}:
				case <-done:
				}
				wg.Done()
			}()
			// Abort the walk if done is closed.
			select {
			case <-done:
				return errors.New("walk canceled")
			default:
				return nil
			}
		})
		// Walk has returned, so all calls to wg.Add are done.  Start a
		// goroutine to close c once all the sends are done.
		go func() {
			wg.Wait()
			close(c)
		}()
		// No select needed here, since errc is buffered.
		errc <- err
	}()
	return c, errc
}

func MD5All(root string) (map[string][md5.Size]byte, error) {
	// MD5All closes the done channel when it returns; it may do so before
	// receiving all the values from c and errc.
	done := make(chan struct{})
	defer close(done)

	c, errc := sumFiles(done, root)

	m := make(map[string][md5.Size]byte)
	for r := range c {
		if r.err != nil {
			return nil, r.err
		}
		m[r.path] = r.sum
	}
	if err := <-errc; err != nil {
		return nil, err
	}
	return m, nil
}

func main() {
	// Calculate the MD5 sum of all files under the specified directory,
	// then print the results sorted by path name.
	m, err := MD5All(os.Args[1])
	if err != nil {
		fmt.Println(err)
		return
	}
	var paths []string
	for path := range m {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	for _, path := range paths {
		fmt.Printf("%x  %s\n", m[path], path)
	}
}
```

- 위 방식에서, 파일마다 고루틴을 생성하여 처리하는 방식을 사용한다. 만일, 파일 각각의 용량이 매우 큰 경우, 컴퓨터의 메모리보다 더 큰 파일을 로드해야 하는 경우가 발생할 수 있다. 이런 경우를 해결하기 위해, `bounded.go`를 작성해 보자.
- 파이프라인에서 워킹 트리, 파일 읽기 및 digests, digests 수집의 세 가지 단계를 거친다.

```go
// walkFiles starts a goroutine to walk the directory tree at root and send the
// path of each regular file on the string channel.  It sends the result of the
// walk on the error channel.  If done is closed, walkFiles abandons its work.
func walkFiles(done <-chan struct{}, root string) (<-chan string, <-chan error) {
	paths := make(chan string)
	errc := make(chan error, 1)
	go func() { // HL
		// Close the paths channel after Walk returns.
		defer close(paths) // HL
		// No select needed for this send, since errc is buffered.
		errc <- filepath.Walk(root, func(path string, info os.FileInfo, err error) error { // HL
			if err != nil {
				return err
			}
			if !info.Mode().IsRegular() {
				return nil
			}
			select {
			case paths <- path: // HL
			case <-done: // HL
				return errors.New("walk canceled")
			}
			return nil
		})
	}()
	return paths, errc
}

// A result is the product of reading and summing a file using MD5.
type result struct {
	path string
	sum  [md5.Size]byte
	err  error
}

// digester reads path names from paths and sends digests of the corresponding
// files on c until either paths or done is closed.
func digester(done <-chan struct{}, paths <-chan string, c chan<- result) {
	for path := range paths { // HLpaths
		data, err := ioutil.ReadFile(path)
		select {
		case c <- result{path, md5.Sum(data), err}:
		case <-done:
			return
		}
	}
}

// MD5All reads all the files in the file tree rooted at root and returns a map
// from file path to the MD5 sum of the file's contents.  If the directory walk
// fails or any read operation fails, MD5All returns an error.  In that case,
// MD5All does not wait for inflight read operations to complete.
func MD5All(root string) (map[string][md5.Size]byte, error) {
	// MD5All closes the done channel when it returns; it may do so before
	// receiving all the values from c and errc.
	done := make(chan struct{})
	defer close(done)

	paths, errc := walkFiles(done, root)

	// Start a fixed number of goroutines to read and digest files.
	c := make(chan result) // HLc
	var wg sync.WaitGroup
	const numDigesters = 20
	wg.Add(numDigesters)
	for i := 0; i < numDigesters; i++ {
		go func() {
			digester(done, paths, c) // HLc
			wg.Done()
		}()
	}
	go func() {
		wg.Wait()
		close(c) // HLc
	}()
	// End of pipeline. OMIT

	m := make(map[string][md5.Size]byte)
	for r := range c {
		if r.err != nil {
			return nil, r.err
		}
		m[r.path] = r.sum
	}
	// Check whether the Walk failed.
	if err := <-errc; err != nil { // HLerrc
		return nil, err
	}
	return m, nil
}

func main() {
	// Calculate the MD5 sum of all files under the specified directory,
	// then print the results sorted by path name.
	m, err := MD5All(os.Args[1])
	if err != nil {
		fmt.Println(err)
		return
	}
	var paths []string
	for path := range m {
		paths = append(paths, path)
	}
	sort.Strings(paths)
	for _, path := range paths {
		fmt.Printf("%x  %s\n", m[path], path)
	}
}
```

---

# Pipeline 교육 코드 응용

## 원본 코드

```go
package main

import "fmt"

func gen() <-chan int {
	next := 0
	intStream := make(chan int)
	go func() {
		defer close(intStream)
		for {
			next++
			intStream <- next
		}
	}()
	return intStream
}

func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n * n
		}
		close(out)
	}()
	return out
}

func addone(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n + 1
		}
		close(out)
	}()
	return out
}

func main() {
	n := 0
	for s := range square(square(addone(square(gen())))) {
		if n == 5 {
			break
		}
		fmt.Println(s)
		n++
	}
}

```

## 응용 코드

- goroutine을 종료시켜 자원을 회수할 수 있도록 각 goroutine에 done 채널을 전송
- done과 out 두 개의 채널을 받는 경우 range를 사용할 수 없어서 가장 마지막에 out만 출력시키는 `finalPipe()`을 추가

```go
package main

import (
	"fmt"
)

func gen(done <-chan struct{}) (<-chan struct{}, <-chan int) {
	next := 0
	intStream := make(chan int)

	go func() {
		defer close(intStream)
		for {
			select {
			case <-done:
				return
			default:
				next++
				intStream <- next
			}
		}
	}()
	return done, intStream
}

func square(done <-chan struct{}, in <-chan int) (<-chan struct{}, <-chan int) {
	out := make(chan int)

	go func() {
		for {
			select {
			case n := <-in:
				out <- n * n
			case <-done:
				close(out)
				return
			}

		}
	}()
	return done, out
}

func addone(done <-chan struct{}, in <-chan int) (<-chan struct{}, <-chan int) {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n + 1
		}
		close(out)
	}()
	return done, out
}

func finalPipe(done <-chan struct{}, in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for {
			select {
			case n := <-in:
				out <- n
			case <-done:
				fmt.Println("done!")
				close(out)
				return
			}
		}
	}()
	return out
}

func main() {
	done := make(chan struct{})
	defer close(done)

	for n := range finalPipe(addone(square(gen(done)))) {
		fmt.Println(n)
		if n > 100 {
			break
		}
	}
}

```

---

읽어주셔서 감사합니다!

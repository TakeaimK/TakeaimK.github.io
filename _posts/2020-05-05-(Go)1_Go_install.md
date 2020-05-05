---
layout: post
title: (Go) 1. Go 설치 (Windows, Linux)
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

---

# Go 설치 - Windows

다음 링크에서 최신 버전의 GO를 다운로드한다. 확장자는 `.msi` 이다.

> [GoLang 공식 다운로드](https://golang.org/dl/)

Windows에서 Go는 변경사항이 없다면 C:\go 폴더에 설치되며, MSI가 C:\go\bin을 PATH 환경변수를 알아서 추가한다.  
설치되었다면, 메모장 or Notepad++ or VSCode를 열고 다음 코드를 작성한다.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}

```

위 내용을 `test.go` 라는 이름과 확장자로 저장하고, 해당 경로에 Powershell을 열어준다. 쉽게 여는 방법은 열고자 하는 경로로 윈도우 탐색기로 들어간 다음 빈 공간에 `Shift + 마우스 우클릭` 후 `여기에 Powershell 열기`를 눌러준다. 이후 다음 명령을 입력한다.

```powershell
go run test.go
```

결과창에 Hello, World! 라고 출력되면 정상이다.

---

# Go 설치 - Linux (Ubuntu)

Windows 설치보다 조금 더 복잡한 과정이 있다. 여기서는 GUI환경과 Console 환경 두 가지 설치법에 대해 알아본다.

## GUI 환경(Xwindow)에서 작업

1. 다음 링크로 들어간 다음 Linux 버전 설치파일을 다운받는다. 확장자는 `.tar.gz` 이다.

> [GoLang 공식 다운로드](https://golang.org/dl/)

2. 다운받았다면, 압축파일을 눌러 `/usr/local` 경로에 압축을 풀어준다. 단, 여기서 root 계정이 아닌 경우 다음과 같은 권한 없음 창이 나온다.  
   ![gui_permission_denied](/assets/images/Go/1_install/gui_1.png)  
   만약 위의 창과 같은 오류가 발생할 경우, 아래 Console 진행에서 2번부터 진행한다.

3. HOME 디렉토리에 들어간 다음, 숨김파일 보기 옵션을 킨 다음 `.bashrc` or `.profile` 파일을 열고, 가장 마지막에 다음 줄을 추가한다.

```
PATH=$PATH:/usr/local/go/bin
```

![gui_PATH](/assets/images/Go/1_install/gui_2.png)

이후 재부팅한다.

## Console 환경에서 작업

1. 현재 글 작성 시점에서 최신 버전의 go(1.14.2)를 다운받는다.  
   다음 명령을 shell에 입력한다. 본 명령은 wget을 사용하였다.

> wget https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz

2. 다운로드 폴더로 이동(`cd download` or `cd 다운로드`)한 다음 아래 명령으로 `/usr/local` 경로에 압축을 풀어준다.

> sudo tar -C /usr/local -xzf go1.14.2.linux-amd64.tar.gz

3. 홈 디렉토리로 이동(`cd ./`)한 다음, vi나 nano 같은 편집기로 `.bashrc` 파일을 열어 다음 구문을 추가한다.

```
PATH=$PATH:/usr/local/go/bin
```

4. 재부팅하거나 다음 명령을 입력한다.

```
source ~/.bashrc
```

5. 다음 명령으로 경로 추가가 잘 되었는지 확인한다.

```
echo $PATH
```

가장 마지막에 위에서 추가한 `/usr/local/go/bin`이 있다면 성공이다.

## 설치 확인

임의 경로로 이동 후 vi(vim) or nano or GUI 텍스트 편집기로 다음 코드를 작성하고 `test.go`라는 이름으로 저장한다.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}

```

이후 Console에서 다음 명령을 수행한다.

```bash
go run test.go
```

![console_hello_world](/assets/images/Go/1_install/console_1.png)

위와 같이 출력되면 성공이다!

---

> 참고 사이트
> http://golang.site/go/article/2-Go-%EC%84%A4%EC%B9%98%EC%99%80-Go-%ED%8E%B8%EC%A7%91%EA%B8%B0-%EC%86%8C%EA%B0%9C  
> https://woongheelee.com/entry/%EC%9A%B0%EB%B6%84%ED%88%AC%EC%97%90%EC%84%9C-path-%EC%84%A4%EC%A0%95%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95%EC%95%84%EB%A7%88-%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%9D%BC%EB%B0%98%EC%A0%81%EC%9D%B8-%EB%B0%A9%EB%B2%95

읽어주셔서 감사합니다.

---
layout: post
title: (Go) 0. Go?
categories:
  - Language-Go
---

**본 글은 Kakao Enterprise 예비인턴 GOLang 교육내용 및 자습/과제를 정리한 내용입니다.**

---

# Go?

![go_마스코트](/assets/images/Go/0_preview/go.png)

Go는 컴파일 언어로, 2009년에 발표된 언어다. 다른 주요 언어들에 비해 상당히 늦은 출발(C++ : 1979, Java : 1995, Python : 1991)이지만, TIOBE 선정 2020년 5월 기준 검색어 점유율 상위 12위를 차지하고 있다. (TIOBE 순위는 [이곳](https://www.tiobe.com/tiobe-index/)에서 확인할 수 있다.)  
타 언어에 비해 신생 언어임에도 이렇게 인기가 있는 이유는 **단순함(simplicity)과 실용성(pragmatism)**을 지향하는 언어로 설계되었기 때문이다.

## Go의 특징

- C++ 등의 언어에 비해 단순함
- 컴파일 속도가 빠름
- 가비지 컬렉션 제공으로 메모리 할당 및 해제 자동화
- keyword가 25개밖에 없음

  |:---:|:---:|:---:|:---:|:---:|
  |break |default |func |interface |select |
  |case |defer |go ||map |struct |
  |chan |else |goto |package |switch |
  |const |fallthrough |if |range |type |
  |continue |for |import |return |var |

- 클래스와 객체 대신 구조체와 메소드를 각각 정의하여 사용
- 대문자로 시작하면 Public, 소문자로 시작하면 private 역할을 수행
- 공식적으로 상속을 지원하지 않음
- 예외 대신 error타입 사용
- 동시성 프로그래밍(다른 함수를 쓰레드와 비슷하게 동시에 작동)이 가능
- 멀티코어 환경 지원
- 웹 프로그래밍에 친화적(net/http)
- Docker, Kubernetes 등의 컨테이너 기반 가상화 도구 제작에 사용
- 문서화 도구 제공

## GO!

위와 같은 특징으로 인해 Go는 급성장할 수 있었다. Go의 특징을 노래로 표현한 영상이 있다. [이곳](https://youtu.be/LJvEIjRBSDA)에서 들어볼 수 있다. 한글 번역 가사는 [이곳](<https://namu.wiki/w/Go(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)#s-7>)에서 볼 수 있다.

사실 위 특징 말고도 너무나도 많은 특징이 있지만 자세히 서술하기에는 너무 많아서 이정도로 줄인다.  
조금 더 자세히 알고 싶다면 아래 링크를 참조해 보자.

> [Golang.org](https://golang.org/)  
> [Go - 위키백과](<https://ko.wikipedia.org/wiki/Go_(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D_%EC%96%B8%EC%96%B4)>)  
> [Go의 주요 특징 - Golang Korean Community](https://golangkorea.github.io/post/go-start/feature/)  
> [Golang 개요 - sncap Style](https://sncap.tistory.com/878)

---

읽어주셔서 감사합니다.

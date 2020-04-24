---
layout: post
title: (Docker) 1. 도커 개념과 설치(Windows)
categories:
  - Docker
---

# Docker?

Docker. 도커는 컨테이너 기반의 오픈소스 가상화 플랫폼이다. 즉, 프로세스들이 각자의 공간(컨테이너)에서 작동할 수 있도록 가상화된 환경을 제공한다...지만 이렇게 말해서는 나도 이해 못 하겠다. 조금 더 쉽게 설명해 보자.  
우선, "컨테이너"에 대해 알아보자. 흔히 서버단에서 여러 프로그램을 돌리는 방법으로 가상 머신(VM)을 사용한다. 즉, 하나의 하드웨어 위에서 돌아가는 VM을 여러 개 놓고, VM마다 OS를 설치 후 그 위에 프로그램을 설치하여 각 프로그램마다 충돌이 발생할 가능성을 최대한 줄이는 방법이다. 그러나 이 방법은 VM마다 OS가 작동되므로, HW에 많은 오버헤드가 발생하는 것은 물론이고, VM의 성능도 덩달아 떨어지면서, 저장 공간도 VM의 수만큼 OS가 설치되므로 꽤나 무거운 작업이 된다.  
![VM_vs_docker](/assets/images/Docker/1_docker_install/vm-vs-docker.png)  
그래서 위 문제를 해결하기 위해 나온 것이 도커이다. 도커는 HW에서 에뮬레이션하는 방식이 아니라 OS커널을 공유하여 도커 엔진에서 프로세스를 실행하기만 하면 된다. 즉, VM마다 있던 OS를 줄일 수 있으면서, 프로세스끼리 각자 독립적으로 도커 엔진 위에서 돌아갈 수 있다. 즉, 매우매우매우 가벼워진다는 장점이 있다.  
조금 더 잘 설명하면서 자세히 알아보고자 한다면 다음 링크를 참조해 보면 좋다.
> [초보를 위한 도커 안내서 - 도커란 무엇인가? ](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html)  
> [도커와 도커 컨테이너의 이해 - ITWorld](http://www.itworld.co.kr/news/110748) 
> [도커 컨테이너는 가상머신인가요? 프로세스인가요? - 44BITS](https://www.44bits.io/ko/post/is-docker-container-a-virtual-machine-or-a-process)  

---

# Docker 설치(Windows)

설치에 앞서, 아래의 도커 공식문서 사이트를 참고하였다.  
> [Docker Document](https://docs.docker.com/)

기본적으로 도커는 리눅스 커널을 공유하여 사용하기 때문에, macOS, Windows에서는 Docker Desktop을 사용하게 된다. 즉, 매우 가벼운 리눅스를 가상머신에 올린 뒤 컨테이너를 구동하는 방식을 사용한다. 필자는 윈도우 환경에서 설치를 진행해 보려고 한다.  

### 0. 설치 전 환경 설정
 - Windows 10 64 비트 버전 Pro, Enterprise 또는 Education 버전(빌드 15063 이상) : 확인 방법은 시작버튼 옆의 검색창에 `winver` 라고 입력한 뒤 나오는 창을 확인한다.
![winver](/assets/images/Docker/1_docker_install/winver.PNG)  
 - 만일 윈도우7이거나 ~~업그레이드가 시급~~ 윈도우10 Home 버전인 경우, [이곳](https://docs.docker.com/toolbox/toolbox_install_windows/) 링크에 있는 설명대로 Docker Toolbox를 설치한다.  
 - Hyper-V 및 컨테이너 Windows 기능이 활성화 : 역시 같은 검색창에 `windows 기능 켜기` 라고 검색한 후, Hyper-V를 체크해 주고, 하라는 대로 설치한다. 설치 후 재부팅이 필요하다.  
![Hyper-V](/assets/images/Docker/1_docker_install/hyper.PNG)  

### 1. 다운로드 및 설치

 - 아래 링크에 접속해서 설치파일을 다운로드 받는다.
> https://hub.docker.com/editions/community/docker-ce-desktop-windows/  

 - 이후 설치파일을 눌러 설치하되, 가능한 체크박스는 모두 체크해 주는 것이 좋다. ~~적어도 이 글 작성 시점에서 애드웨어는 없다~~  
![install](/assets/images/Docker/1_docker_install/install.PNG)  

 - 설치 완료 후 로그아웃되니 다른 파일은 모두 잘 저장해 두자.

### 2. 회원가입

 - 위 과정을 거친 후 윈도우에 로그인하면 다음과 같은 창을 볼 수 있다.
![login](/assets/images/Docker/1_docker_install/login.PNG)  
 - 아래 링크로 들어가 회원가입을 한다.
> https://hub.docker.com/  
 - 회원가입 중간에 Plan이 있는데, 사정에 맞는 플랜을 골라준다.
 - 이메일 인증까지 마치면 다시 도커 데스크톱으로 돌아와 로그인하면, 다음과 같은 창이 나온다.
![docker_desktop1](/assets/images/Docker/1_docker_install/docker_desktop_1.PNG)  

 - 여기까지 무사히 왔다면 기본 설치는 끝났다! CLI로 설치를 확인하고 싶다면, cmd를 켜고 다음과 같이 입력해 본다.
 ```docker version```
 ![docker_version](/assets/images/Docker/1_docker_install/docker_version.PNG)  

 ---  

 다음에는 도커에서 이미지를 받아 컨테이너를 실행해 보도록 하겠습니다.  
 읽어주셔서 감사합니다.



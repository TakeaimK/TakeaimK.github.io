---
layout: post
title: (Docker) 2. 도커 컨테이너 구동
categories:
  - Docker
---

# Docker에서 제공하는 간단한 예제

지난 시간에 도커 데스크톱을 설치했다면, 이제 간단한 예제를 돌려 봄으로서 설치가 제대로 되었는지, 어떻게 돌리는지 실습해 보자.  

우선, 다음 코드를 cmd나 powershell을 켜고 입력해 보자.  

```powershell
git clone https://github.com/docker/doodle.git
```  

위 코드는 git이 설치되어 있어야 작동한다. git은 다음 링크에서 설치할 수 있다.
> [Git 설치하기](https://git-scm.com/downloads)

이후 git에서 무언가 clone해온다. 이제 다음 코드를 입력해 보자.  

```powershell
cd doodle\cheers2019
docker build -t (your_nickname)/cheers2019 .
```
**(your_nickname) 자리에는 Docker Hub의 Nickname을 넣어주자.**

![Docker_sample](/assets/images/Docker/2_docker_container/sample_1.PNG)  

clone해온 파일의 cheers2019로 이동 후, docker로 무언가를 build한다.  
즉, 이 과정이 컨테이너에 핵심이 될 이미지를 만드는 과정이다.  
두 번째 명령어인 build를 차근차근 살펴보면, 다음과 같은 구조를 가진다.  

```dockerfile
docker build [OPTIONS] PATH | URL | -
```

> __옵션 설명__  
> -t : 이미지에 이름을 부여

맨 뒤의 `.`은 현재 경로를 의미한다.  

이제 이미지를 build했으면, 위에서 제작한 이미지로 컨테이너를 돌려 보자.

```dockerfile
docker run -it --rm (your_nickname)/cheers2019
```
> __옵션 설명__
> -i : 상호 입출력
> -t : tty를 활성화하여 bash 쉘을 사용
> --rm : 컨테이너 종료 시 자동으로 컨테이너 삭제 

![Docker_sample2](/assets/images/Docker/2_docker_container/sample_2.PNG)  
~~커엽~~  
고래가 움직이는 아스키 아트를 볼 수 있다.  
그런데 여기서 궁금증이 생긴다, 단지 이미지만 만들고, run을 돌렸는데 알아서 컨테이너를 만들고, 만든 컨테이너를 실행하며, 실행된 컨테이너로 들어가 화면을 띄운다. run이라는 명령어가 많은 과정을 함축하고 있다는 것을 알 수 있다.  
위의 run 명령은 다음 세 줄의 명령을 한 번에 실행시킨 것이다.(rm 제외)  

```dockerfile
docker create -i -t --name (container_name) (your_nickname)/cheers2019
docker start (container_name)
docker attach (container_name)
```
esc를 눌러 나오게 되면 위 --rm 옵션 덕에 자동으로 컨테이너가 삭제된다. 만약 --rm 옵션을 하지 않는다면 컨테이너가 남게 되므로 다음과 같이 수동으로 컨테이너를 삭제시켜 줘야 한다.  

```dockerfile
docker ps -a
(name 확인)
docker rm (확인한 name)
```

추가적인 docker 명령어 reference는 다음 사이트를 참고하자.  
> [docker document - run](https://docs.docker.com/engine/reference/run/)  

이 이미지를 이제 도커 hub에 올려 보자.

```dockerfile
docker login
docker push takeaim/cheers2019
```

이제 본인의 docker hub에 올라간 테스트 컨테이너를 볼 수 있다. 만약 docker hub에 올린 이미지를 가져오고자 한다면 다음 명령어를 사용한다.  
```dockerfile
docker pull (image_name)
```

---

# docker hub에서 이미지 다운 및 실행

이제 실제 docker hub에 공유되고 여러 분야에서 사용되는 이미지를 받아서 실행해 보도록 하자.  
> [docker hub - container](https://hub.docker.com/search?q=&type=image)  

위 사이트에서 이미지를 고를 수 있다. 여기서는 두 가지 이미지를 받아보려고 한다.  

## Hello World 이미지 실행

첫 번째로, 프로그래밍을 할 때 가장 먼저 실행해 보는 Hello World를 실행해 보자. 
> https://hub.docker.com/_/hello-world  
터미널에 다음과 같이 입력한다.

```dockerfile
docker pull hello-world
docker run hello-world
```
![Docker_hello_world](/assets/images/Docker/2_docker_container/hello_world.PNG)  

위와 같은 창이 나오면 정상적으로 실행되어 출력 후 종료되었다.

## Ubuntu 이미지 실행
Docker는 본래 운영체제 전체가 시뮬레이션이 되는게 아니다.  
서비스를 제공하는 프로세스들와 필요로 하는 라이브러리가 함께 격리되어 실행된다. 이 점에서 Virtual Machine과의 차이점이다.  
하지만 Docker에서도 리눅스 등의 OS를 돌릴 수 있고, Shell로 명령도 가능하며, 심지어 공식 이미지를 제공한다. 아래 명령을 따라가면, bash shell을 만날 수 있다.

```dockerfile
docker pull ubuntu
docker run -it ubuntu
```

물론 이름을 지정하여 컨테이너를 생성하고 싶다면 위 두 번째 명령을 다음과 같이 바꿔주면 된다.  

```dockerfile
docker run -it --name ubuntu_test ubuntu
```
위 명령이 제대로 실행되었다면, 컨테이너 생성과 동시에 들어가서 root 계정으로 로그인된 우분투의 bash shell을 볼 수 있다. 정말로 우분투가 맞는지 vim 에디터를 설치해 보자.  

```dockerfile
apt-get update
apt-get upgrade
apt-get install vim
<After install>
vim
```

![vim](/assets/images/Docker/2_docker_container/vim.PNG)  

정말로 작동된다! 간단한 텍스트를 입력하고 저장하여 실제로 파일이 생성되는지 확인해 보자.~~(리눅스 배우는 시간)~~  

> `i` Key 누르기 > 내용 작성 > `esc` Key 누르기 > `w <filename>` 입력 후 Enter > `q` 입력 후 Enter  

![vim](/assets/images/Docker/2_docker_container/vim_edit.PNG)  

vim 에디터를 빠져나왔다면 `ls` 명령으로 확인해 보자.

![ls](/assets/images/Docker/2_docker_container/ls.PNG)  

정상적으로 파일이 저장되어 있는 모습을 볼 수 있다.  
콘솔 창을 닫더라도 아래처럼 윈도우 도커 GUI에서 잘 돌아가고 있음을 확인할 수도 있다.  

![docker_gui](/assets/images/Docker/2_docker_container/docker_gui.PNG)  



---  
 
 읽어주셔서 감사합니다.



---
layout: post
title: 1. React Native 설치 (Windows based)
categories:
  - React-native
---

# React-Native 개요

![React_logo](/assets/images/React_native/react.png)

프론트엔드 개발, 즉 UI를 제작하는 React의 문법으로 iOS, Android 등에서 구동할 수 있는 크로스플랫폼 앱을 만들 수 있습니다. 자세한 내용은 다음 사이트를 참고하길 바랍니다.  

> [React - 나무위키](https://namu.wiki/w/React(%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC))  
> [React-native 공식 문서(영문)](https://facebook.github.io/react-native/docs/getting-started)  

**본 글은 React Native _ver 0.61_ 을 바탕으로 작성되었습니다.**  

**Expo가 아닌 순수 React Native 기반의 앱 제작 목적으로 만들어졌습니다.**

---

## 1. Package 설치  

먼저, Windows 기반에서 React Native를 설치해 보겠습니다.  
Chocolatey는 Windows 기반의 패키지 관리자입니다. 이곳에서 필요한 패키지를 내려받겠습니다. 먼저 Chocolatey을 설치하겠습니다.  
다음 링크를 눌러 아래 사진의 사이트에 접속합니다.  

[Chocolatey - Package manager](https://chocolatey.org/)  

![React_Native_install(1)](/assets/images/React_native/React_native_install/install(1).png)

우측 상단의 install now를 눌러 다운로드 받고 설치합니다.  

저희가 설치하고자 하는 패키지는 nodejs, python2, jdk8 이렇게 3개입니다. 설치하는 방법은 다음과 같습니다.  

### Windows Powershell(관리자) 열기

- Windows10 기준 우하단 검색창에 powershell을 입력
- "관리자로 실행" 클릭
![React_Native_install(2)](/assets/images/React_native/React_native_install/install(2).png)


### 명령 창(Command Window)

- Matlab 명령어를 직접 입력하여 실행한다.

### 작업 공간(Workspace)

- 현재 Matlab에서 사용되고 있는 변수에 대한 값과 정보를 보여준다.
- 더블 클릭하여 해당 변수의 값과 데이터형 알 수 있으며, 엑셀과 같은 구조에서 수정도 가능하다.

### 명령 내역(Command History)

- Matlab을 사용하는 동안 실행한 모든 명령어들의 목록을 보여준다.

### Matlab 인터페이스의 최기화

- ‘홈 – 환경 – 레이아웃 – 디폴트’ 를 실행한다.

### 언어 설정

- ‘홈 – 환경 – 설정 – 매트랩 – 일반 – 테스크탑 언어– 한국어/영어’ 를 설정한다.

상단 주황색 상자를 누르게 되면, 다음과 같은 창이 나옵니다.  
![둘러보기(2)](https://user-images.githubusercontent.com/44010902/65816746-79be3580-e23a-11e9-9e61-06caee4d72c0.PNG)

"편집기 창"이 나오며, 편집기 창에서 코드를 작성한 뒤, 상단의 실행(F5)을 누르면 명령 창에서 코드의 실행 결과를 알 수 있습니다. 파일 확장자는 ".m"입니다.

---

## 2. MATLAB 특징

- 변수를 선언할 필요가 없다.
- Matlab은 명령어를 한 행 단위로 실행되는 스크립트 언어이다.
- 대/소문자를 구별한다.
- 변수는 문자로 시작하며 문자, 숫자, \_로 구성된다 (내장 변수는 피한다).
- 라인의 끝에 있는 세미콜론(;)은 명령어의 출력을 보여주지 않는다.
- 모든 값은 1차원 이상의 배열(행렬)에 저장된다.
- 행렬의 첨자는 1부터 시작한다.
- 행렬의 원소를 나타내기 위해 괄호를 사용한다. A(i,j) – yes, A[i][j] – no
- 모든 연산자는 행렬에 오버로드(overloaded) 되어 있다.
- Matlab 함수의 반환 값은 변수로 구성된 벡터에 할당된다.
- 함수의 반환 값이 1개 이상일 수 있다.
- 일반적으로 명령어는 여러 줄에 걸쳐 작성되지 않는다. (예외: …연산자를 사용하면 가능하다)
- Matlab의 명령어는 함수 형태로 되어 있으므로 ‘명령어’와 ‘함수명’이 혼용되어 사용된다.

---

## 3. 코드 실행하며 기초 명령어 익히기

다음의 예제를 편집기 창에서 그대로 작성한 뒤, 명령어에 대해 간단히 설명해 보겠습니다.

```
% 점수의 평균을 계산하는 프로그램
clc; clear;
disp( '점수 평균 계산기' );
kor = input('국어 점수 = ');
eng = input('영어 점수 = ');
mat = input('수학 점수 = ');
sum = kor + eng + mat;
avg = sum/3
```

> ### "%"(퍼센트) 부호
>
> - "%" 이후에 나오는 문장은 무시합니다. 즉, 주석 처리합니다.
>
> ### ";"(세미콜론) 부호
>
> - MATLAB에서는 모든 명령에 대해 결과를 출력합니다. 하지만 세미콜론을 사용하면 **명령 창에 결과값이 나오지 않습니다**.
> - 명령을 구분하는 목적으로도 사용합니다.(1행)
> - 이 부호가 없어도 코드를 실행하는 데 아무런 문제가 없습니다.
> - 위 명령에서 sum값은 출력되지 않고, avg값만 출력됩니다.
>
> ### clc
>
> - **명령 창에 있는 내용을 모두 지웁니다**.
> - Windows CMD의 "cls"와 Linux Bash의 "clear"과 동일합니다.
>
> ### clear
>
> - 작업 공간에 있는 내용을 모두 지웁니다. 변수 값 설정이 전부 지워집니다.
> - **MATLAB은 코드 실행이 완료된 이후에도 변수 값을 지우지 않고 저장**합니다. 따라서 새로운 코드 실행 시 반드시 변수 내용을 비워주어야 합니다.
> - clear "변수명" 으로 변수 하나에 대해 초기화 할 수 있습니다.
>
> ### disp('String')
>
> - 괄호 내 작은따옴표 안의 **String 값이 명령 창에 출력**됩니다.
> - C언어의 printf, 파이썬의 print, JAVA의 System.out.println과 기능이 같습니다.
>
> ### input('string')
>
> - **명령 창으로부터 변수 값을 입력받습니다**.
> - 괄호 내 작은따옴표 안의 String 값이 명령 창에 출력됩니다.

다음으로 몇 가지 주의사항을 알아보겠습니다.

> - 변수를 초기화해 주지 않으면 (clear 명령) 다음 프로그램 실행 시 영향을 미칠 수 있습니다. 전에 계산한 변수를 사용하지 않는다면 되도록 코드의 제일 앞부분에 clear를 넣어주는 것이 좋습니다..
> - 코드는 한 줄에 작성을 원칙으로 하되, 여러 줄에 걸쳐서 작성하고자 할 때에는 줄의 끝부분에 "..." (마침표 3개)를 붙이고 다음 줄에 작성합니다.

---

이상으로 가장 기초적인 사용법 정리를 마치겠습니다. 다음에는 행렬과 벡터에 대해 알아보겠습니다.  
읽어주셔서 감사합니다.

---
layout: post
title: 1. React Native 설치 (Windows based)
categories:
  - React-native
---

# React-Native 개요

![React_logo](/assets/images/React_native/react.png)

프론트엔드 개발, 즉 UI를 제작하는 React의 문법으로 iOS, Android 등에서 구동할 수 있는 크로스플랫폼 앱을 만들 수 있습니다. 자세한 내용은 다음 사이트를 참고하길 바랍니다.  

> [React - 나무위키](https://namu.wiki/w/React(%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC)){: target="_blank"}    
> [React-native 공식 문서(영문)](https://facebook.github.io/react-native/docs/getting-started){: target="_blank"}    

**본 글은 React Native _ver 0.61_ 을 바탕으로 작성되었습니다.**  

**Expo가 아닌 순수 React Native 기반의 앱 제작 목적으로 만들어졌습니다.**

---

## 1. Package 설치  

먼저, Windows 기반에서 React Native를 설치해 보겠습니다.  
Chocolatey는 Windows 기반의 패키지 관리자입니다. 이곳에서 필요한 패키지를 내려받겠습니다. 먼저 Chocolatey을 설치하겠습니다.  
다음 링크를 눌러 아래 사진의 사이트에 접속합니다.  

[Chocolatey - Package manager](https://chocolatey.org/){: target="_blank"}  

![React_Native_install_1](/assets/images/React_native/React_native_install/install_1.PNG)

우측 상단의 install now를 눌러 다운로드 받고 설치합니다.  

저희가 설치하고자 하는 패키지는 nodejs, python2, jdk8 이렇게 3개입니다. 설치하는 방법은 다음과 같습니다.  

### Windows Powershell(관리자) 열기

- Windows10 기준 우하단 검색창에 powershell을 입력
- "관리자로 실행" 클릭  
![React_Native_install_2](/assets/images/React_native/React_native_install/install_2.PNG)  

### install 명령어 입력

- 다음과 같이 명령어를 입력합니다.  
```
choco install -y nodejs.install python2 jdk8
```
- install이 완료되면 창을 닫습니다.  

---

## 2. Android Studio 설치하기  

다음 게시글을 참조하여 Android Studio를 설치합니다.  
[Android Studio 설치(1) - Takeaim](http://takeaimk.tk/android%20app%20developing/2019/09/02/(Android-Studio)1.%EA%B0%9C%EB%B0%9C-%EC%A4%80%EB%B9%84(1).html){: target="_blank"}  

---
## 3. Android SDK 설치 및 환경변수 설정  

- 다음 게시글을 참조하되, SDK는 Android 9(Pie) - SDK Platform 28을 설치하고, AVD도 API Level을 28로 설치해 주세요!  
[Android Studio 설치(2) - Takeaim](http://takeaimk.tk/android%20app%20developing/2019/09/09/(Android-Studio)2.%EA%B0%9C%EB%B0%9C-%EC%A4%80%EB%B9%84(2).html){: target="_blank"}  

- 환경 변수 설정을 위해 다음과 같이 시작 표시줄 검색창에 "환경 변수"를 검색 후 눌러주세요.  
![React_Native_install_3](/assets/images/React_native/React_native_install/install_3.PNG)  
![React_Native_install_4](/assets/images/React_native/React_native_install/install_4.PNG)  
- 이곳에서 시스템 변수를 추가하고 변경하는 작업을 해야 합니다. 먼저, 시스템 변수의 "새로 만들기"를 눌러 다음과 같이 추가합니다.  
```
변수 이름 : ANDROID_HOME
변수 값 : c:\Users\<윈도우 계정 이름>\AppData\Local\Android\Sdk
```
- 만약 윈도우 계정 이름을 모르면 내PC(내 컴퓨터)-C드라이브-사용자 로 들어가서 확인해 줍니다.  
![React_Native_install_5](/assets/images/React_native/React_native_install/install_5.PNG)  
![React_Native_install_6](/assets/images/React_native/React_native_install/install_6.PNG)  
- 다음으로, Path를 추가합니다. 시스템 변수에서 Path를 찾아 편집을 누르고, 다음과 같이 추가합니다.
![React_Native_install_7](/assets/images/React_native/React_native_install/install_7.PNG)  
![React_Native_install_8](/assets/images/React_native/React_native_install/install_8.PNG)  
```
C:\Users\<윈도우 계정 이름>\AppData\Local\Android\Sdk\platform-tools
```

---
## 4. 새로운 APP 생성  
- 이제 App을 만들 위치에 경로 이동 후, 해당 경로의 폴더에 (Shift + 마우스 오른쪽 클릭) 을 한 후, "여기에 Powershell 창 열기"를 누릅니다.  
![React_Native_install_9](/assets/images/React_native/React_native_install/install_9.PNG)
- Powershell 창이 뜨면, 다음 코드를 입력 후 엔터를 누릅니다.  
```
npx react-native init AwesomeProject
```  
- 이제 한참 동안 무언가 다운로드 후 진행됩니다. 전부 진행될 때까지 기다립니다.  
![React_Native_install_10](/assets/images/React_native/React_native_install/install_10.PNG)
- 아래의 창이 나오면, 설치가 완료되었다는 뜻입니다.
![React_Native_install_11](/assets/images/React_native/React_native_install/install_11.PNG)  

---

이상으로 React Native 설치를 마치겠습니다.  
다음에는 Android 기반으로 처음 앱을 실행하는 방법을 알아보겠습니다.
읽어주셔서 감사합니다.

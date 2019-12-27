---
layout: post
title: 2. React Native 실행 (오류 대처 포함)
categories:
  - React-native
---

지난 글에 이어서 App을 실행해 보겠습니다.  
[React-native 설치](http://takeaimk.tk/react-native/2019/12/26/(React-native)1.React-Native-%EC%84%A4%EC%B9%98.html){: target="_blank"}    

**본 글은 React Native _ver 0.61_ 을 바탕으로 작성되었습니다.**  

**Expo가 아닌 순수 React Native 기반의 앱 제작 목적으로 만들어졌습니다.**

---

## 5. Android Studio에서 최초 실행  

지난 시간에 설치했던 Android Studio를 열어줍니다.  
이곳에서 App project를 열어줍니다.  
### open -> (React-Native 프로젝트 생성했던 폴더) -> AwesomeProject -> **android** 클릭 후 open 하고, Run task까지 완료될 때까지 기다립니다.  

> **APP Build 실패 시**
> - AwesomeProject\android\app\src\main 경로로 진입하여 "assets" 폴더 생성
> - Android Studio 상단의 Build-Rebuild Project 클릭

![React_Native_start_1](/assets/images/React_native/React_native_start/start_1.PNG)  
완료되면 하단의 **Terminal**을 누르고, 다음과 같이 입력하여 상위 경로로 이동합니다.  
```
cd ..
```
![React_Native_start_2](/assets/images/React_native/React_native_start/start_2.PNG)  

---

## 6. 최초 App 실행 (오류 대처 방법)  

이제 Terminal에 다음과 같이 입력합니다.
```
npx react-native run-android
```
여기서, 만약 실제 안드로이드 스마트폰이 있다면 개발자 설정에서 ADB를 켜둔 상태로 USB로 연결한다면 스마트폰에서 App 화면이 나옵니다.  
그렇지 않다면 안드로이드 에뮬레이터가 실행됩니다.  
> **에뮬레이터(AVD) 실행 실패 에러 발생 시**  
> - 에뮬레이터(AVD)가 정상적으로 설치되어 있는지 확인
> - 에뮬레이터를 먼저 실행시키고 다시 시도

![React_Native_start_3](/assets/images/React_native/React_native_start/start_3.PNG)  
![React_Native_start_4](/assets/images/React_native/React_native_start/start_4.PNG)  
![React_Native_start_5](/assets/images/React_native/React_native_start/start_5.PNG)  
다음과 같이 진행되었다면, Node.js도 실행되고, 에뮬레이터도 실행되어 App이 켜집니다. 다만, 조금 당혹스러운 화면이 나옵니다.  

![React_Native_start_6](/assets/images/React_native/React_native_start/start_6.PNG)  
~~첫 실행부터 에러라니!~~
당황하지 말고, 오류를 해결해 봅시다. 다음 방법을 따라해 봅시다.  
> - 다음 경로로 이동합니다.
> ```
> AwesomeProject\node_modules\metro-config\src\defaults
> ```
> - blacklist.js 파일을 열고, 해당 부분을 찾습니다.
> ```
> var sharedBlacklist = [
> /node_modules[/\\]react[/\\]dist[/\\].*/,
> /website\/node_modules\/.*/,
> /heapCapture\/bundle\.js/,
> /.*\/__tests__\/.*/
> ];
> ```
> - 해당 코드를 다음 코드로 바꾸어 줍니다.
> ```
> var sharedBlacklist = [
> /node_modules[\/\\]react[\/\\]dist[\/\\].*/,
> /website\/node_modules\/.*/,
> /heapCapture\/bundle\.js/,
> /.*\/__tests__\/.*/
> ];
> ```
> -저장 후 다시 실행합니다.
  
위 방법 시도 후 다음과 같은 창이 나오면 성공입니다.  

![React_Native_start_7](/assets/images/React_native/React_native_start/start_7.PNG)  

---
이상으로 React Native 최초 앱 실행을 마치겠습니다.  
다음에는 (미정)  
읽어주셔서 감사합니다.

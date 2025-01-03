---
layout: post
title: 1. 안드로이드 APP 개발 준비 (1)
categories:
  - Android App Developing
---

# 안드로이드 앱 제작을 위한 기본 개념과 IDE

![Android_studio](https://user-images.githubusercontent.com/44010902/64094485-d858d680-cd96-11e9-9198-26d5829df56e.jpg)

안드로이드 앱을 만드는 방법은 생각보다 다양합니다. 가장 쉬운 방법으로는, 앱 인벤터를 활용하는 방법입니다. "[앱 인벤터 2](http://ai2.appinventor.mit.edu/)"를 활용하면 좀 더 쉽게 앱을 만들 수 있습니다. 그러나 본 글에서는 안드로이드 스튜디오를 활용해서 앱을 만드는 방법을 작성해 보도록 하겠습니다.

---

## 1. 안드로이드 앱 개발에 필요한 언어

원래 안드로이드 앱은 JAVA를 사용하여 만들어졌습니다. 그러나 JAVA를 개발한 Sun사를 인수한 오라클은 저작권 분쟁 소송을 제기하고, 이 과정 속에서 구글은 안드로이드 앱 개발 언어를 코틀린으로 바꾸게 되었습니다. 자세한 설명은 다음 글들을 통해 알아보실 수 있습니다.

> [JAVA - 나무위키](https://namu.wiki/w/Java)  
> [코틀린 - 나무위키](https://namu.wiki/w/Kotlin)  
> [구글vs오라클 완벽히 이해하기 - ETI](https://etinow.me/1)

따라서 현재는 JAVA를 사용하여 개발이 가능하지만, 코틀린을 같이 익히는 것도 좋은 선택이 될 수 있습니다.

---

## 2. 안드로이드 스튜디오 (Android Studio 설치)

먼저 안드로이드 스튜디오가 어떤 것인가에 대해서는 길게 설명하지 않습니다. 다음 글을 가볍게 읽어보시기 바랍니다.

> [안드로이드 스튜디오 - 나무위키](https://namu.wiki/w/%EC%95%88%EB%93%9C%EB%A1%9C%EC%9D%B4%EB%93%9C%20%EC%8A%A4%ED%8A%9C%EB%94%94%EC%98%A4)

다음 과정을 순서대로 잘 따라와 주세요!

---

### 1. 아래 주소를 클릭합니다.

> https://developer.android.com/studio/

주소에 접속하면 현재 사용하고 있는 컴퓨터에 알맞은 버전의 안드로이드 스튜디오 다운로드 링크가 나옵니다.

---

### 2. 다운로드 버튼을 누릅니다.

![AS설치1](https://user-images.githubusercontent.com/44010902/64095007-89ac3c00-cd98-11e9-8359-6a176bc50895.PNG)  
![AS설치2](https://user-images.githubusercontent.com/44010902/64095227-2f5fab00-cd99-11e9-94d9-474cc80613a6.PNG)

**용량이 700MB를 넘으므로 꼭 안정되어 있는 네트워크에서 다운로드 받으세요!**
![AS설치3](https://user-images.githubusercontent.com/44010902/64095351-8d8c8e00-cd99-11e9-82e7-e814743a1e1e.PNG)

---

### 3. 설치를 진행합니다.

캡처된 사진을 보며 진행해 주세요.

![AS설치4](https://user-images.githubusercontent.com/44010902/64096643-2670d880-cd9d-11e9-8ed4-ef54c6e3938b.PNG)  
![AS설치5](https://user-images.githubusercontent.com/44010902/64096647-296bc900-cd9d-11e9-9cc5-ef572d739012.PNG)  
![AS설치6](https://user-images.githubusercontent.com/44010902/64096649-2bce2300-cd9d-11e9-8173-7d7bd0c16bbc.PNG)  
![AS설치7](https://user-images.githubusercontent.com/44010902/64096656-2d97e680-cd9d-11e9-811f-8026e01e99fe.PNG)  
![AS설치8](https://user-images.githubusercontent.com/44010902/64096664-2ec91380-cd9d-11e9-99ae-ae76bb8662ad.PNG)

---

### 4. 초기 설정을 진행합니다.

![AS설치9](https://user-images.githubusercontent.com/44010902/64096823-98e1b880-cd9d-11e9-933e-b7f0967c8d0a.PNG)  
만약 기존 안드로이드 스튜디오에서 사용하던 설정이 있으시다면 이 과정에서 넣어주시면 됩니다.

![AS설치10](https://user-images.githubusercontent.com/44010902/64096986-01309a00-cd9e-11e9-89c3-59853c50d17c.PNG)  
사용자 데이터(통계) 등을 익명으로 구글에 보낼 것이냐 묻는 창입니다. 꺼림직하시다면 Don't send 누르셔도 무관합니다.

![AS설치11](https://user-images.githubusercontent.com/44010902/64097265-c0855080-cd9e-11e9-9aed-c8de69d8acc8.PNG)  
Next를 눌러주세요

![AS설치12](https://user-images.githubusercontent.com/44010902/64097830-38a04600-cda0-11e9-8f7f-2be4315ac275.PNG)  
두 가지 선택이 있습니다. Standard로 설치하셔도 무관하지만 가상 머신의 RAM 크기를 직접 설정하기 위해 Custom으로 진행하였습니다.

![AS설치13](https://user-images.githubusercontent.com/44010902/64097834-39d17300-cda0-11e9-97ac-b8e3401cc8ff.PNG)  
테마는 취향으로 골라주시면 됩니다. 저는 다크 테마를 좋아하기 때문에 Darcula를 선택했습니다.

![AS설치14](https://user-images.githubusercontent.com/44010902/64097836-3b9b3680-cda0-11e9-8ce9-ae91035fe3fe.PNG)  
**꼭 제일 하단의 체크박스(Android Virtual Device)에 체크해 주세요!**  
안드로이드 가상 머신이 없으면 무엇 하나 추가할 때마다 직접 폰으로 옮겨서 테스트 해 보아야 합니다. 매우 귀찮은 작업일 수밖에 없죠. 이러한 작업을 직접 컴퓨터 상에서 돌려볼 수 있게 해 주는 가상 안드로이드 머신입니다. 기본은 체크 해제 상태이므로 확인 후 넘어가 주세요!  
참고로 SDK 설치 주소는

```
C:\Users\(현재 계정 이름)\AppData\Local\Android\Sdk
```

입니다. AppData 폴더가 보이지 않을 경우, 윈도우 탐색기의 상단 탭 "보기"를 누른 후, 숨긴 항목 체크를 해 주시면 됩니다.

![AS설치15](https://user-images.githubusercontent.com/44010902/64097838-3ccc6380-cda0-11e9-9a92-273c6d16a77b.PNG)  
가상 머신의 RAM 크기 설정입니다. 왠만해서 이곳에서 앱을 만드려고 보시는 분들께서는 2GB로도 차고 넘칠 것이지만... 저는 RAM이 16GB이므로 ~~자랑~~ 넉넉하게 4~~달라~~GB 할당하겠습니다.

![AS설치16](https://user-images.githubusercontent.com/44010902/64097844-3dfd9080-cda0-11e9-9fdc-02e059562d1b.PNG)  
Finish를 누르면 다운로드를 진행합니다. 가상 머신 용량이 꽤 크므로 시간이 좀 소요됩니다. 안정된 네트워크에 연결 후 잠시 ~~낮잠을~~ 쉬었다가 오시면 되겠습니다.

![AS설치17](https://user-images.githubusercontent.com/44010902/64098294-79e52580-cda1-11e9-8ba3-f16f701f69cb.PNG)  
![AS설치18](https://user-images.githubusercontent.com/44010902/64100749-35f51f00-cda7-11e9-9c85-862297230bc1.PNG)  
설치가 완료되었습니다. Finish를 눌러주세요.

### 5. 최신 버전으로 업데이트합니다.

![AS설치19](https://user-images.githubusercontent.com/44010902/64102693-6d65ca80-cdab-11e9-905f-1c8b31e66540.PNG)  
다음과 같은 창이 뜨면 하단의 configure을 클릭 후 Check for update를 눌러 최신 버전인지 확인해 주세요.  
![AS설치19](https://user-images.githubusercontent.com/44010902/64102920-e6652200-cdab-11e9-8ab7-0459e8458c01.PNG)  
![AS설치20](https://user-images.githubusercontent.com/44010902/64102921-e6fdb880-cdab-11e9-9e44-06a152925bd2.PNG)  
![AS설치21](https://user-images.githubusercontent.com/44010902/64102923-e6fdb880-cdab-11e9-9d90-7073a7e4e80b.PNG)

---

이상으로 설치를 마치겠습니다. 다음에는 기본 설정과 프로젝트 생성에 대해 알아보겠습니다.  
읽어주셔서 감사합니다.

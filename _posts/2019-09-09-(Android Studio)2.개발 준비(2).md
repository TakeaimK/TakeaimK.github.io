---
layout: post
title: 2. 안드로이드 APP 개발 준비 (2)
categories:
  - Android App Developing
---

# 안드로이드 스튜디오 기본 설정

지난 게시글 <[1. 안드로이드 APP 개발 준비 (1)](http://takeaimk.tk/android%20app%20developing/2019/09/02/(Android-Studio)1.%EA%B0%9C%EB%B0%9C-%EC%A4%80%EB%B9%84(1).html)>에 이어서, 이번 시간에는 프로젝트 생성, API 다운로드, 가상머신 실행 등을 해보겠습니다.

---

## 1. 프로젝트 생성

먼저 새로운 프로젝트를 생성해 보겠습니다.  
가장 위에 있는 메뉴를 눌러주세요.  
![AS셋팅1](https://user-images.githubusercontent.com/44010902/64516527-a06b0980-d329-11e9-941d-498aa2aa4e90.PNG)

Empty Activity를 선택하고, Next를 눌러줍니다.
![AS셋팅2](https://user-images.githubusercontent.com/44010902/64516528-a06b0980-d329-11e9-84f2-6038548cd5ed.PNG)

몇 가지 설정을 진행하게 됩니다.  
![AS셋팅3](https://user-images.githubusercontent.com/44010902/64516530-a06b0980-d329-11e9-8db2-46cb79b6103d.PNG)  
Name은 적당히 만들어 주고, Package name은 Name에 따라 자동으로 변경되니 되도록 놔두는 것이 좋습니다.  
저장 경로는 되도록 바꾸지 않는 것을 추천하지만, 필요하다면 공간이 넉넉한 드라이브로 바꿔주세요.  
언어는 Kotlin과 Java가 있는데, 자세한 내용은 지난 게시글에 올려놓았습니다. 본 강좌에서는 Java를 사용하도록 하겠습니다.  
**Minimuum API level 설정이 중요합니다!** 이 항목은 만드는 App이 돌아갈 수 있는 최소 운영체제 버전을 의미합니다. 본인이 사용하는 디바이스 운영체제 버전을 확인하고, 여러 가지 버전을 눌러보며 하단에 나오는 "이 앱을 사용 가능한 디바이스 비율"을 보고 적절한 버전을 선택해 주세요. 저는 Android 7.0(Nougat)을 선택했습니다.  
모두 설정했으면, Finish를 눌러주세요.

잠시 기다리면 다음과 같은 화면이 나옵니다. 우상단의 File을 누르고, Setting을 눌러주세요.
![AS셋팅4](https://user-images.githubusercontent.com/44010902/64516532-a103a000-d329-11e9-9a85-948ef340b958.PNG)  
![AS셋팅5](https://user-images.githubusercontent.com/44010902/64516535-a103a000-d329-11e9-886d-c00521941df5.PNG)

먼저 SDK를 다운로드 받아보겠습니다.  
Appearance & Behavior - System Setting - Android SDK 순으로 눌러줍니다.
![AS셋팅6](https://user-images.githubusercontent.com/44010902/64516536-a103a000-d329-11e9-89b1-282dbefb1bd2.PNG)  
우측에 SDK 목록이 나오는데, 사용할 SDK를 체크해 주세요. 저와 같이 체크해 두시는 것을 추천드립니다.

체크를 하더라도 전부 설치하는 것이 아니라 그 안에 쪼개져 있는 여러가지 설치항목이 있는데, 다음과 같이 하단의 _"Show Package Detail"_ 을 체크하시면 조회하실 수 있습니다.
![AS셋팅8](https://user-images.githubusercontent.com/44010902/64516539-a19c3680-d329-11e9-8ad7-4ee5f886d459.PNG)

체크하시면 다음과 같이 우측에 다운로드 모양 아이콘이 활성화됩니다.
![AS셋팅7](https://user-images.githubusercontent.com/44010902/64516537-a19c3680-d329-11e9-9cf0-3aeffb4a1617.PNG)  
 우하단에 Apply를 눌러주세요.

용량 확인 후 OK를 눌러주세요.
![AS셋팅9](https://user-images.githubusercontent.com/44010902/64516540-a19c3680-d329-11e9-81dc-e8208e51b84a.PNG)

설치가 진행됩니다.
![AS셋팅10](https://user-images.githubusercontent.com/44010902/64516541-a19c3680-d329-11e9-9337-f993c07d647d.PNG)

![AS셋팅11](https://user-images.githubusercontent.com/44010902/64516543-a234cd00-d329-11e9-8aa5-eb0713ed2585.PNG)  
Finish를 눌러주세요.

### 추가 설정 - Auto import, Font

사용하는 함수들의 라이브러리를 일일히 import시킬 필요 없이 안드로이드 스튜디오에서 자체적으로 import시켜주는 기능입니다. 먼저 위에서 진행한 대로 File - Setting으로 진입 후 아래처럼 Editor - General - Auto import 로 들어갑니다.
![AS셋팅12](https://user-images.githubusercontent.com/44010902/64516544-a234cd00-d329-11e9-97a9-6b063fac5ac1.PNG)
상단의 사진처럼 모든 항목에 체크해 주시고 똑같이 설정해 주시면 되겠습니다.

또한 Editor 메뉴 하단의 Font에서 글씨 크기, 글씨체 등을 변경할 수 있습니다.
![AS셋팅13](https://user-images.githubusercontent.com/44010902/64516546-a234cd00-d329-11e9-86fa-82694ecb8a4b.PNG)

---

## 2. AVD(Android Virtual Device) 설정

Android Virtual Device(안드로이드 가상 디바이스, 속칭 AVD)는 App을 Build 후 실제로 실행시켜 볼 수 있는 가상 안드로이드 장치를 말합니다. 실제로 주변에서 볼 수 있는 안드로이드 스마트폰에서 지원하는 기능을 모두 사용하지는 못하지만(Wifi, Bluetooth, NFC, Headphone 등), 가상 App을 실행시킬 수 있기 때문에 거의 필수입니다.  
방금 전까지 설정하던 Setting 창을 닫고, 다음 과정을 따라와 주세요.

우상단의 AVD Manager을 눌러주세요.
![AS셋팅14](https://user-images.githubusercontent.com/44010902/64516547-a2cd6380-d329-11e9-977b-b5a9fc0e0e40.PNG)

누르면 이미 기기가 있는 경우도 있고, 없는 경우도 있습니다. 저는 제가 글 작성 시점에 사용 중인 스마트폰 Pocophone F1 기준으로 안드로이드 가상 디바이스를 만들고 싶어서 새로 만들어 보겠습니다.
![AS셋팅15](https://user-images.githubusercontent.com/44010902/64516548-a2cd6380-d329-11e9-9fb5-70d35def195f.PNG)
좌측 하단의 _"Create Virtual Device.."_ 버튼을 클릭합니다.

다음과 같이 다양한 레퍼런스 디바이스가 나옵니다.
![AS셋팅16](https://user-images.githubusercontent.com/44010902/64516549-a2cd6380-d329-11e9-9e68-e8b4c9834aee.PNG)
아마 대부분 이 글을 보시는 분들께서는 목록에 나온 같은 기기를 사용하시는 분이 거의 없을 것입니다. 따라서 해상도나 화면 크기가 조금씩 다를 수 있기에 좌측 하단의 _"New Hardware Profile"_ 을 눌러 직접 설정해 보겠습니다.

![AS셋팅17](https://user-images.githubusercontent.com/44010902/64516551-a2cd6380-d329-11e9-976c-9ff89e4b26a8.PNG)
다음과 같이 창이 나오면 각 항목을 본인의 기기 사양에 맞게 입력하시면 됩니다. 기기 사양은 구글이나 위키 등에 본인의 기기명을 검색하면 화면 크기와 해상도를 찾을 수 있습니다.  
Memory 항목은 **사용하고 계신 컴퓨터 메모리 크기의 4분의 1** 이하를 추천드립니다. 그래도 최소 2G(2048MB)의 메모리를 추천드립니다.  
하단 체크박스는 전부 다 체크하셔도 되고, 본인의 휴대폰에 없는 센서 등은 제외시키셔도 좋습니다.

다 설정하셨다면 Finish를 눌러 다시 전 창으로 돌아옵니다.  
상단에 새로 만든 기기명으로 등록되어 있습니다.
![AS셋팅18](https://user-images.githubusercontent.com/44010902/64516552-a365fa00-d329-11e9-87db-fded7b7428db.PNG)
본인이 설정한 기기명을 누르고 Next를 누릅니다.

![AS셋팅19](https://user-images.githubusercontent.com/44010902/64516553-a365fa00-d329-11e9-903c-5dc0a6aa5de7.PNG)  
안드로이드 가상 디바이스에서 사용할 안드로이드 OS 버전을 선택하는 창입니다. 본인의 기기와 같은 OS를 선택하셔도 좋고, 최신 OS를 선택하셔도 좋습니다.  
선택 후 Next를 누릅니다.

최종적으로 점검하는 창입니다. 점검 후 Finish를 누릅니다.
![AS셋팅20](https://user-images.githubusercontent.com/44010902/64516554-a365fa00-d329-11e9-849f-e5f0cc9824e9.PNG)

본인이 설정한 기기가 창에 나옵니다. 우측의 초록색 화살표를 눌러 가상 디바이스를 실행합니다.
![AS셋팅21](https://user-images.githubusercontent.com/44010902/64516555-a3fe9080-d329-11e9-95ad-283ce1e77f98.PNG)

만약 다음과 같은 경고가 나온다면, 일단 OK를 누릅니다. 이 경고에 대한 내용과 해결책은 하단에 서술하겠습니다.
![AS셋팅22](https://user-images.githubusercontent.com/44010902/64516556-a3fe9080-d329-11e9-8113-d6ea522d4001.PNG)

다음과 같은 부팅 애니메이션이 나온 뒤 흔한 스마트폰 메인 런처를 보실 수 있습니다.
![AS셋팅23](https://user-images.githubusercontent.com/44010902/64516558-a3fe9080-d329-11e9-8a92-a3350cf8990c.PNG)
![AS셋팅24](https://user-images.githubusercontent.com/44010902/64516560-a4972700-d329-11e9-848d-c6587160ef1f.PNG)  
우측에 있는 컨트롤 패널로 화면 끄기, 볼륨 조절, 화면 회전, 캡처, 네비게이션, 그리고 AVD 종료와 최소화 등을 수행할 수 있습니다.

---

### Detected ADB 오류 수정

다음과 같은 오류 메세지가 발생하는 경우는 안드로이드 에뮬레이터 등이 최신 버전이 아닐 때 발생합니다.
![AS셋팅22](https://user-images.githubusercontent.com/44010902/64516556-a3fe9080-d329-11e9-8113-d6ea522d4001.PNG)

다음과 같은 방법으로 해결할 수 있습니다. 먼저, File-Setting 메뉴로 진입한 후, Android SDK 메뉴로 진입합니다. 그리고 가운에 있는 SDK Tools을 선택합니다.
![AS셋팅25](https://user-images.githubusercontent.com/44010902/64516561-a4972700-d329-11e9-9544-f2795791faa4.PNG)
위 사진과 같이 업데이트가 가능하다고 나오는 항목이 있고, 체크박스에 "-" 표시가 나와 있습니다.

아래 사진과 같이 체크박스의 "-"를 체크가 될 때까지 클릭해 주시고, 하단의 Apply를 눌러주세요.
![AS셋팅26](https://user-images.githubusercontent.com/44010902/64516562-a4972700-d329-11e9-8595-6d0f78ac0a41.PNG)

OK를 눌러주세요.
![AS셋팅27](https://user-images.githubusercontent.com/44010902/64516563-a4972700-d329-11e9-9424-1b074d884eb0.PNG)

![AS셋팅28](https://user-images.githubusercontent.com/44010902/64516564-a52fbd80-d329-11e9-88ec-942a6338b3d0.PNG)

Finish를 눌러주세요.
![AS셋팅29](https://user-images.githubusercontent.com/44010902/64516565-a52fbd80-d329-11e9-836b-5984f83d6a42.PNG)  
이제 에뮬레이터를 실행할 때 오류가 발생하지 않는 것을 볼 수 있습니다.

---

이상으로 개발 준비를 마치겠습니다. 다음에는 프로젝트 생성 시 기본 생성 파일과 안드로이드 스튜디오 창에 대해 알아보겠습니다.
읽어주셔서 감사합니다.

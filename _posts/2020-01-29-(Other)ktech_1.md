---
layout: post
title: K-Tech 현장실습 - React-Native로 공지사항 제작
categories:
  - Other
---

## 프로젝트 개요
 - 현재 Ionic으로 개발된 하이브리드 K-HUB APP -> 크로스플랫폼 App으로 변경
 - Framework : React-native
 - Reopsitory : Github, npm
 - 작업인원 : 실습생 4명

 ## 준비과정
 - React-native 설치 : [설치(1)](http://takeaimk.tk/react-native/2019/12/26/(React-native)1.React-Native-%EC%84%A4%EC%B9%98.html) / [설치(2)](http://takeaimk.tk/react-native/2019/12/27/(React-native)2.React-Native-%EC%8B%A4%ED%96%89.html)  

 - App 제작에 필요한 node_modules install  
 ```
1. 네비게이션
 npm install --save react-navigation
 npm install --save react-native-gesture-handler
 npm install --save react-navigation-stack

2. 뷰
 npm install --save @react-native-community/masked-view
 npm install react-native-safe-area-context

3. 모달 팝업
 npm install react-native-extra-dimensions-android
 npm install react-native-modal
 npm install react-native-reanimated

4. 아이콘
 npm install react-native-vector-icons --save

5. image 선택
 npm install react-native-image-picker

6. AsyncStorage
 npm install @react-native-community/async-storage --save
 ```  
## 실제 화면 (Web)
![khub_site_Notice](/assets/images/Other/khub_site_notice.PNG)  
![khub_site_Notice_detail](/assets/images/Other/khub_site_notice_detail.PNG)  

## 화면 구성 요소 설명 및 Code
1. Navigation
- 화면 상단에 뒤로가기 버튼과 제목 노출
```javascript
<View style={styles.header}>
    <Icon onPress={()=>{navigation.goBack()}} style={{color:'#fff',fontSize:26, position:'absolute',left:15,}} name='ios-arrow-back'/>
    <Text style={styles.title}>공지사항</Text>
</View>
```
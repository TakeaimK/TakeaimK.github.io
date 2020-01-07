---
layout: post
title: 3. React Native Component(1)
categories:
  - React-native
---

React Native에서는 주로 사용되는 컴포넌트를 지원합니다.  
지금부터 몇 개의 컴포넌트를 중심으로 하나씩 알아가 보도록 하겠습니다.  

**본 글은 React Native _ver 0.61_ 을 바탕으로 작성되었습니다.**  

**Expo가 아닌 순수 React Native 기반의 앱 제작 목적으로 만들어졌습니다.**

---
## View, Text, Image  

### App.js
```

import React, { Component } from 'react';
import {
  StyleSheet,
  View,
  Text,
  Image,
} from 'react-native';




export default class App extends Component{
  render(){
    let pic = {
      uri : 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
    }
    return(
      <View style={styles.container}>
        <Text style={styles.title}>Hello World!</Text>  
        <Text style={styles.title}>Hi</Text>
        <Image source={pic} style={{width:300, height:100}} />
      </View>
    )
  };
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent:'center',
    alignItems:'center',
    //backgroundColor: 'powderblue',
  },
  title: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
});

```
### Import 분석  
- View
  - div와 유사한 역할을 수행
  - 주로 구역을 나누거나 style을 입힐 때 사용
  ```
  <View style={styles.someone}>
       (Contents)
  </View>
  ```
- Text
  - 문장을 화면에 띄울 때 사용
  ```
   <Text style={styles.someone}>Hello World!</Text> 
  ```
- Image
  - 로컬 이미지나 네트워크 경로의 이미지를 띄울 때 사용
  ```
  <Image source={pic} style={{width:300, height:100}} />
  ```
- StyleSheet
  - CSS와 거의 동일한 방법으로 디자인
  - CSS와의 차이점 : 카멜 케이스 (camelCase, 낙타 표기법) 사용. font-size => fontSize  
  ```
  const styles = StyleSheet.create({
  someone: {
    (write design)
  },
  });
  ```

  ### 실행화면
![React_Native_ViewTextImage](/assets/images/React_native/Component/ViewTextImage.PNG) 
---


---
이상으로 React Native 최초 앱 실행을 마치겠습니다.  
다음에는 (미정)  
읽어주셔서 감사합니다.

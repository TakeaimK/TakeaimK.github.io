---
layout: post
title: 4. React Native Component(2) - State
categories:
  - React-native
---

이번 시간에 알아볼 것은 상태, 즉 State입니다.  
1초 간격으로 상태를 바꾸어 주는 예제를 실습해 보겠습니다.

**본 글은 React Native _ver 0.61_ 을 바탕으로 작성되었습니다.**  

**Expo가 아닌 순수 React Native 기반의 앱 제작 목적으로 만들어졌습니다.**

---
## State - setInterval

### App.js
```

import React, { Component } from 'react';
import {
  StyleSheet,
  View,
  Text,
} from 'react-native';

class Blink extends Component{
  constructor(props){
      super(props);
      this.state = {isShowingText: true}

      setInterval(()=>(this.setState(
        prevState => (
          {isShowingText: !prevState.isShowingText})
          )), 1000);
  }
  render(){
    if(!this.state.isShowingText){
      return (
        <Text>♥ ♥ ♥</Text>
      );
    }
    return(
      <Text>{this.props.text}</Text>
    );
  }
}



export default class App extends Component{
  render(){
    return(
      <View style={styles.container}>
        <Blink text="테스트입니다"/>
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
### 코드 분석  

- export default class APP
  - Blink 클래스를 호출할 때 text를 넘겨 줌. Blink Class에서는 props의 text로 사용

```
export default class App extends Component{
  render(){
    return(
      <View style={styles.container}>
        <Blink text="1초 단위로 번갈아가며 출력"/>
      </View>
    )
  };
}
```  

- extend Component
  - Component를 상속받음
  - 쉽게 말해, Component가 가진 메소드를 사용할 수 있음

```
class Blink extends Component{
  (Contents)
}
```  

- constructor(props)
  - 생성자. 즉, 해당 컴포넌트가 마운트되기 전에 호출됨
  - super(props)를 통해 this.state를 정의 및 객체를 할당하여 지역 state를 초기화
  - this.state의 isShowingText를 True로 설정

- setInterval(A, B)
  - B msec 단위로 A 가 작동하는 함수
  - A는 Arrow Function으로 구성. B msec가 지나면 this.setState의 prevState(직전 상태)에서 isShowingText 값이 반전됨. 즉 T=true면 false로, false면 true가 됨
  - B 값이 1000 이므로 1000msc=1sec. 즉, 1초마다 상태가 변경됨

```
constructor(props){
      super(props);
      this.state = {isShowingText: true}

      setInterval(()=>(this.setState(
        prevState => (
          {isShowingText: !prevState.isShowingText})
          )), 1000);
  }
  
```  

- render()
  - this.state.isShowingText가 false라면 ♥ ♥ ♥ 을 return
  - this.state.isShowingText가 true라면 넘겨받은 원래의 text를 출력

```
render(){
    if(!this.state.isShowingText){
      return (
        <Text>♥ ♥ ♥</Text>
      );
    }
    return(
      <Text>{this.props.text}</Text>
    );
  }
```  


### 실행화면
![React_Native_ViewTextImage](/assets/images/React_native/Component/State1.PNG)  
![React_Native_ViewTextImage](/assets/images/React_native/Component/State2.PNG) 

---
본 강좌는 [ideafactory kaist](https://www.youtube.com/channel/UCTivi6Kji_93AjJu-7-osLQ) 강좌 기반으로 진행됩니다.  
읽어주셔서 감사합니다.

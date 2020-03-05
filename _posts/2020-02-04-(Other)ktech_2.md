---
layout: post
title: K-Tech 현장실습 - React-Native로 공지사항 제작(2)
categories:
  - Other
---

## 지난 진행 과정
[K-Tech 현장실습 - React-Native로 공지사항 제작(1)](http://takeaimk.tk/other/2020/01/29/(Other)ktech_1.html){: target="_blank"}  

## 이번에 실습할 사항
 - 공지사항의 Main화면을 제작했으니, 이제 세부사항 보기 화면을 제작해 보자.
 - 전체 공지사항 코드를 조금만 수정하면, 그룹 공지사항에도 사용이 가능하다. 코드 재사용으로 생산성을 향상시켜 보자.
 - 일부 항목(이용약관 등)은 웹 사이트를 그대로 띄워주어도 괜찮다. Webview를 사용해 보자.
 - React Native 내부에서도 HTML 태그를 사용할 수 있는 라이브러리를 사용해서 가독성을 높여보자.

## 준비과정

<details>
<summary>추가 node_modules install </summary>
<div markdown="1"> 

 ```
1. WebView
    npm install react-native-htmlview --save
2. HTMLView
    npm install react-native-webview --save
 ```  
 </div>
</details>

## 실제 화면 (Web)
![khub_site_Notice](/assets/images/Other/khub_site_group_notice.PNG){: width="360" height="640"}    
![khub_site_Notice](/assets/images/Other/khub_site_group_notice_2.PNG){: width="360" height="640"}    
![khub_site_Notice_detail](/assets/images/Other/khub_site_group_notice_detail.PNG){: width="360" height="640"}    

## 화면 구성 요소 설명 및 Code (공지사항 세부내용)

![khub_App_React-native_Notice](/assets/images/Other/khub_app_rn_notice_detail.png){: width="360" height="640"}  

### 1. Navigation
- 공지사항 목록과 유사
- 상단 타이틀 제목을 "공지사항 내용"으로만 변경

### 2. 공지 제목
- AdminNotice로부터 필요한 항목을 navigation.getParam()을 사용하여 받아옴
- 가져온 항목을 hook를 사용(useState)하여 update
- 시간 값은 유닉스 시간으로 넘어오기 때문에 알아보기 쉽도록 변환 함수(timestamp2DateStr) 사용

### 3. 공지 내용
- 공지 내용이 HTML 태그가 붙어서 전달받기 때문에 태그 처리 필요
- HTML 태그를 사용할 수 있는 HTMLView를 사용하여 표현

<details>
<summary>Code</summary>
<div markdown="1">

```javascript
const [title,setTitle] = useState(navigation.getParam('title','null'));
const [body,setBody] = useState(navigation.getParam('body','null'));
const [userName,setUserName] = useState(navigation.getParam('user_name','null'));
const [date,setDate] = useState(navigation.getParam('date','null'));
const [count,setCount] = useState(navigation.getParam('count','null'));

(...)

<View style={styles.contents}>
    <ScrollView>
        <View style={styles.subTitle}>
            <Text style={{fontSize:22}}>{title}</Text>
        </View>
        <View style={styles.adminAndDate}>
            <Text style={{fontSize:14}}>
                작성자 : {userName} | 작성일시{timestamp2DateStr(date)} | 조회수{count}
            </Text>
        </View>
        <View style={styles.mainContent}>
        <HTMLView
            value={body}
            stylesheet={{fontSize:16, color:'white'}}
        /> 
        </View>
    </ScrollView>
</View>
```

</div>
</details>

<details>
<summary>Unix Timestamp function</summary>
<div markdown="1">

```javascript

function timestamp2DateStr(UNIX_timestamp){
    var a = new Date(UNIX_timestamp);
    console.log(UNIX_timestamp);
  
    var year = a.getFullYear();
    //var month = months[a.getMonth()];
    var month = (a.getMonth()+1);
    var day = "0" + a.getDate();
    var hour = "0" + a.getHours();
    var minute = "0" + a.getMinutes();
    var second = "0" + a.getSeconds();
    var time = year + "-" + month.toString().substr(-2) + "-" + day.substr(-2) + " " + hour.substr(-2) + ":" + minute.substr(-2) + ":" + second.substr(-2);
    return time;
  }
```

</div>
</details>

## 코드 재사용으로 빠르게 그룹 공지 제작하기


## 화면 구성 요소 설명 및 Code (이용약관 및 개인정보 보호정책)
![khub_App_React-native_Policy](/assets/images/Other/khub_app_rn_policy.png){: width="360" height="640"}  
![khub_App_React-native_Policy](/assets/images/Other/khub_app_rn_policy_detail.png){: width="360" height="640"}  

### WebView
- 특정 사이트에서 넘어오는 HTML 문서를 그대로 화면에 띄워 줌
- 데스크톱 브라우저 버전으로 열려 핀치 줌이 가능
- 웹 페이지의 내용을 가공하지 않고 그대로 화면에 띄워 줄 때 유용

<details>
<summary>Unix Timestamp function</summary>
<div markdown="1">

```javascript
<View style={styles.contents}>
    <WebView
        source={{uri: '(이용약관이 담겨있는 URL을 입력)'}}
    />  
</View>
```

</div>
</details>

## 구현에서 어려웠던 점
- 페이지 데이터 전송 시 HTML Tag가 같이 넘어오는데 이 데이터를 그대로 출력 시 HTML Tag를 읽지 못하고 텍스트로 인지하여 그대로 출력하는 문제가 발생하였다.
- 초기에는 'HTMLView'를 활용해서 이용약관을 작성하려고 시도했다. 그러나 모바일 환경에 맞춰 만들어진 페이지가 아니라 가독성이 떨어졌고, 스크롤이 굉장히 길어지는 문제가 발생했다. 같이 근무하는 실습생의 조언을 토대로 Webview를 사용하여 비교적 쉽게 해결하였다.

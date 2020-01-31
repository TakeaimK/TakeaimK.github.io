---
layout: post
title: K-Tech 현장실습 - React-Native로 공지사항 제작
categories:
  - Other
---

## 프로젝트 개요
 - 현재 Ionic으로 개발된 하이브리드 K-HUB APP -> 크로스플랫폼 App으로 변경
 - 현재 내 파트 : 전체 공지사항 구현
 - Framework : React-native
 - Reopsitory : Github, npm
 - 작업인원 : 실습생 4명
  
## 공지사항 작동 구조

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
![khub_App_React-native_Notice](/assets/images/Other/khub_app_rn_notice.png){: width="360" height="640"}  

### 1. Navigation
- 화면 상단에 뒤로가기 버튼과 제목 노출
- ios 스타일의 뒤로가기 버튼 적용

<details>
<summary>Code</summary>
<div markdown="1">

```javascript
<View style={styles.header}>
    <Icon onPress={()=>{navigation.goBack()}} style={{color:'#fff',fontSize:26, position:'absolute',left:15,}} name='ios-arrow-back'/>
    <Text style={styles.title}>공지사항</Text>
</View>
```
</div>
</details>

### 2. 공지사항 List
- publicNotices에서 공지사항 Data를 가져옴
- `Flatlist`를 사용하고 각 항목마다 `TouchableOpacity`를 눌러 
NoticeDetail으로 넘어가도록 구성
- NoticeDetail에 받아온 요소 중 필요한 항목을 넘겨줌
- 각 항목은 게시글의 고유ID로 구분

<details>
<summary>Code</summary>
<div markdown="1">

```javascript
const [publicNotices,setPublicNotices] = useState([]);
//Hook를 사용하여 publicNotices를 Update
...

<View style={styles.contents}>
  <FlatList
      data ={publicNotices}
      numColumns={1}
      renderItem = {({item})=>
      <View style={styles.list}>
          <TouchableOpacity
              onPress={()=>navigation.navigate('NoticeDetail',{
                  title: item.title,
                  body: item.body,
                  ...(넘겨지는 Data)...
              })
          }>
          
          <Text numberOfLines={1}style={{fontSize:20}}>
              {item.title}
          </Text>
          <Text style={{fontSize:12}}>
              {item.userName} | {timestamp2DateStr(item.date)} | {item.count}
          </Text>
          
          </TouchableOpacity>
      </View>
      }
      keyExtractor = {(item,postId)=>item.postId}
  />
</View>
```
</div>
</details>

### 3. Data Parsing
- useEffect를 사용하여 Token 및 publicNotice를 Load
- REST API에서 Axios에서 Token을 붙여 데이터 요청
- 비동기를 사용하여 데이터를 받아올 때까지 대기
- 공지 목록을 성공적으로 불러오면 setPublicNotices 등록

<details>
<summary>Code</summary>
<div markdown="1">

```javascript
const [token,setToken] = useState('');
const [load,setLoad] = useState(false);

...

useEffect(()=>{
    const getToken = async () => {
        ...(Token 가져오기)...
        setToken(tkn);
    } 
    getToken();
},[]);

useEffect(()=>{
    getPublicNotices();
    setLoad(true);
},[token]);

const getPublicNotices = async () => {
    await axios.get((공지사항 내용)
    ).then((res) => {
        setPublicNotices(res.data);    //성공 시 setting
    }).catch((err) => {
        console.log("전체 공지 목록을 가져오는 데 실패했습니다.");
    });
}

```
</div>
</details>

## 구현에서 어려웠던 점
- `Axios`를 처음 사용해 보는 터라 사용법을 익히는 데 꽤 많은 시간 소요. Web에서 Parsing이 처음이라 어떤 형태로 데이터가 넘어오는지, 넘어온 데이터를 어떻게 Handling해서 출력시킬 수 있는지 오랜 시간이 걸림.
- `Hook`에 대해 오해하고 있던 부분이 있어(Class에서 사용하는 줄 알고 착각) Hook에 대해 다시 공부하고 사용법을 익혀 적용.
- 시간 값이 `Unix Timestamp` 값으로 넘어오는데 이 값을 다시 시간으로 바꾸어 주는 과정에서 애를 먹었다. timestamp2DateStr 함수를 제작해 값을 변경시켜 주었는데 변수를 date가 아닌 data라고 적는 바람에(...) undefined된 값으로 함수에 전달되어 시간낭비를 좀 했다.

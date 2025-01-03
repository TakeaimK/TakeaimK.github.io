---
layout: post
title: 20. Africa
categories:
  - Baekjoon
---

## 문제 원문 : [Baekjoon NO.15629 : Africa](https://www.acmicpc.net/problem/15629){: target="\_blank"}

### 문제 난이도 (solved.ac 기준) : Bronze I

### 문제 내용

![15629_Africa_1](/assets/images/Baekjoon/15629_Africa_1.PNG)  
![15629_Africa_2](/assets/images/Baekjoon/15629_Africa_2.PNG)  
![15629_Africa_3](/assets/images/Baekjoon/15629_Africa_3.PNG)  
![15629_Africa_4](/assets/images/Baekjoon/15629_Africa_4.PNG)  
![15629_Africa_5](/assets/images/Baekjoon/15629_Africa_5.PNG)

### 입력 1

```
3
ethiopia
kenya
tanzania
```

### 출력 1

```
150
```

### 문제 이해

문제가 매우 길고 대체 무엇을 출력하라는지 파악하려면, 일단 18개의 문단을 분석할 비문학 독해능력(...)이 필요해 보인다.  
먼저 출력값을 보아 하니, 일정이나 비자 비용에 관해 출력하는 것으로 보인다. 일정일 경우보다 비자 비용에 대한 내용이 좀 더 많이 보이므로 비자 비용에 대하여 계산하면서 문단을 분석하며 포인트를 찾아보자.

---

#### 5문단

```markdown
대행사를 통해 비자를 받는 경우 필요한 비용은 140달러로 매우 비싸기 때문에 현지에서 비자를 받는 것이 비용 측면에서는 유리하지만, 아프리카에서 한국인이 나미비아 비자를 받을 수 있는 곳은 매우 한정적이다."와 "많은 여행객들이 가는 지역 중에서는 남아프리카공화국의 케이프타운이 사실상 유일하기 때문에 경로 상 남아프리카공화국을 먼저 방문하지 않거나 케이프타운에서 비자가 발급될 때까지 충분히 머무를 수 없는 사람의 경우 한국에서 비자를 신청해야 한다. 만약 남아프리카공화국에서 비자를 받는 것이 가능하다면 그 비용은 40달러로 매우 저렴해진다.
```

> **나미비아** 입국 비자 _140\$_  
> **나미비아**를 갈 때 **남아공**을 거쳐 가면 _\$40_

#### 6문단

```markdown
예를 들어 케냐에 입국하려면 50달러를 내고 1회 입국이 가능한 비자를 발급받거나, 100달러를 내고 여러 번 입국이 가능한 비자를 받아야 한다.
```

> **케냐** 1회 입국 비자는 _\$50_, ~~여러 번 입국 가능 비자는 _\$100_~~  
> (1번씩만 방문함 -> 입력조건)

#### 7문단

```markdown
남아프리카공화국은 무비자 입국으로 30일 체류가 가능하며, 보츠와나는 90일 체류가 가능하다.
```

> **남아공**은 _무비자 30일_(Free)  
> **보츠와나**는 _무비자 90일_(Free)

#### 10문단

```markdown
짐바브웨의 경우 1회 입국 가능한 비자의 발급 비용이 30불, 2회 입국 가능한 비자는 45불이다. 잠비아는 1회 입국 가능한 비자가 50불, 2회 입국 가능한 비자가 80불이다.", " 다행히 이와 같이 방문하는 여행객들이 선택할 수 있는 옵션이 한 가지가 더 있는데, 잠비아-짐바브웨 연합 비자가 이에 해당한다. 이 비자를 발급받을 경우 지정된 기간 동안 짐바브웨와 잠비아 간을 제한 없이 방문할 수 있다. 단, 잠비아 혹은 짐바브웨가 아닌 다른 국가로 이동한 경우 비자는 유효하지 않게 된다. 이 비자를 발급받는 비용은 50불로, 두 국가를 모두 방문할 계획이 있는 여행객이라면 이를 발급받는 것이 유리하다. 따라서 국가별 방문 순서를 잘 정하면 비자 발급 비용을 절약할 수 있다. 그래서 국가를 방문하는 순서가 있을 때 총 비자 발급 비용을 구하려고 한다. 지금까지의 설명과 앞으로 적을 다른 국가 및 지역에 대한 소개를 조합하면 이를 해결하기 위한 충분한 정보를 얻을 수 있을 것이다. 이때 비용을 줄이기 위해 정해진 순서 중간에 다른 국가를 방문하는 것도 생각해볼 수 있겠지만 일단 여기에서는 생각하지 않기로 하자.
```

> **짐바브웨** 1회 입국 비자 _30\$_, ~~2회 입국 비자 _45\$_~~  
> (1번씩만 방문함 -> 입력조건)  
> **잠비아** 1회 입국 비자 _50\$_, ~~2회 입국 비자 _80\$_~~  
> (1번씩만 방문함 -> 입력조건)  
> **짐바브웨** <-> **잠비아** 시 _50\$_  
> (**짐바브웨** _30\$_ > **잠비아** _20\$_ / **잠비아** _50\$_ > **짐바브웨** _0\$_)

#### 12문단

```markdown
탄자니아 비자의 발급 비용은 $50이다. 단 여러 번 입국하기 위한 비자는 $100를 내고 발급이 가능하다.
```

> **탄자니아** 1회 입국 비자 _50\$_, ~~다회 입국 비자 _100\$_~~  
> (1번씩만 방문함 -> 입력조건)

#### 17문단

```markdown
에티오피아 역시 50달러를 내고 도착비자 발급이 가능하다.
```

> **에티오피아** 입국 비자 _50\$_

---

이제 문제를 간략히 정리해 보자.

|    국가    | 비용(\$) |       특이사항(\$)       |
| :--------: | :------: | :----------------------: |
|  나미비아  |   140    |    남아공 방문 시 40     |
|    케냐    |    50    |            X             |
|   남아공   |    0     |          무비자          |
|  보츠와나  |    0     |          무비자          |
|  짐바브웨  |    30    |  직전 잠비아 방문 시 0   |
|   잠비아   |    50    | 직전 짐바브웨 방문 시 20 |
|  탄자니아  |    50    |            X             |
| 에티오피아 |    50    |            X             |

~~읽고 분석하는 사이 코딩하기 귀찮아졌다~~  
이제 문제의 조건을 토대로 코딩을 해 보자.

### 소스 코드 (Python)

```python
def trip():

    cost = 0
    goSA = False
    goZam = False
    goZim = False
    num = int(input())

    for _ in range(num):
        country = input()

        if country == "botswana" :
            cost = cost+0
        if country == "ethiopia" :
            cost = cost+50
        if country == "kenya" :
            cost = cost+50
        if country == "tanzania" :
            cost = cost+50
        if country == "south-africa" :
            goSA = True
            cost = cost+0
        if country == "namibia" :
            if(goSA):
                cost+=40
            else:
                cost = cost+140
        if country == "zambia" :
            goZam = True
            if(goZim):
                cost = cost+20
            else:
                cost = cost+50
        if country == "zimbabwe" :
            goZim = True
            if(goZam):
                cost = cost+0
            else:
                cost = cost+30

        if country != "zambia" and country != "zimbabwe":
            goZam = False
            goZim = False
    return cost



if __name__ == "__main__":

    answer = 0

    answer = trip()

    print(answer)


```

### 소스 코드 (Java)

```java

```

### 소스 코드 (C++)

```cpp

```

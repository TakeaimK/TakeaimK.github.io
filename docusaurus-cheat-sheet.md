

이 문서는 Docusaurus에서 사용할 수 있는 특수 마크다운 기능들을 정리한 치트시트입니다.
글을 작성할 때 이 문서를 참고하여 복사/붙여넣기 하세요.

## 1. 탭 (Tabs)
여러 언어의 코드나 OS별 설정을 보여줄 때 사용합니다.
**주의:** 반드시 파일 상단이나 사용 직전에 `import` 구문이 있어야 합니다.
```python
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
```

<Tabs>
  <TabItem value="python" label="Python" default>

```python
print("Hello, AI World!")
```

</TabItem>
<TabItem value="js" label="JavaScript">

```javascript
console.log("Hello, Cloud World!");

```

</TabItem>
<TabItem value="bash" label="Terminal">

```bash
npm start

```

</TabItem>
</Tabs>

---

## 2. 강조 박스 (Admonitions)

독자의 주의를 환기시킬 때 사용합니다.

:::note 노트
이것은 일반적인 노트입니다. 부가 설명을 적을 때 좋습니다.
:::

:::tip 꿀팁
이 부분은 팁을 줄 때 사용합니다. (예: 단축키, 효율적인 방법)
:::

:::info 정보
추가적인 정보를 제공할 때 사용합니다.
:::

:::warning 주의사항
사용자가 주의해야 할 점을 적습니다. (예: 버전 호환성)
:::

:::danger 위험
치명적인 오류나 데이터 손실 위험이 있을 때 사용합니다.
:::

---

## 3. 코드 블록 꾸미기

코드 블록에 파일명과 하이라이트를 추가합니다.

* `title`: 파일 이름 표시
* `{숫자}`: 해당 라인 강조 (예: `{1, 3-5}`는 1번 줄과 3~5번 줄 강조)

```python title="train_model.py" {3,6-7}
import torch
import torch.nn as nn

# 이 아래 함수가 중요합니다 (하이라이트 예시)
def get_model():
    model = nn.Linear(10, 1)
    return model

print("Model Loaded")

```

---

## 4. 접기/펼치기 (Details)

로그 파일이나 긴 정답을 숨겨둘 때 사용합니다.

<details>
<summary>클릭하여 아주 긴 에러 로그 보기</summary>

```bash
Error: Connection Refused
at /lib/network.js:120
at /lib/core.js:50
... (생략된 긴 내용) ...

```

</details>

---

## 5. 수식 (LaTeX)

AI/수학 공식을 표현합니다. (플러그인 설정 필요)

**인라인 수식:** 문장 중간에  $E=mc^2$ 처럼 사용합니다.

블록 수식:
$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

행렬 예시:
$$A = \begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}$$
---

## 6. 이미지 및 에셋

`static` 폴더에 이미지를 넣고 아래와 같이 경로를 지정합니다.
(`static` 글자는 경로에서 제외합니다)

*이미지 크기 조절이 필요하면 HTML 태그를 사용하세요:*
<img src="https://docusaurus.io/img/docusaurus_keytar.svg" alt="drawing" width="200"/>

```

```
---
slug: first-ai-study
title: 나의 첫 번째 AI 학습 기록
authors: [me]
tags: [Daily]
date: 2026-01-10
---

여기는 **요약(Summary)** 부분이 들어갑니다.
블로그 목록에서 미리보기로 보여지는 부분입니다.

# 서론
Docusaurus로 블로그를 만들었습니다. 앞으로 AI와 Cloud 학습 내용을 정리할 예정입니다.

## 1. 코드 블록 테스트
AI 모델링에 자주 쓰이는 Python 코드 예시입니다.

```python title="model.py"
import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 1)

    def forward(self, x):
        return self.linear(x)

print("Model Loaded!")

```

$$
I = \int_0^{2\pi} \sin(x)\,dx
$$
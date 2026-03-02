---
slug: openclaw-사용을-위한-삽질기록
title: "[AI] OpenClaw 사용을 위한 삽질 기록"
authors: [me]
tags: [openclaw, lmstudio, ollama, ai, troubleshooting]
---

최근 AI 에이전트 도구인 **OpenClaw**를 환경에 맞게 구축하면서 정말 많은 시행착오를 겪었는데요. 오늘은 제가 로컬 환경(LM Studio)과 외부 백업 서버(Ollama API)를 연동해 가며 OpenClaw를 쫀득하게 길들였던 '권장 설정 및 트러블슈팅 삽질기'를 공유해 봅니다. 

<!--truncate-->

## 0. 현재 저의 서빙 환경 소개 (Environment Context)

본격적인 문제 해결에 앞서, 어떤 상황에서 이런 삽질(...)이 시작되었는지 가볍게 설명해 드릴게요.

* **메인 서빙 (Local)**: RTX 5060Ti 16GB VRAM 데스크탑 
* **모델**: `unsloth/qwen3.5-35b-a3b` (IQ2_M 양자화) - LM Studio 사용 
* **백업 플랜 (Fallback)**: `https://***/v1` 의 외부 망 Ollama API 서버

평소에는 로컬과 외부 Ollama 서버를 혼용해서 썼지만, **현재 백업 플랜인 Ollama 서버가 유지보수 중**이라 로컬 VRAM(16GB)으로 온전히 버텨야 하는 제한적인 상황이었습니다. 

자, 그럼 이 환경에서 겪었던 주요 이슈와 그 해결 과정을 하나씩 짚어보겠습니다.

---

## 1. 응답이 뚝뚝 끊기는 현상 (Streaming Chunk Issue)

### 📌 1. 무엇을 원했는가?
질문을 던지면 LM Studio 측에서 토큰이 생성되고 있을 텐데, OpenClaw 화면에서는 응답이 안 오다가 마지막에 한꺼번에 채팅이 쏟아져 나오는 현상이 있었습니다. 이 과정을 **실시간으로 자연스럽게 생성(Streaming)**되도록 만들고 싶었어요.

### 🛠️ 2. 어떻게 조치했는가?
LM Studio쪽 스트리밍 문제가 아닌 탓을 파악하고, `openclaw.json` 내의 에이전트 스트리밍 설정을 다음과 같이 수정했습니다. `blockStreamingBreak` 속성을 `"text_end"` (텍스트 청크 단위 전송)로 변경했습니다.

<details>
<summary>📄 (클릭) openclaw.json 수정 내용</summary>

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on",
      "blockStreamingBreak": "text_end",
      "blockStreamingChunk": {
        "minChars": 200,
        "maxChars": 1500,
        "breakPreference": "paragraph"
      }
    }
  }
}
```
</details>

#### ✨ 시도 요약
LM Studio 자체 GUI에서 스트리밍 옵션을 찾았으나 원인이 아님을 알게 되었습니다. 문제는 OpenClaw가 문장이 끝날 때까지 버퍼링하는 기본 설정(`message_end`) 때문이었습니다. 설정 파일 수정 시 `blockStreamingChunk` 객체 괄호(`{}`) 위치를 잘못 지정해 JSON 포맷 오류 에러가 떴었고, 괄호 쌍을 올바르게 맞추며 해결했습니다.

---

## 2. Slack 연동하기 (Slack Integration)

### 📌 1. 무엇을 원했는가?
OpenClaw를 Slack과 연동하여, 언제 어디서나 메신저를 통해 에이전트와 대화하고 싶었습니다. 외부 포트포워딩 없이 사내/개인 PC에서도 안정적인 연결이 필요했습니다.

### 🛠️ 2. 어떻게 조치했는가?
Slack App을 생성하고 **Socket Mode**를 통해 연동했습니다. 이렇게 하면 고정/공인 IP 없이도 동작합니다.
1. Slack API에서 앱 생성 후 `Socket Mode` 활성화 (App Token 발급: `xapp-***`)
2. 웹소켓용 권한 Scope 부여 후 워크스페이스 설치 (Bot Token 발급: `xoxb-***`)
3. `openclaw.json` 채널 설정에 발급받은 두 가지 Token을 추가

<details>
<summary>📄 (클릭) openclaw.json - Slack 설정</summary>

```json
"channels": {
    "slack": {
      "enabled": true,
      "mode": "socket",
      "appToken": "xapp-***",
      "botToken": "xoxb-***",
      "dmPolicy": "pairing",
      "groupPolicy": "open",
      "streaming": true,
      "textChunkLimit": 4000,
      "chunkMode": "newline"
    }
}
```
</details>

#### ✨ 시도 요약
Slack 연동 자체는 공식 문서대로 무난히 처리했습니다. 다만, 연결 완료 후에도 Slack에서 이전 세션 모델(qwen 27b)이 계속 매핑된 상태로 잡혀있어 응답 거부 에러가 났습니다. 이를 해결하기 위해 슬랙에서 명령어 `new` 혹은 `reset`을 전송해 세션을 초기화시켜 해결했습니다. (주의: 슬래시 명령어 `/new`는 Slack 자체 명령어와 충돌하여 텍스트 형태로 전송)

---

## 3. Ollama 서버로 인한 응답 지연 (API Timeout Fallback)

### 📌 1. 무엇을 원했는가?
LM Studio 로컬 모델을 primary로 사용함에도 질문 답변이 한참 걸리는 현상이 있었습니다. 확인해보니 유지보수 중인 외부 Ollama API 서버 쪽으로 모델 디스커버리를 시도하느라 계속 `TimeoutError`가 발생해 발목을 잡고 있었습니다. 이 딜레이를 없애고 싶었습니다.

### 🛠️ 2. 어떻게 조치했는가?
`openclaw.json`의 `fallbacks` 기능에서 Ollama 서버 관련 코드를 일시적으로 `//` 블록 주석 처리했습니다. 

```json
// "fallbacks": [
//   "ollama/qwen3.5:122b"
// ]
```

#### ✨ 시도 요약
에이전트는 주기적으로 모든 등록된 모델 프로바이더(Ollama 등) 상태를 체크합니다. 주석 처리하여 에러 로그 빈도를 낮췄고, 추가로 세션에서 이전 캐싱 데이터가 남아있는 문제를 해결하기 위해 CLI 환경으로 세션 백업본 이동(`mv ~/.openclaw/agents/main/sessions.bak`)과 `openclaw status` 점검을 거쳤습니다.

---

## 4. 서브에이전트 컨텍스트 크기 이슈 & VRAM 튜닝 (VRAM & Context Limit)

### 📌 1. 무엇을 원했는가?
서브에이전트가 리서치 작업을 맡을 때마다 컨텍스트 오버플로우가 나며 뻗어버렸습니다. 저는 RTX 5060Ti 16GB VRAM을 가지고 있어 65,536 컨텍스트를 사용 중이었는데 여유 메모리로 **생성 속도를 희생하지 않고 컨텍스트 크기만 더 늘리고** 싶었습니다.

### 🛠️ 2. 어떻게 조치했는가?
LM Studio에서 **KV 캐시 양자화(K/V Cache Quantization Type)**를 `Q8_0`으로 켰습니다! 
이 설정 하나로 모델 가중치는 그대로인 채 컨텍스트를 **131,072(128k)**까지 끌어올릴 수 있었습니다.

<details>
<summary>🔽 (클릭) VRAM 최적화 관련 기타 설정</summary>

*   **Context Length**: 65,536 ➡️ 131,072
*   **Max Concurrent Predictions**: 4 ➡️ 2 (컨텍스트 확장 시 OOM 방지)
*   **OpenClaw 설정 최적화**: `softThresholdTokens`를 128k 규모에 맞게 기존 4000에서 8000으로 조정

```json
"memoryFlush": {
  "enabled": true,
  "softThresholdTokens": 8000,
  "systemPrompt": "Session nearing compaction. Store durable memories now.",
}
```
</details>

#### ✨ 시도 요약
비싼 VRAM을 아끼기 위해 모델 양자화 버전을 낮출까 고민했지만, 다행히 `Qwen3.5-35B-A3B` 모델은 전체 중 일부 레이어만 전통적인 KV 캐시가 필요한 구조입니다. `Q8_0` 양자화면 큰 화질의 열화 없이 16GB 내에서 128k 환경을 커버할 수 있었습니다. 쓸데없는 `hardThresholdPct` 파라미터 등을 JSON에 넣었다가 에러가 나기도 했었는데 유효한 `softThresholdTokens` 값만 수정하여 정리했습니다.

---

## 5. 서브에이전트 타임아웃 & 무한 대기 수렁 (Sub-agent Control)

### 📌 1. 무엇을 원했는가?
위 VRAM 조치로 컨텍스트 용량은 넉넉해졌지만, 서브에이전트에게 리서치와 교안 작성을 지시하면 여전히 타임아웃 오류(`Subagent main timed out`)와 함께 작업을 멈췄습니다. 작업 실패 없이 안정적으로 완수하게 하고 싶었습니다.

### 🛠️ 2. 어떻게 조치했는가?
문제는 **1) 서브에이전트의 기본 타임아웃(180초)이 너무 짧았고, 2) 브레이브 API 키가 없는데도 없는 도구에 집착**한 것이었습니다.
따라서, 프롬프트(명령) 자체에 강력하게 룰과 도구를 정해주고, 단계를 분리하여 요청했습니다.

> "리서치는 `duckduckgo_search` 스킬만 사용해(Brave API 쓰지 마). 서브에이전트 `runTimeoutSeconds`를 900(15분)으로 맞춰줘. `web_fetch`는 3회로 강제로 제한해."

#### ✨ 시도 요약
JSON 설정 파일에 `runTimeoutSeconds: 900`을 명시했으나, LM 모델 자체가 `sessions_spawn` (자식 프로세스 실행) 시 명시적으로 권한을 무시하고 180초로 강제 할당하는 증상이 발견되었습니다. 이를 위해 `TOOLS.md`나 프롬프트에 직접 타임아웃 및 Fetch 횟수를 제한하여, 서브에이전트의 컨텍스트 비대화를 막고 물리적인 수행 과정을 정상화시켰습니다.

---

## 6. WSL 환경에서 바탕화면 경로 바로 지정 (WSL File Export)

### 📌 1. 무엇을 원했는가?
마지막으로, 생성된 결과물 파일이나 교안을 "바탕화면에 저장해 줘" 한마디로 바로 제 PC 바탕화면으로 파일이 똑 떨어지게 만들고 싶었습니다. 저는 윈도우 환경 위에 WSL 가상 머신을 올려 쓰고 있어서 경로가 특이합니다.

### 🛠️ 2. 어떻게 조치했는가?
OpenClaw 설정 파일 중 `USER.md`와 `TOOLS.md`에 WSL(Windows Subsystem for Linux) 마운트 변환 경로인 `/mnt/c/Users/***/Desktop`를 추가했습니다. 

```markdown
## 파일 저장 기본 경로
- 윈도우 바탕화면 경로: `/mnt/c/Users/***/Desktop`
- "바탕화면에 저장해줘"라고 명령이 오면 위 경로를 기본으로 사용할 것
```

#### ✨ 시도 요약
단순히 `C:\` 경로를 지정하면 WSL 내의 리눅스 샌드박스에서 인식하지 못하기 때문에 어떻게 환경 경로를 주입할지 고민했습니다. 루트 수준의 설정 파일인 `USER.md` (사용자 톤앤매너 규칙) 와 `TOOLS.md` (로컬 툴, 경로 환경)에 해당 설정을 못 박아 둠으로써 번거로운 타이핑 없이 매끈하게 파일을 생성해 낼 수 있었습니다!

---

## 🌟 마치며 (Conclusion)

생각보다 "설정이 복잡했죠?" 거의 다 했습니다! OpenClaw를 구성하며 겪었던 스트리밍 딜레이부터, VRAM 컨텍스트 한계 돌파, 타임아웃 서브에이전트 다루기, 이 기나긴 삽질 로그들이 여러분의 환경 셋업에도 큰 도움이 되었으면 좋겠습니다. 특히 넉넉지 않은 하드웨어에서는 옵션 하나하나가 엄청난 속도 개선을 가져다 주니까요!

---

**검증 환경 (Verification Environment)**
* **OS**: Windows (WSL2 백엔드)
* **GPU**: NVIDIA RTX 5060Ti (16GB VRAM)
* **Serving**: LM Studio (Local), OpenClaw (Agent Framework)
* **LLM**: `unsloth/qwen3.5-35b-a3b.GGUF` (IQ2_M)

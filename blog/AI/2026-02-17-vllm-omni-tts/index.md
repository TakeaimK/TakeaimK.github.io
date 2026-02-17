---
slug: vllm-omni-tts
title: "[AI] vLLM-omni와 Qwen3-TTS로 나만의 한국어 TTS 서버 만들기"
authors: [me]
tags: [k3s, vllm, tts, qwen, uv, infra]
date: 2026-02-17
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

> **요약:** 최신 멀티모달 인퍼런스 엔진인 **vLLM-omni**와 **Qwen3-TTS** 모델을 사용하여 한국어 음성 합성 서비스를 구축하는 방법을 다룹니다. Python **uv**를 활용한 로컬 테스트부터 `k3s` 클러스터에 **vLLM** 서비스를 배포하는 과정까지 상세히 가이드합니다.

---

## 1. 들어가며 (Introduction)

안녕하세요! 오늘은 텍스트를 입력하면 사람처럼 자연스러운 목소리로 읽어주는 **TTS(Text-to-Speech)** 서비스를 직접 구축해 보려 합니다.

최근 **Qwen(Alibaba Cloud)** 팀에서 공개한 `Qwen3-TTS`는 단순한 음성 합성을 넘어, 텍스트의 문맥을 이해하고 감정(Emotion)과 억양(Tone)까지 조절할 수 있는 강력한 기능을 자랑합니다. 게다가 **vLLM-omni**를 사용하면 이 무거운 모델을 빠르고 효율적으로 서빙할 수 있죠.

이번 포스팅에서는 다음 두 가지를 목표로 합니다.
1.  **Qwen3-TTS**의 강력한 기능(Custom Voice, Emotion Control)을 파헤치고,
2.  이를 **k3s + vLLM** 환경에 배포하여 나만의 안정적인 TTS 서버를 만드는 것입니다.

<!--truncate-->

---

## 2. Qwen3-TTS 모델 살펴보기 (Model Overview)

우리가 사용할 모델은 **[Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)** 입니다.

### 2.1 주요 특징
*   **다국어 지원**: 한국어를 포함해 영어, 중국어, 일본어 등 10개 주요 언어를 유창하게 구사합니다.
*   **Custom Voice**: 사전 정의된 고품질 페르소나(Speaker)를 선택하여 다양한 목소리를 낼 수 있습니다.
*   **지시문(Instruct) 제어**: "화난 목소리로", "빠르게", "슬프게"와 같은 자연어 지시를 통해 발화 스타일을 조절할 수 있습니다.
*   **스트리밍 지원**: vLLM-omni와 결합하여 끊김 없는 실시간 대화가 가능합니다.

### 2.2 핵심 옵션 및 사용법

`generate_custom_voice` 함수를 사용할 때 주요 파라미터는 다음과 같습니다.

| 파라미터 | 설명 | 예시 |
| :--- | :--- | :--- |
| `text` | 음성으로 변환할 텍스트 | `"안녕하세요, 반가워요!"` |
| `speaker` | 발화자 페르소나 (지원 목록에서 선택) | `"Vivian"`, `"Ryan"` 등 (모델 지원 목록 참고) |
| `instruct` | 감정이나 톤을 지시하는 자연어 프롬프트 | `"밝고 명랑한 톤으로 말해줘"` |
| `language` | 발화 언어 지정 (Auto 가능) | `"Korean"`, `"English"` |

> **Tip:** 지원하는 스피커 목록은 코드상에서 `model.get_supported_speakers()`를 호출하여 확인할 수 있습니다. 모델명에 'CustomVoice'가 붙은 경우, 프리셋 된 고품질 스피커를 사용하는 것이 일반적입니다.

### 2.3 Qwen3-TTS 모델 라인업 (Model Variants)

Qwen3-TTS는 사용 목적에 따라 세 가지 특화된 모델을 제공합니다. (공식 문서 기준)

*   **CustomVoice (추천)**:
    *   **특징**: 9개의 프리미엄 음색(Speaker)이 내장되어 있습니다. (성별, 연령, 언어, 방언별 조합)
    *   **강점**: 사용자가 제공하는 텍스트 지시문(Instruct)을 통해 말하기 속도, 감정, 톤 등을 미세하게 조정할 수 있습니다. 
    *   **용도**: 가장 안정적이고 고품질의 TTS 서비스가 필요할 때 사용합니다. (이번 실습 대상)
*   **VoiceDesign**:
    *   **특징**: 기존에 없는 목소리를 **텍스트 프롬프트만으로 창조**합니다.
    *   **강점**: "굵고 낮은 목소리의 중년 남성", "활기찬 어린아이" 등 원하는 목소리 특징을 자연어 문장으로 묘사하면, 그에 맞는 새로운 화자를 즉석에서 생성합니다.
*   **Base**:
    *   **특징**: 특정 화자에 얽매이지 않은 **파운데이션 모델**입니다.
    *   **강점**: 3초 정도의 짧은 오디오 샘플만 있어도 목소리를 복제하는 **제로샷(Zero-shot) 음성 복제** 기능에 탁월합니다. 또한 특정 도메인 데이터로 파인튜닝하기 위한 베이스 모델로도 활용됩니다.

---

## 3. 사전 준비 (Prerequisites)

실습을 위해 다음 도구들이 설치되어 있어야 합니다.

*   **Docker & NVIDIA Container Toolkit**: GPU 사용을 위해 필수입니다.
*   **uv**: 빠르고 간편한 Python 패키지 관리자입니다.
*   **Kubernetes (k3s)**: wsl 환경 내에 k3s가 구축된 상태여야 합니다.

---

## 4. 로컬 테스트: uv로 Qwen3-TTS 맛보기

서버에 올리기 전에, 로컬에서 `uv`를 사용해 간단히 모델을 테스트해 보겠습니다.

### 4.1 프로젝트 초기화

만약 `uv`가 설치되어 있지 않다면(`Command 'uv' not found`), 다음 공식 설치 명령어를 실행하여 설치해주세요.

```bash
# uv 설치 (Linux/macOS/WSL)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env 2> /dev/null || source $HOME/.cargo/env # 환경변수 적용
```

설치가 완료되었다면 프로젝트 폴더를 만들고 초기화합니다.

> **Warning:** 프로젝트 폴더나 이름을 `qwen-tts`로 지정하면 안 됩니다! 패키지 이름과 충돌하여 설치 에러(`Requirement name matches project name`)가 발생합니다. 반드시 `qwen-tts-demo` 처럼 다른 이름을 사용하세요.

> **Note:** `uv init` 명령어는 프로젝트 설정 파일(`pyproject.toml`)만 생성합니다. 가상환경 폴더(`.venv`)를 생성하려면 `uv venv` 명령어를 추가로 실행하거나 패키지를 추가해야 합니다.

```bash
mkdir qwen-tts-demo
cd qwen-tts-demo

# 1. 프로젝트 초기화 (이름 충돌 방지)
uv init --name qwen-tts-demo --python 3.12
uv python pin 3.12  #uv python 기본 버전이 구버전인 경우 패키지 버전 충돌 방지

# 2. 가상환경(.venv) 생성 및 활성화
uv venv
source .venv/bin/activate
```

### 4.2 패키지 설치

Qwen 팀에서 제공하는 공식 패키지인 `qwen-tts`와 관련 의존성을 설치합니다.
(Linux/WSL 환경에서는 오디오 처리를 위해 `sox` 패키지가 시스템에 설치되어 있어야 합니다.)

```bash
# 1. 시스템 라이브러리 설치 (SoX 필수)
sudo apt update && sudo apt install -y sox libsox-dev

# 2. Python 패키지 설치
uv add qwen-tts torch soundfile transformers

# 3. (권장) GPU 가속을 위한 FlashAttention 2 설치
uv pip install flash-attn --no-build-isolation
```

### 4.3 Python 테스트 코드 작성 (3가지 모델 실습)

Qwen3-TTS의 강력한 기능인 **CustomVoice**, **VoiceDesign**, **Base(Clone)** 3가지 모델을 모두 체험해 볼 수 있는 종합 스크립트(`tts.py`)를 작성합니다.

> **주의:** 3개의 모델을 한 번에 모두 로드하면 GPU 메모리(VRAM)가 부족할 수 있습니다. `Run inference` 부분에서 주석을 해제하여 하나씩 실행하는 것을 권장합니다.

<details>
<summary>📄 <strong>(클릭) tts.py 전체 코드</strong></summary>

```python title="tts.py"
import sys
import os
import torch
import soundfile as sf
import re
from datetime import datetime
from qwen_tts import Qwen3TTSModel

# -----------------------------------------------------------------------------
# [초기 설정] GPU 및 FlashAttention 설정
# -----------------------------------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32
attn_impl = "eager"

if device == "cuda":
    try:
        import flash_attn
        attn_impl = "flash_attention_2"
    except ImportError:
        print("⚠️ FlashAttention이 설치되지 않아 'eager' 모드로 실행합니다.")

# -----------------------------------------------------------------------------
# [모델 경로 설정]
# -----------------------------------------------------------------------------
MODELS = {
    "custom": "/mnt/c/Users/csj76/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    "design": "/mnt/c/Users/csj76/models/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    "clone": "/mnt/c/Users/csj76/models/Qwen/Qwen3-TTS-12Hz-1.7B-Base"
}

def load_model(path, model_name_for_log):
    print(f"\n[{model_name_for_log}] 모델 로딩 중... ({path})")
    return Qwen3TTSModel.from_pretrained(
        path,
        device_map="auto",
        dtype=dtype,
        attn_implementation=attn_impl
    )

def get_output_filename(type_str, identifier):
    """
    파일명 생성 규칙: output-<type>-<identifier>-<YYMMDDHHMM>.wav
    - identifier: 공백 및 특수문자는 '_'로 치환
    - timestamp: 현재 시간
    """
    # 1. Identifier 정제 (파일명에 사용할 수 없는 문자 및 공백, 특수문자 치환)
    # 한글, 영문, 숫자, 언더바, 하이픈을 제외한 모든 문자를 '_'로 변경
    clean_identifier = re.sub(r'[^가-힣a-zA-Z0-9_\-]', '_', str(identifier))
    # 연속된 언더바는 하나로 줄임
    clean_identifier = re.sub(r'_+', '_', clean_identifier)
    
    # 2. 날짜 포맷 (YYMMDDHHMM)
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    
    return f"output-{type_str}-{clean_identifier}-{timestamp}.wav"

# -----------------------------------------------------------------------------
# [기능 구현]
# -----------------------------------------------------------------------------

def run_custom_voice(text, speaker):
    """
    1. CustomVoice: 프리셋 화자 사용
    """
    model = load_model(MODELS["custom"], "CustomVoice")
    
    # 기본 instruct (필요하다면 상수로 빼거나 인자로 받을 수 있음)
    default_instruct = "차분하고 전문적인 뉴스 앵커 톤으로(Speak in a calm and professional news anchor tone)"
    
    print(f"🎙️ 생성 중: '{text}' (Speaker: {speaker})")
    
    wavs, sr = model.generate_custom_voice(
        text=text,
        language="Korean",
        speaker=speaker,
        instruct=default_instruct
    )
    
    # output-custom_voice-<Speaker>-<Date>.wav
    output_filename = get_output_filename("custom_voice", speaker)
    
    sf.write(output_filename, wavs[0], sr)
    print(f"✅ 완료: {output_filename}")

def run_voice_design(text, instruct):
    """
    2. VoiceDesign: 목소리 묘사 사용
    """
    model = load_model(MODELS["design"], "VoiceDesign")
    
    print(f"🎙️ 생성 중: '{text}'")
    print(f"✨ 목소리 묘사: {instruct}")
    
    wavs, sr = model.generate_voice_design(
        text=text,
        language="Korean",
        instruct=instruct
    )
    
    # output-voice_design-<Instruct앞10글자>-<Date>.wav
    # instruct가 길 수 있으므로 앞 10글자만 사용
    short_instruct = instruct[:10]
    output_filename = get_output_filename("voice_design", short_instruct)
    
    sf.write(output_filename, wavs[0], sr)
    print(f"✅ 완료: {output_filename}")

def run_voice_clone(text, ref_audio_path, ref_text=None):
    """
    3. VoiceClone: 목소리 복제
    """
    model = load_model(MODELS["clone"], "VoiceClone")
    
    # ref_text가 제공되지 않았을 경우 (CLI 모드 등에서)
    if not ref_text:
        print("\nℹ️  참조 오디오의 텍스트(Transcript)가 입력되지 않았습니다.")
        ref_text = input("   복제 품질을 위해 참조 오디오의 내용을 입력해주세요 (모르면 Enter): ").strip()
        if not ref_text:
            print("⚠️  Warning: 참조 텍스트 없이 진행합니다. 품질이 저하될 수 있습니다.")
            # 텍스트가 꼭 필요하다면 임의의 값이나 에러 처리가 필요할 수 있습니다.
            # 여기서는 빈 문자열이나 플레이스홀더를 사용하여 진행 시도
            ref_text = "The quick brown fox jumps over the lazy dog." 
    
    print(f"🎙️ 생성 중: '{text}'")
    print(f"🔊 참조 파일: {ref_audio_path}")
    
    wavs, sr = model.generate_voice_clone(
        text=text,
        language="Korean",
        ref_audio=ref_audio_path,
        ref_text=ref_text
    )
    
    # output-voice_clone-<RefFileName>-<Date>.wav
    # 경로에서 파일명 추출 (확장자 제외)
    base_name = os.path.basename(ref_audio_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    
    output_filename = get_output_filename("voice_clone", file_name_without_ext)

    sf.write(output_filename, wavs[0], sr)
    print(f"✅ 완료: {output_filename}")

# -----------------------------------------------------------------------------
# [메인 로직]
# -----------------------------------------------------------------------------

def print_help():
    print("""
[사용법] python tts.py [모드번호] [인자...]

1. Custom Voice (프리셋)
   사용법: python tts.py 1 "변환할 텍스트" [프리셋이름 (기본값: Sohee)]
   예시:   python tts.py 1 "안녕하세요" Aiden

2. Voice Design (목소리 묘사)
   사용법: python tts.py 2 "변환할 텍스트" "목소리 묘사"
   예시:   python tts.py 2 "안녕하세요" "귀여운 한국인 여자아이 목소리"

3. Voice Clone (목소리 복제)
   사용법: python tts.py 3 "변환할 텍스트" "목소리 파일 경로"
   예시:   python tts.py 3 "안녕하세요" "./my_voice.wav"

* 인자 없이 실행 시 대화형 모드로 실행됩니다.
""")

def main():
    args = sys.argv[1:]
    
    # 1. 인자가 없는 경우 -> 대화형 모드
    if len(args) == 0:
        print("\n=== Qwen3 TTS 대화형 모드 ===")
        print("1. Custom Voice (프리셋 선택)")
        print("2. Voice Design (목소리 묘사)")
        print("3. Voice Clone  (목소리 복제)")
        
        mode = input("\n원하는 모드를 선택하세요 (1/2/3): ").strip()
        
        if mode == "1":
            t = input("변환할 텍스트: ").strip()
            s = input("원하는 프리셋 (기본값 Sohee): ").strip()
            if not s: s = "Sohee"
            run_custom_voice(t, s)
            
        elif mode == "2":
            t = input("변환할 텍스트: ").strip()
            i = input("원하는 목소리 묘사: ").strip()
            run_voice_design(t, i)
            
        elif mode == "3":
            t = input("변환할 텍스트: ").strip()
            p = input("참조 오디오 경로: ").strip()
            # 대화형에서는 명시적으로 받음
            r = input("참조 오디오의 텍스트 내용: ").strip()
            run_voice_clone(t, p, r)
            
        else:
            print("잘못된 입력입니다.")
            
    # 2. 인자가 있는 경우 -> CLI 모드
    else:
        mode = args[0]
        
        if mode == "1":
            # python tts.py 1 "text" "speaker"
            if len(args) < 2:
                print("❌ 텍스트 인자가 필요합니다.")
                print_help()
                return
            
            text = args[1]
            speaker = args[2] if len(args) > 2 else "Sohee"
            run_custom_voice(text, speaker)
            
        elif mode == "2":
            # python tts.py 2 "text" "instruct"
            if len(args) < 3:
                print("❌ 텍스트와 묘사 인자가 필요합니다.")
                print_help()
                return
                
            text = args[1]
            instruct = args[2]
            run_voice_design(text, instruct)
            
        elif mode == "3":
            # python tts.py 3 "text" "path"
            if len(args) < 3:
                print("❌ 텍스트와 파일 경로 인자가 필요합니다.")
                print_help()
                return
                
            text = args[1]
            path = args[2]
            # CLI 모드에서는 ref_text를 인자로 받지 않기로 했으므로 내부에서 처리(None 전달)
            run_voice_clone(text, path, ref_text=None)
            
        else:
            print_help()

if __name__ == "__main__":
    main()
```

</details>


### 4.4 실행 및 확인

```bash
uv run tts.py
```

스크립트를 실행하면 `output-custom_voice-...wav` 형태의 파일이 생성됩니다. 다른 모델도 체험해보고 싶다면 코드의 마지막 부분(CLI 인자 또는 대화형 모드)을 활용해보세요.

> **Note:** Base 모델의 `ref_audio`에 본인의 목소리 파일(wav/mp3) 경로를 넣으면, AI가 내 목소리로 말하는 신기한 경험을 할 수 있습니다!

> **Note:** 로컬 실행은 개발 및 테스트 목적에는 좋지만, 모델 로딩 시간이 매번 소요되므로 비효율적입니다. 따라서 실서비스를 위해서는 아래와 같이 **vLLM 서버** 형태로 띄워두고 API를 호출하는 방식이 필수적입니다.

---

## 5. k3s에 vLLM-omni 배포하기 (Serving Setup)

이제 Qwen3-TTS를 위한 매니페스트를 작성하겠습니다. (블로그의 k3s vLLM 서빙 가이드 문서 참조)

### 5.1 Deployment Manifest 작성

`vllm-tts.yaml` 파일을 생성합니다.

<details>
<summary>📄 <strong>(클릭) vllm-tts.yaml 파일 전체 보기</strong></summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-tts
  namespace: llm-serving
  labels:
    app: vllm-tts
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-tts
  template:
    metadata:
      labels:
        app: vllm-tts
    spec:
      runtimeClassName: nvidia  # GPU 사용 필수
      hostIPC: true             # vLLM 성능을 위해 공유 메모리 사용
      containers:
        - name: vllm-omni
          # vLLM-omni 전용 이미지 사용 (Qwen3-TTS 지원)
          image: vllm/vllm-omni:latest
          resources:
            limits:
              nvidia.com/gpu: 1
              memory: "16Gi"
            requests:
              nvidia.com/gpu: 1
              memory: "8Gi"
          env:
            - name: HUGGING_FACE_HUB_TOKEN
              value: "hf_YOUR_TOKEN_HERE" # 토큰 입력 필요
            # WSL2 환경 필수 설정 (GPU 드라이버 패스스루)
            - name: LD_LIBRARY_PATH
              value: "/usr/lib/wsl/lib:/usr/lib/wsl/drivers/nvmdsi.inf_amd64_83eb34a6b09136c0:/usr/local/nvidia/lib64:/usr/local/cuda/lib64"
          args:
            - serve
            - Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
            - --omni
            - --port=8000
            - --host=0.0.0.0
            - --gpu-memory-utilization=0.9
            - --max-model-len=8192
            - --trust-remote-code
          ports:
            - containerPort: 8000
              name: http
          volumeMounts:
            - name: hf-cache
              mountPath: /root/.cache/huggingface
      volumes:
        - name: hf-cache
          hostPath:
            path: /root/.cache/huggingface
            type: DirectoryOrCreate
---
apiVersion: v1
kind: Service
metadata:
  name: vllm-tts-service
  namespace: llm-serving
spec:
  selector:
    app: vllm-tts
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

</details>

#### 📄 파일 상세 설명
*   **Image**: `vllm/vllm-omni:latest`를 사용했습니다. 일반 vLLM 이미지보다 오디오/TTS 처리에 최적화된 포크(Fork) 또는 모듈을 포함하고 있습니다.
*   **Args**:
    *   `--omni`: 멀티모달(음성 입출력) 기능을 활성화하는 플래그입니다.
    *   `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`: 사용할 모델 ID입니다.
*   **RuntimeClassName**: `nvidia`를 지정하여 파드가 GPU에 접근할 수 있게 합니다.

### 5.2 Ingress 설정 (선택 사항)

매번 포트 포워딩을 하기 귀찮다면 Ingress를 설정합니다. `vllm-tts-ingress.yaml`을 작성합니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vllm-tts-ingress
  namespace: llm-serving
spec:
  ingressClassName: traefik
  rules:
    - host: localhost
      http:
        paths:
          - path: /tts
            pathType: Prefix
            backend:
              service:
                name: vllm-tts-service
                port:
                  number: 80
```

### 5.3 배포 및 확인

```bash
kubectl apply -f vllm-tts.yaml
# Ingress 사용 시
kubectl apply -f vllm-tts-ingress.yaml

# 파드 상태 확인 (Running이 뜰 때까지 대기)
kubectl get pods -n llm-serving -w
```

---

## 6. 클라이언트 제작 및 테스트 (Client Implementation)

서버가 준비되었으니, 실제로 요청을 보내 한국어 음성을 생성해 봅시다. Python의 `openai` 라이브러리를 사용해 API 표준에 맞춰 요청할 수 있습니다.

### 6.1 클라이언트 코드 작성 (`tts_client.py`)

```python title="tts_client.py"
from openai import OpenAI
import os

# k3s Ingress 주소 (또는 포트포워딩 주소)
# Ingress 사용 시: http://localhost/tts/v1
# 포트포워딩 사용 시: http://localhost:8000/v1
client = OpenAI(
    base_url="http://localhost:8000/v1",  # 상황에 맞게 수정하세요
    api_key="EMPTY"
)

def create_korean_voice(text, filename="korean_voice.wav"):
    print(f"🎙️ 음성 생성 중: '{text}'")
    
    try:
        response = client.audio.speech.create(
            model="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
            voice="Vivian", # 💡 중요: 화자 페르소나 선택
                            # 지원되지 않는 이름일 경우 기본 화자로 대체될 수 있습니다.
            input=text,
            # 추가적인 instruct가 필요하다면 API 규격에 따라 extra_body 등에 포함할 수 있습니다.
        )
        
        # 파일 저장
        response.stream_to_file(filename)
        print(f"✅ 생성 완료! 저장된 파일: {filename}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 포트포워딩이 필요하다면 먼저 실행하세요:
    # kubectl port-forward svc/vllm-tts-service 8000:80 -n llm-serving
    
    script = "안녕하세요! Qwen3 TTS 모델을 통해 생성된 한국어 음성입니다. 목소리가 자연스러운가요?"
    create_korean_voice(script)
```

### 6.2 실행 및 결과

```bash
uv run tts_client.py
```

잠시 후 `korean_voice.wav` 파일이 생성됩니다. 미디어 플레이어로 실행하여 자연스러운 한국어 발음을 확인해 보세요!

---

## 7. 트러블슈팅 (Troubleshooting)

### 증상 1: `RuntimeError: No CUDA GPUs are available`
*   **원인**: 파드 컨테이너 내부에서 GPU를 인식하지 못했습니다.
*   **해결**: 
    1.  Deployment XML에 `runtimeClassName: nvidia`가 있는지 확인하세요.
    2.  WSL2 환경이라면 `LD_LIBRARY_PATH` 환경변수가 올바르게 설정되었는지 확인하세요.

### 증상 2: 모델 다운로드 중 멈춤
*   **원인**: 1.7B 모델과 관련 파일들이 크기 때문에(몇 GB), 로컬 네트워크 속도에 따라 오래 걸릴 수 있습니다.
*   **해결**: `kubectl logs -f [POD_NAME] -n llm-serving` 명령어로 다운로드 진행률을 모니터링하세요.

### 증상 3: `onnxruntime` 설치 에러 (`hint: You're using CPython 3.10`)
*   **상황**: 분명히 Python 3.12 가상환경을 만들었는데, `uv add` 실행 시 `Removed virtual environment` 로그가 뜨며 Python 3.10으로 다시 설치되고 결국 에러가 납니다.
*   **원인**: 프로젝트 설정 파일(`.python-version`)이 3.10으로 고정(Pin)되어 있어서, `uv`가 명령어를 실행할 때마다 자동으로 버전을 3.10으로 되돌리기 때문입니다. (이전 단계에서 실수로 3.10으로 초기화했거나, 시스템 환경을 따라간 경우)
*   **해결**: CPython을 업그레이드하는 것이 아니라, `uv`에게 **"이 프로젝트는 Python 3.12를 써야 해"** 라고 알려주어 설정을 갱신해야 합니다.
    ```bash
    # 1. 프로젝트 파이썬 버전을 3.12로 고정 (가장 중요!)
    uv python pin 3.12
    # 출력 예시: Pinned to Python 3.12.x
    
    # 2. 가상환경 재생성
    uv venv
    source .venv/bin/activate
    
    # 3. 패키지 설치 재시도
    uv add qwen-tts torch soundfile transformers
    ```

---

## 8. 마치며 (Conclusion)

지금까지 **vLLM-omni**와 **Qwen3-TTS**를 활용하여 나만의 AI 성우를 만들어보았습니다.

*   **Qwen3-TTS**는 1.7 B라는 비교적 가벼운 사이즈로도 놀라운 다국어 성능과 감정 표현력을 보여줍니다.
*   **k3s** 위에 배포함으로써 언제 어디서나 호출 가능한 API 서버를 갖추게 되었습니다.

이제 이 기술을 응용하여 뉴스 요약 봇, 오디오북 생성기, 또는 AI 비서의 목소리 등 다양한 서비스로 확장해 보시기 바랍니다.

다음 시간에는 또 다른 흥미로운 AI 모델 서빙 방법으로 찾아오겠습니다. 감사합니다! 👋

---

### 검증 환경 (Verification Environment)
*   **OS**: Windows 11 (WSL2 Ubuntu 22.04)
*   **Kubernetes**: k3s v1.31.1+k3s1
*   **GPU**: NVIDIA GeForce RTX 4070 Ti (Driver 560.x)
*   **Model**: Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
*   **Tool**: uv 0.4.x, Docker 27.x

---
slug: k3s-ollama-serving
title: "[Infra] K3s에 Ollama로 LLM 서빙하기"
authors: [me]
tags: [k3s, ollama, qwen, llm, serving, gpu, nvidia]
---

지난 포스팅에서 **vLLM**을 활용해 고성능 LLM 추론 환경을 구축했습니다.
이제 시리즈의 마지막, **2탄**입니다! 이번에는 가볍고 간편한 **Ollama**를 사용하여 모델을 배포해보겠습니다.

1탄: 압도적인 성능과 확장성, vLLM 편
**2탄: 가볍고 간편한 로컬 실행, Ollama 편**

이번 글에서는 로컬 LLM 실행의 대명사 **Ollama**를 사용하여, 동일한 **Qwen3-4B** 모델을 K3s 위에서 서빙하고, **Modelfile**로 나만의 커스텀 모델까지 만들어봅니다.

<!--truncate-->

## 1. 왜 Ollama인가? (Why Ollama?)

지난 포스팅에서 vLLM의 강력함을 확인했지만, 솔직히 설정이 꽤 복잡했죠? `LD_LIBRARY_PATH`, `gpu-memory-utilization`, `max-model-len`... 옵션이 한가득이었습니다.

**Ollama**는 이런 복잡함을 모두 감추고, **"모델 실행은 원래 이렇게 쉬워야 한다"** 는 철학으로 만들어진 도구입니다.

### 1.1 원커맨드 실행 (One-Command Simplicity)

Ollama의 가장 큰 매력은 **한 줄이면 끝**이라는 것입니다.

```bash
# 이것만으로 모델 다운로드 + 서버 실행 + 대화 시작!
ollama run qwen3:4b
```

복잡한 설정 파일도, 토크나이저 초기화도, 메모리 계산도 필요 없습니다. Ollama가 알아서 해줍니다. 그 비밀은 Ollama의 내부 동작 방식에 있습니다.

<details>
<summary>🔽 <strong>(클릭) Ollama는 어떻게 이것을 자동화하나요?</strong></summary>

Ollama 내부에서는 다음과 같은 일이 자동으로 일어납니다:

**1. 모델 포맷 (GGUF)**
Ollama는 **llama.cpp** 라이브러리를 백엔드로 사용하며, 모든 모델을 **GGUF**(GPT-Generated Unified Format)라는 단일 파일 포맷으로 관리합니다.
GGUF 파일 하나에 **모델 가중치 + 토크나이저 + 메타데이터**가 모두 포함되어 있기 때문에, vLLM처럼 별도로 토크나이저를 초기화하거나 `config.json`을 파싱할 필요가 없습니다.

**2. 자동 메모리 관리**
모델을 로드하면, Ollama(llama.cpp)는 다음 순서로 메모리를 할당합니다:
1. 사용 가능한 **GPU VRAM** 용량을 자동으로 감지합니다.
2. 모델의 각 레이어를 VRAM에 올릴 수 있는 만큼 GPU에 적재합니다.
3. VRAM이 부족하면, 나머지 레이어를 **CPU RAM(시스템 메모리)** 에 자동으로 오프로딩합니다.
4. 사용하지 않는 모델은 `OLLAMA_KEEP_ALIVE` 시간(기본 5분) 이후 자동으로 VRAM에서 언로드합니다.

즉, vLLM에서 `--gpu-memory-utilization 0.85`나 `--max-model-len 8192` 같은 값을 수동으로 계산해서 넣어야 했던 것을, Ollama는 **하드웨어를 감지하고 알아서 최적의 설정을 결정**합니다.

**3. 자동 양자화**
Ollama 레지스트리의 모델들은 대부분 **Q4_K_M** 양자화가 기본 적용되어 있습니다. 이는 정확도와 모델 크기 사이의 밸런스가 좋은 4비트 양자화 방식으로, 원본(FP16/BF16) 대비 약 **1/4 크기**로 압축됩니다. 따라서 vLLM보다 훨씬 적은 VRAM으로도 동일한 모델을 실행할 수 있습니다.

> **예시**: Qwen3-4B 모델 기준
> - vLLM (FP16): ~8GB VRAM 필요
> - Ollama (Q4_K_M): ~2.5GB VRAM 필요

</details>

### 1.2 자체 모델 레지스트리

vLLM은 HuggingFace에서 모델을 다운로드하거나 로컬 경로를 직접 마운트해야 했습니다.
Ollama는 자체적으로 **모델 레지스트리** ([ollama.com/library](https://ollama.com/library))를 운영합니다. Docker Hub처럼 `pull`/`push` 명령어로 모델을 관리할 수 있습니다.

```bash
# 모델 다운로드 (Docker 이미지 pull과 동일한 UX)
ollama pull qwen3:4b

# 다운로드된 모델 목록 확인
ollama list
```

#### 💡 레지스트리에 없는 모델은 어떡하나요?

갓 출시된 모델이 아직 Ollama 레지스트리에 등록되지 않은 경우에도 사용할 수 있습니다! 두 가지 방법이 있습니다:

**방법 1: HuggingFace에서 GGUF 파일 직접 가져오기**

최근 대부분의 모델은 HuggingFace에 GGUF 포맷으로도 함께 업로드됩니다. (예: `모델명-GGUF` 레포지토리 검색)

```bash
# 1. HuggingFace에서 GGUF 파일 다운로드
wget https://huggingface.co/사용자/모델명-GGUF/resolve/main/model-Q4_K_M.gguf

# 2. Modelfile 작성 (FROM에 로컬 GGUF 파일 경로 지정)
cat > Modelfile << EOF
FROM ./model-Q4_K_M.gguf
EOF

# 3. Ollama에 모델 등록
ollama create my-model -f Modelfile
```

**방법 2: Safetensors → GGUF 변환**

GGUF 파일이 없는 경우, `llama.cpp`의 변환 도구를 사용할 수 있습니다.

```bash
# llama.cpp의 convert 스크립트로 변환
python3 llama.cpp/convert_hf_to_gguf.py ./model-directory --outtype q4_k_m
```

> **Ollama 레지스트리 검색**: [ollama.com/library](https://ollama.com/library)에서 모델명을 검색하세요. `qwen3`, `llama3`, `gemma3` 등 주요 오픈소스 모델은 대부분 등록되어 있습니다.

#### 🌐 오프라인 환경에서 Ollama 사용하기

인터넷이 없는 폐쇄망 서버에서도 Ollama를 활용할 수 있습니다:

1. **인터넷이 되는 PC**에서 모델을 미리 다운로드합니다.
   ```bash
   ollama pull qwen3:4b
   ```
2. Ollama 모델 디렉토리(`~/.ollama/models`)를 통째로 USB나 네트워크를 통해 오프라인 서버로 복사합니다.
3. 오프라인 서버에서 Ollama를 실행하면 **모델이 이미 있으므로 바로 사용 가능**합니다.

GGUF 파일을 직접 가져오는 방법도 동일합니다:
```bash
# 오프라인 서버에서 로컬 GGUF 파일로 모델 등록
ollama create my-model -f Modelfile  # FROM ./model.gguf
```

### 1.3 Modelfile: 나만의 모델 만들기

Ollama만의 킬러 피처입니다. **Dockerfile**처럼 텍스트 파일 하나로 모델의 시스템 프롬프트, 파라미터, 페르소나 등을 정의하여 **커스텀 모델**을 만들 수 있습니다.

```
FROM qwen3:4b
SYSTEM "당신은 한국어 전문 AI 비서입니다. 항상 존댓말을 사용합니다."
PARAMETER temperature 0.7
PARAMETER num_ctx 8192
```

이번 글의 보너스 섹션에서 직접 만들어볼 예정이니, 기대해 주세요!

### 1.4 vLLM vs Ollama: 언제 무엇을 쓸까?

| 비교 항목 | vLLM | Ollama |
| :--- | :--- | :--- |
| **주요 목적** | 프로덕션 서빙 | 로컬 개발/프로토타이핑 |
| **설정 난이도** | 높음 (옵션 다수) | 매우 낮음 (원커맨드) |
| **동시 처리 성능** | 매우 높음 (PagedAttention) | 보통 (순차 처리 기본) |
| **모델 포맷** | HuggingFace (Safetensors) | GGUF (양자화 특화) |
| **커스터마이징** | 코드 레벨 | Modelfile (선언적) |
| **OpenAI API 호환** | ✅ 완전 호환 | ✅ 호환 (실험적) |
| **적합한 환경** | 팀/서비스 운영 | 개인 개발/학습 |

#### 📌 실전 시나리오별 비교

단순 기능 비교만으로는 어떤 도구를 선택해야 할지 감이 잘 안 오죠? 실제 환경별로 어떤 도구가 유리한지 비교해 봅시다.

**시나리오 1: 개인 개발 환경**
> 단일 GPU, 소수(1~5명) 사용자, 모델 1~2개 사용, 최신 모델이 출시되면 자주 교체

| 기준 | vLLM | Ollama |
| :--- | :--- | :--- |
| **모델 교체 속도** | YAML 수정 → Pod 재시작 (수 분) | `ollama pull` → 즉시 사용 (수 초) |
| **VRAM 효율** | FP16 기본, 큰 VRAM 필요 | Q4_K_M 양자화, 적은 VRAM으로 구동 |
| **초기 설정** | 복잡 (LD_LIBRARY_PATH 등) | 간단 (서버만 띄우면 됨) |
| **모델 관리** | 파일 다운로드 + 경로 설정 | `pull`/`rm`으로 간편 관리 |
| **🏆 추천** | △ (오버스펙) | **✅ 강력 추천** |

**시나리오 2: 팀 단위 개발 환경**
> 멀티 GPU, 수십 명 사용자, 안정적인 모델 1~2개 상시 서빙 + 신규 모델 검증

| 기준 | vLLM | Ollama |
| :--- | :--- | :--- |
| **동시 접속 처리** | PagedAttention + Continuous Batching | 순차 처리, 대기열 발생 가능 |
| **멀티 GPU 활용** | Tensor Parallelism (모델 분할 가속) | Pipeline 방식 (순차 레이어 전달) |
| **안정성** | Probe 기반 자동 복구, 프로덕션 검증 | 단순 서버, 기본적 안정성 |
| **신규 모델 검증** | YAML 수정 + 별도 Deployment 필요 | `pull` → 즉시 비교 테스트 가능 |
| **🏆 추천** | **✅ 상시 서빙용** | **✅ 신규 모델 검증용** |

> **결론**: 두 도구를 **같은 K3s 클러스터에 공존**시키는 것이 가장 이상적입니다.
> 안정적인 서비스는 vLLM으로, 새로운 모델 테스트나 프로토타이핑은 Ollama로 빠르게!

---

## 2. Ollama 주요 명령어 (Quick Reference)

Ollama는 CLI 기반으로 동작합니다. 실무에서 자주 사용하는 핵심 명령어를 정리합니다.

| 명령어 | 설명 | 예시 |
| :--- | :--- | :--- |
| `ollama pull` | 모델을 레지스트리에서 다운로드 | `ollama pull qwen3:4b` |
| `ollama run` | 모델 실행 (다운로드 + 대화) | `ollama run qwen3:4b` |
| `ollama list` | 다운로드된 모델 목록 확인 | `ollama list` |
| `ollama show` | 모델 상세 정보 확인 | `ollama show qwen3:4b` |
| `ollama rm` | 모델 삭제 | `ollama rm qwen3:4b` |
| `ollama create` | Modelfile로 커스텀 모델 생성 | `ollama create my-bot -f Modelfile` |
| `ollama ps` | 현재 로드된 모델 확인 | `ollama ps` |

<details>
<summary>🔽 <strong>(클릭) Ollama 주요 환경변수 정리</strong></summary>

Ollama는 환경변수를 통해 서버 동작을 제어합니다. K3s 배포 시 Pod의 `env`에 설정할 수 있습니다.

| 환경변수 | 기본값 | 설명 |
| :--- | :--- | :--- |
| `OLLAMA_HOST` | `127.0.0.1:11434` | Ollama 서버 바인딩 주소. 외부 접근 허용 시 `0.0.0.0:11434`로 설정 |
| `OLLAMA_MODELS` | `~/.ollama/models` | 모델 저장 디렉토리 경로 |
| `OLLAMA_KEEP_ALIVE` | `5m` | 모델을 메모리에 유지하는 시간. `0`이면 즉시 언로드 |
| `OLLAMA_NUM_PARALLEL` | `1` | 동시 처리 요청 수 |
| `OLLAMA_MAX_LOADED_MODELS` | `1` | 동시에 메모리에 로드할 모델 수 (아래 상세 설명 참고) |
| `OLLAMA_DEBUG` | `false` | 디버그 로깅 활성화 |
| `OLLAMA_FLASH_ATTENTION` | `true` | Flash Attention 사용 여부 (아래 상세 설명 참고) |

#### 💡 `OLLAMA_MAX_LOADED_MODELS`와 멀티 GPU VRAM 적재 방식

멀티 GPU 호스트(예: H200 8장)에서 여러 모델을 동시에 올리면 어떤 일이 일어나는지 알아봅시다.

Ollama의 멀티 GPU 동작 방식은 다음과 같습니다:

1. **단일 모델 로딩**: 모델이 하나의 GPU VRAM에 들어가면 해당 GPU에 전부 적재합니다. 만약 하나의 GPU에 들어가지 않으면, **여러 GPU에 레이어를 순차 분배**합니다. (Pipeline Parallelism)
2. **여러 모델 동시 로딩**: `OLLAMA_MAX_LOADED_MODELS=N`으로 설정하면 N개의 모델을 동시에 VRAM에 올릴 수 있습니다. 이 경우 각 모델은 **가능한 한 서로 다른 GPU에 분산 배치**됩니다.
3. **VRAM 부족 시**: 모델의 일부 레이어를 **CPU RAM으로 자동 오프로딩**합니다. (속도는 느려지지만 동작은 합니다)

```
# H200 8장 예시 - 3개 모델 동시 로딩
GPU 0: [모델 A 전체 레이어]
GPU 1: [모델 B 전체 레이어]
GPU 2-3: [모델 C 레이어 분산] ← 큰 모델은 여러 GPU에 걸쳐 분배
GPU 4-7: [유휴]
```

> ⚠️ **vLLM과의 차이**: vLLM은 **Tensor Parallelism**으로 하나의 모델을 여러 GPU에 분할하여 **추론 속도 자체를 가속**합니다. Ollama는 **Pipeline Parallelism**으로 레이어를 순차적으로 처리하므로, 단일 추론 속도 향상 효과는 제한적입니다.

#### 💡 `OLLAMA_FLASH_ATTENTION`이란?

**Flash Attention**은 LLM 추론의 핵심 연산인 Attention의 속도와 메모리 효율을 극적으로 개선하는 기술입니다.

일반적인 Attention 연산은 시퀀스 길이의 제곱(N²)에 비례하는 메모리를 사용합니다. 예를 들어, 입력이 1만 토큰이면 1억 개의 값을 저장해야 합니다. Flash Attention은 이 문제를 다음과 같이 해결합니다:

*   GPU의 **고속 SRAM(캐시 메모리)** 에서 Attention을 작은 블록 단위로 계산합니다.
*   전체 Attention 행렬을 한번에 만들지 않으므로, **메모리 사용량이 O(N²) → O(N)으로 감소**합니다.
*   결과적으로 **추론 속도 향상 + 더 긴 컨텍스트 처리**가 가능해집니다.

> 비유하자면, 1000페이지짜리 책의 목차를 만들 때 **전체 내용을 한번에 메모리에 올리는 것**(일반 Attention)과 **한 챕터씩 읽으면서 목차를 채워나가는 것**(Flash Attention)의 차이입니다.

Ollama는 기본적으로 Flash Attention을 활성화합니다. 특별한 이유가 없다면 꺼둘 필요가 없습니다.

> **참고**: 환경변수에 대한 자세한 내용은 [Ollama 공식 문서](https://ollama.com/docs)를 참고하세요.

</details>

---

## 3. 실습: Qwen3-4B 서빙하기

이제 K3s 클러스터에 Ollama를 배포해 봅시다.
vLLM 포스팅과 동일한 **Qwen3-4B** 모델을 사용하여, 두 도구의 차이를 직접 느껴보세요.

### 3.1 Deployment Manifest 작성

`ollama-qwen3.yaml` 파일을 작성합니다.
지난 시간에 만든 `llm-serving` 네임스페이스에 배포하겠습니다.

<details>
<summary>📄 <strong>(클릭) ollama-qwen3.yaml 파일 전체 내용 보기</strong></summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama-qwen3
  namespace: llm-serving
  labels:
    app: ollama-qwen3
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama-qwen3
  template:
    metadata:
      labels:
        app: ollama-qwen3
    spec:
      # [K3s 핵심] NVIDIA 컨테이너 런타임 사용 명시
      runtimeClassName: nvidia
      # 공유 메모리(SHM) 접근 허용 (GPU 간 통신 시 필요)
      hostIPC: true
      # [자동 모델 Pull] 서버가 뜨자마자 모델을 다운로드하는 Init Container
      initContainers:
        - name: model-puller
          image: ollama/ollama:latest
          command:
            - bash
            - -c
            - |
              # 1. 백그라운드에서 Ollama 서버 시작
              ollama serve &
              # 서버가 준비될 때까지 대기
              sleep 5
              # 2. 모델 Pull (이미 있으면 즉시 완료)
              ollama pull qwen3:4b
              # 3. 서버 종료
              kill %1
          env:
            - name: OLLAMA_HOST
              value: "0.0.0.0:11434"
            - name: OLLAMA_MODELS
              value: "/models/ollama/models"
            - name: LD_LIBRARY_PATH
              value: "/usr/lib/wsl/lib:/usr/lib/wsl/drivers/nvmdsi.inf_amd64_83eb34a6b09136c0:/usr/local/nvidia/lib64:/usr/local/cuda/lib64"
          securityContext:
            privileged: true
          resources:
            limits:
              nvidia.com/gpu: 1
            requests:
              nvidia.com/gpu: 1
          volumeMounts:
            - name: ollama-models
              mountPath: /models/ollama
      containers:
        - name: ollama
          # Ollama 공식 Docker 이미지 (최신 버전)
          image: ollama/ollama:latest
          securityContext:
            privileged: true
          resources:
            limits:
              # GPU 1개 할당
              nvidia.com/gpu: 1
              memory: "16Gi"
            requests:
              nvidia.com/gpu: 1
              memory: "8Gi"
          env:
            # Ollama가 모든 인터페이스에서 수신하도록 설정
            - name: OLLAMA_HOST
              value: "0.0.0.0:11434"
            # 모델 저장 경로 (볼륨 마운트 경로와 일치)
            - name: OLLAMA_MODELS
              value: "/models/ollama/models"
            # 로그 레벨 설정 (디버깅 시 "true"로 변경)
            - name: OLLAMA_DEBUG
              value: "false"
            # [WSL2 필수] 호스트 드라이버가 먼저 로딩되도록 경로 우선 배치
            # (아래 상세 설명 참고)
            - name: LD_LIBRARY_PATH
              value: "/usr/lib/wsl/lib:/usr/lib/wsl/drivers/nvmdsi.inf_amd64_83eb34a6b09136c0:/usr/local/nvidia/lib64:/usr/local/cuda/lib64"
            # NCCL 관련 설정 (WSL2 환경 호환성)
            - name: NCCL_P2P_DISABLE
              value: "1"
            - name: NCCL_CUMEM_HOST_ENABLE
              value: "0"
            - name: NCCL_NVLS_ENABLE
              value: "0"
          ports:
            - containerPort: 11434
              name: http
          # Ollama 서버 헬스체크 (루트 엔드포인트 사용)
          livenessProbe:
            httpGet:
              path: /
              port: 11434
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /
              port: 11434
            initialDelaySeconds: 15
            periodSeconds: 5
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /
              port: 11434
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
          volumeMounts:
            # Ollama 모델 저장소 (호스트와 공유하여 재다운로드 방지)
            - name: ollama-models
              mountPath: /models/ollama
      volumes:
        - name: ollama-models
          hostPath:
            # 호스트(WSL2)의 모델 디렉토리
            path: /mnt/c/Users/csj76/models/ollama
            type: DirectoryOrCreate
---
apiVersion: v1
kind: Service
metadata:
  name: ollama-qwen3-service
  namespace: llm-serving
spec:
  selector:
    app: ollama-qwen3
  ports:
    - protocol: TCP
      port: 80
      targetPort: 11434
  type: ClusterIP
```

</details>

#### 📄 YAML 파일 상세 설명 (초보자 필독!)

vLLM 배포와 비교하면서 핵심적인 차이점을 살펴봅시다.

*   `image: ollama/ollama:latest`: Ollama 공식 Docker 이미지입니다. vLLM은 `vllm/vllm-openai:v0.15.1`처럼 특정 버전을 지정했지만, Ollama는 `latest` 태그만으로도 자동으로 GPU를 감지합니다. 아래에서 자세히 설명합니다.
*   `containerPort: 11434`: Ollama의 기본 포트입니다. (vLLM은 8000번)
*   `OLLAMA_HOST: "0.0.0.0:11434"`: **중요!** 기본값이 `127.0.0.1`이라 Pod 외부에서 접근할 수 없습니다. 반드시 `0.0.0.0`으로 바꿔야 Service를 통해 접근할 수 있습니다.
*   `OLLAMA_MODELS`: 모델이 저장되는 경로입니다. `hostPath` 볼륨과 매칭하여 파드를 재시작해도 모델을 다시 다운로드하지 않습니다.
*   `initContainers`: **배포 시 자동으로 모델을 Pull** 하는 Init Container입니다. 아래에서 자세히 설명합니다.
*   `args`가 **없다**는 점에 주목하세요! vLLM과 달리 Ollama는 서버만 띄우면 됩니다.
*   `livenessProbe`의 `path: /`: Ollama는 루트 경로(`/`)에 접근하면 `"Ollama is running"` 메시지를 반환합니다. vLLM의 `/health`와 다릅니다.

#### 🤔 GPU 자동 감지는 어떻게 되나요? (`runtimeClassName`과 `LD_LIBRARY_PATH`)

vLLM 이미지(`vllm/vllm-openai`)와 Ollama 이미지(`ollama/ollama`) 모두 **`runtimeClassName: nvidia`가 필수**입니다. 이 설정이 K3s에게 "NVIDIA 컨테이너 런타임을 사용해서 GPU 디바이스를 파드에 주입해줘!"라고 알려주는 역할을 합니다. 이 설정이 없으면 어떤 이미지든 GPU를 인식하지 못합니다.

그렇다면 `LD_LIBRARY_PATH`와 `NCCL` 설정은 왜 필요할까요?

*   **`LD_LIBRARY_PATH`** : **(WSL2 환경 필수)** vLLM과 Ollama 이미지 모두 내부에 CUDA 관련 라이브러리(`libcuda.so`)가 포함되어 있습니다. 문제는 WSL2에서는 실제 GPU와 통신하는 드라이버가 **호스트(Windows)의 드라이버**(`/usr/lib/wsl/lib/libcuda.so`)인데, 컨테이너 내부의 드라이버가 먼저 로딩되면 충돌이 발생합니다.
    ```
    # LD_LIBRARY_PATH 검색 순서 (왼쪽이 우선)
    /usr/lib/wsl/lib          ← ① WSL2 호스트 드라이버 (진짜)
    /usr/local/nvidia/lib64   ← ② 컨테이너 내부 드라이버 (가짜!)
    /usr/local/cuda/lib64     ← ③ CUDA 라이브러리
    ```
    따라서 `LD_LIBRARY_PATH`의 **맨 앞에 WSL2 드라이버 경로를 배치**하여, 호스트의 진짜 드라이버가 먼저 로딩되도록 강제합니다. **네이티브 Linux나 Docker Desktop에서는 이 설정이 불필요**합니다.

*   **`NCCL_*` 설정**: NCCL(NVIDIA Collective Communications Library)은 멀티 GPU 통신에 사용되는 라이브러리입니다. WSL2에서는 P2P(Peer-to-Peer) 메모리 접근 등 일부 기능이 지원되지 않으므로, 해당 기능을 비활성화하여 호환성 문제를 방지합니다. 이 역시 **WSL2 환경에서만 필요한 설정**입니다.

#### 🔄 `initContainers`로 배포 시 자동 모델 Pull

vLLM은 `args`에 `--model` 옵션으로 모델을 지정하면 Deployment 시작 시 자동으로 모델을 로딩합니다. 하지만 Ollama는 서버만 먼저 뜨고, 모델은 별도로 `pull` 해야 하는 구조입니다.

매번 수동으로 `kubectl exec ... -- ollama pull`을 실행하면 번거롭겠죠? **Init Container**를 활용하면 배포 시 자동으로 모델을 다운로드할 수 있습니다.

```yaml
initContainers:
  - name: model-puller
    image: ollama/ollama:latest
    command:
      - bash
      - -c
      - |
        ollama serve &   # 백그라운드 서버 시작
        sleep 5           # 준비 대기
        ollama pull qwen3:4b  # 모델 Pull (이미 있으면 즉시 완료)
        kill %1           # 서버 종료
```

> **동작 원리**: Init Container가 먼저 실행되어 모델을 다운로드한 뒤 종료되고, 그 다음에 메인 Container가 시작됩니다. 볼륨을 공유하므로 Init Container에서 받은 모델을 메인 Container가 그대로 사용합니다.
> **이미 모델이 있다면?** `ollama pull`은 이미 다운로드된 모델은 `already exists` 처리하고 즉시 완료되므로, 재배포 시에도 불필요한 다운로드가 발생하지 않습니다.

### 3.2 배포 및 확인

작성한 YAML 파일을 K3s 클러스터에 적용합니다.

```bash
# 네임스페이스가 없다면 먼저 생성
kubectl create namespace llm-serving

# 배포 적용
kubectl apply -f ollama-qwen3.yaml
```

#### 🔍 진행 상황 모니터링

```bash
# 파드 상태를 실시간으로 확인
kubectl get pods -n llm-serving -w
```

Init Container가 모델 Pull을 완료한 후, 메인 Container가 `Running` 상태가 되면 준비 완료입니다.

```bash
# 모델이 정상 등록되었는지 확인
kubectl exec -n llm-serving deploy/ollama-qwen3 -- ollama list
```

```
NAME        ID              SIZE      MODIFIED
qwen3:4b    359d7dd4bcda    2.5 GB    21 seconds ago
```

> **💡 Tip**: `hostPath`로 호스트의 모델 디렉토리를 마운트했기 때문에, 파드를 삭제하고 다시 만들어도 모델이 유지됩니다. 다시 다운로드할 필요가 없습니다!

#### 🚧 트러블슈팅: GPU 관련 문제

vLLM 편과 동일하게, GPU 인식 실패 시 다음을 확인하세요:

> **증상: GPU를 인식하지 못하는 경우**
> 1. **CDI 스펙 미생성**: [K3s 설치 가이드](../2026-02-07-k3s-wsl-install/index.md)의 1단계에서 `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml` 명령을 실행했는지 확인하세요.
> 2. **CUDA compat 드라이버 충돌**: YAML의 `env`에 `LD_LIBRARY_PATH` 설정이 포함되어 있는지 확인하세요. (WSL2 환경 필수)

---

## 4. API 테스트: 네이티브 API & OpenAI 호환 API

Ollama는 **두 가지 API**를 제공합니다.
1. **네이티브 API** (`/api/chat`, `/api/generate`): Ollama 고유의 API
2. **OpenAI 호환 API** (`/v1/chat/completions`): 기존 OpenAI 클라이언트를 그대로 사용 가능

### 4.1 포트 포워딩 설정

```bash
# 로컬 포트 11434번을 서비스 포트 80번에 연결
kubectl port-forward svc/ollama-qwen3-service 11434:80 -n llm-serving
```

이제 터미널을 하나 더 열어서 테스트를 진행합니다.

### 4.2 네이티브 API 테스트

Ollama의 고유 API인 `/api/chat`을 사용해 봅니다.

```bash
# 모델 목록 확인
curl -s http://localhost:11434/api/tags | python3 -m json.tool
```

```json
{
    "models": [
        {
            "name": "qwen3:4b",
            "model": "qwen3:4b",
            "size": 2497293931,
            "details": {
                "format": "gguf",
                "family": "qwen3",
                "parameter_size": "4.0B",
                "quantization_level": "Q4_K_M"
            }
        }
    ]
}
```

채팅 API를 호출합니다. `stream: false`로 설정하면 응답을 한 번에 받을 수 있습니다.

```bash
curl -s http://localhost:11434/api/chat \
  -d '{
    "model": "qwen3:4b",
    "messages": [
      {"role": "user", "content": "3.11과 3.9 중 어느 숫자가 더 큰가요?"}
    ],
    "stream": false
  }' | python3 -m json.tool
```

**[실행 결과 예시]**

```json
{
    "model": "qwen3:4b",
    "message": {
        "role": "assistant",
        "content": "3.9가 더 큰 숫자입니다.\n(3.9는 3.90이므로, 3.11보다 0.79가 더 큽니다.)",
        "thinking": "Okay, so I need to figure out whether 3.11 or 3.9 is the larger number..."
    },
    "done": true,
    "total_duration": 49690154045,
    "eval_count": 356,
    "eval_duration": 3247069741
}
```

> **주목!** 응답에 `thinking` 필드가 별도로 분리되어 있습니다. vLLM에서는 `content` 안에 `<think>...</think>` 태그가 포함되어 있었지만, Ollama는 사고 과정을 별도 필드로 깔끔하게 분리해줍니다.

### 4.3 OpenAI 호환 API 테스트

기존 OpenAI 클라이언트와 호환되는 `/v1/chat/completions` 엔드포인트도 지원합니다.
vLLM 편의 테스트 코드와 거의 동일하게 사용할 수 있습니다!

```bash
python3 -c "import urllib.request, json; \
print(json.load(urllib.request.urlopen(urllib.request.Request( \
    'http://localhost:11434/v1/chat/completions', \
    data=json.dumps({ \
        'model': 'qwen3:4b', \
        'messages': [{'role': 'user', 'content': '3.11과 3.9 중 어느 숫자가 더 큰가요?'}], \
        'temperature': 0.7 \
    }).encode('utf-8'), \
    headers={'Content-Type': 'application/json'} \
)))['choices'][0]['message']['content'])"
```

vLLM과 동일한 OpenAI 포맷으로 응답이 옵니다!

#### 📊 Ollama 네이티브 API vs OpenAI 호환 API 비교

두 API의 차이를 표로 정리합니다. 어떤 API를 사용할지 선택할 때 참고하세요.

| 비교 항목 | Ollama 네이티브 API | OpenAI 호환 API |
| :--- | :--- | :--- |
| **엔드포인트** | `/api/chat`, `/api/generate` | `/v1/chat/completions` |
| **포트** | `11434` | `11434` (동일) |
| **요청 포맷** | `{"model", "messages", "stream"}` | `{"model", "messages", "temperature", ...}` |
| **응답 구조** | `message.content` + `message.thinking` (분리) | `choices[0].message.content` (통합) |
| **Thinking 처리** | `thinking` 필드로 별도 분리 | `content` 안에 포함 |
| **성능 지표** | `total_duration`, `eval_count`, `eval_duration` 제공 | 제공하지 않음 |
| **스트리밍** | `"stream": true/false` | `"stream": true/false` |
| **호환성** | Ollama 전용 | OpenAI SDK, LangChain 등 기존 도구와 호환 |
| **안정성** | 안정 (공식 API) | 실험적 (변경 가능성 있음) |
| **추천 용도** | Ollama 단독 사용 시 | 기존 코드 마이그레이션, 프레임워크 연동 시 |

> **💡 vLLM → Ollama 마이그레이션 팁**
> OpenAI 호환 API를 사용하면, 코드 변경 없이 `base_url`만 바꾸면 됩니다.
> - vLLM: `http://localhost:8000/v1/chat/completions`
> - Ollama: `http://localhost:11434/v1/chat/completions`

---

## 5. 보너스: Ingress로 포트포워딩 없이 접근하기

vLLM 편과 동일하게, **Ingress**를 설정하여 포트포워딩 없이 API에 접근할 수 있습니다.

### 5.1 Ingress Manifest 작성

`ollama-ingress.yaml` 파일을 작성합니다. Ollama는 네이티브 API(`/api`)와 OpenAI 호환 API(`/v1`) 두 가지 경로를 모두 라우팅해야 합니다.

```yaml
# Ollama Ingress 설정
# K3s 내장 Traefik Ingress Controller를 사용하여
# 포트 포워딩 없이 Ollama API에 접근할 수 있도록 구성합니다.
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ollama-ingress
  namespace: llm-serving
  annotations:
    # Traefik을 Ingress Controller로 사용
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  # K3s 내장 Traefik Ingress Class 지정
  ingressClassName: traefik
  rules:
    # DNS가 없으므로 localhost를 호스트로 사용
    - host: localhost
      http:
        paths:
          # Ollama 네이티브 API 경로 (/api/chat, /api/generate 등)
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: ollama-qwen3-service
                port:
                  number: 80
          # OpenAI 호환 API 경로 (/v1/chat/completions 등)
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: ollama-qwen3-service
                port:
                  number: 80
```

#### 📄 YAML 파일 상세 설명

vLLM의 Ingress와 비교했을 때 핵심 차이점은 다음과 같습니다:

*   `path: /api`: Ollama 네이티브 API용 경로입니다. vLLM에는 없던 경로입니다.
*   `path: /v1`: OpenAI 호환 API 경로는 vLLM과 동일합니다.
*   `/health` 경로가 **없습니다**: Ollama는 루트 경로(`/`)로 헬스체크하므로, 별도의 `/health` 경로 라우팅이 필요 없습니다.

> ⚠️ **주의**: vLLM Ingress를 동시에 사용하고 있다면, `/v1` 경로가 충돌할 수 있습니다. 하나만 사용하거나, `host`를 다르게 설정하세요.

### 5.2 Ingress 배포 및 확인

```bash
# Ingress 배포
kubectl apply -f ollama-ingress.yaml

# 전체 리소스 확인
kubectl get all,ingress -n llm-serving
```

**[실행 결과 예시]**

```
NAME                                READY   STATUS    RESTARTS   AGE
pod/ollama-qwen3-85f9bf8c54-ldd47   1/1     Running   0          14m

NAME                           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/ollama-qwen3-service   ClusterIP   10.43.184.24   <none>        80/TCP    14m

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ollama-qwen3   1/1     1            1           14m

NAME                                       CLASS     HOSTS       ADDRESS         PORTS   AGE
ingress.networking.k8s.io/ollama-ingress   traefik   localhost   172.22.239.53   80      6s
```

### 5.3 Ingress를 통한 API 테스트

포트포워딩 없이 바로 API를 호출합니다!

```bash
# 모델 목록 확인 (Ingress 경유)
curl -s -H 'Host: localhost' http://localhost/api/tags | python3 -m json.tool

# OpenAI 호환 API 모델 목록 (Ingress 경유)
curl -s -H 'Host: localhost' http://localhost/v1/models | python3 -m json.tool
```

> **💡 포트포워딩 vs Ingress 비교**
>
> | 구분 | 포트포워딩 | Ingress |
> | :--- | :--- | :--- |
> | **URL** | `http://localhost:11434/api/...` | `http://localhost/api/...` |
> | **터미널 점유** | 별도 터미널 필요 | 불필요 |
> | **안정성** | 터미널 종료 시 끊김 | 항상 유지 |
> | **용도** | 개발/디버깅 | 개발~운영 전 단계 |

---

## 6. 보너스: Modelfile로 커스텀 모델 만들기

Ollama의 진정한 강점인 **Modelfile**을 활용해 나만의 커스텀 모델을 만들어 봅시다.

### 6.1 Modelfile이란?

Modelfile은 Docker의 Dockerfile과 비슷한 개념입니다. 텍스트 파일 하나로 모델의 행동을 정의합니다.

| 명령어 | 설명 | 필수 |
| :--- | :--- | :--- |
| `FROM` | 베이스 모델 지정 | ✅ |
| `SYSTEM` | 시스템 프롬프트 (모델의 역할/성격 설정) | |
| `PARAMETER` | 모델 파라미터 설정 (temperature 등) | |
| `TEMPLATE` | 프롬프트 템플릿 커스터마이징 | |
| `ADAPTER` | LoRA 어댑터 적용 | |
| `MESSAGE` | 대화 히스토리 사전 시딩 | |
| `LICENSE` | 라이선스 정보 | |

### 6.2 한국어 전문 비서 만들기

실제로 커스텀 모델을 만들어 봅시다. Pod 내부에서 직접 실행합니다.

```bash
# 1. Modelfile 작성 (Pod 내부에서 실행)
kubectl exec -n llm-serving deploy/ollama-qwen3 -- bash -c 'cat > /tmp/Modelfile << EOF
FROM qwen3:4b

# 시스템 프롬프트: 모델의 페르소나 정의
SYSTEM """당신은 "지니"라는 이름의 한국어 AI 비서입니다.
다음 규칙을 반드시 따릅니다:
1. 항상 존댓말(합쇼체)을 사용합니다.
2. 답변은 간결하고 명확하게 합니다.
3. 기술적 내용은 비유를 들어 쉽게 설명합니다.
4. Thinking 과정 없이 바로 답변합니다."""

# 파라미터 설정
PARAMETER temperature 0.7
PARAMETER num_ctx 8192
PARAMETER top_p 0.9

# Thinking 비활성화
PARAMETER /no_think true
EOF'

# 2. 커스텀 모델 생성
kubectl exec -n llm-serving deploy/ollama-qwen3 -- ollama create jini-bot -f /tmp/Modelfile
```

**[실행 결과 예시]**

```
gathering model components
using existing layer sha256:3e4cb1417446...
creating new layer sha256:a1b2c3d4e5f6...
writing manifest
success
```

### 6.3 커스텀 모델 테스트

만들어진 `jini-bot` 모델을 테스트해 봅시다.

```bash
# 모델 목록 확인 - jini-bot이 추가되었는지 확인
kubectl exec -n llm-serving deploy/ollama-qwen3 -- ollama list

# API 호출 테스트
curl -s http://localhost:11434/api/chat \
  -d '{
    "model": "jini-bot",
    "messages": [
      {"role": "user", "content": "쿠버네티스가 뭔지 쉽게 설명해줘"}
    ],
    "stream": false
  }' | python3 -m json.tool
```

커스텀 시스템 프롬프트가 적용되어, "지니" 페르소나로 존댓말을 사용하며 비유를 들어 설명하는 모습을 확인할 수 있습니다.

> **💡 활용 아이디어**
> *   고객 응대 봇: 회사의 FAQ를 시스템 프롬프트에 넣고 전용 봇 생성
> *   코드 리뷰어: 코딩 컨벤션을 정의하고 코드 리뷰 전문 모델 생성
> *   번역가: 특정 도메인 용어집을 시스템 프롬프트에 포함

---

## 7. 마치며: 시리즈 총정리

2회에 걸쳐 K3s 위에서 LLM을 서빙하는 두 가지 방법을 다뤘습니다.

| 구분 | 1탄: vLLM | 2탄: Ollama |
| :--- | :--- | :--- |
| **설정 파일** | YAML 내 `args`로 모델+옵션 지정 | YAML은 서버만, 모델은 `pull`로 별도 관리 |
| **모델 포맷** | HuggingFace (Safetensors) | GGUF (양자화 특화) |
| **API** | OpenAI 호환 (`/v1/...`) | 네이티브 (`/api/...`) + OpenAI 호환 |
| **커스터마이징** | 코드 수준 설정 | Modelfile (선언적) |
| **강점** | 동시 처리, 고성능 | 간편함, 빠른 프로토타이핑 |

두 도구 모두 **같은 K3s 인프라** 위에서 동작하며, 목적에 따라 선택하면 됩니다.
이 시리즈를 통해 여러분의 로컬 환경이 **나만의 AI 서버**로 거듭나길 바랍니다! 🚀

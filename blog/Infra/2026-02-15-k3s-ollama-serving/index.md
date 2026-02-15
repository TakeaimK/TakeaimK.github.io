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

**Ollama**는 이런 복잡함을 모두 감추고, **"모델 실행은 원래 이렇게 쉬워야 한다"**는 철학으로 만들어진 도구입니다.

### 1.1 원커맨드 실행 (One-Command Simplicity)

Ollama의 가장 큰 매력은 **한 줄이면 끝**이라는 것입니다.

```bash
# 이것만으로 모델 다운로드 + 서버 실행 + 대화 시작!
ollama run qwen3:4b
```

복잡한 설정 파일도, 토크나이저 초기화도, 메모리 계산도 필요 없습니다. Ollama가 알아서 해줍니다.

### 1.2 자체 모델 레지스트리

vLLM은 HuggingFace에서 모델을 다운로드하거나 로컬 경로를 직접 마운트해야 했습니다.
Ollama는 자체적으로 **모델 레지스트리**를 운영합니다. Docker Hub처럼 `pull`/`push` 명령어로 모델을 관리할 수 있습니다.

```bash
# 모델 다운로드 (Docker 이미지 pull과 동일한 UX)
ollama pull qwen3:4b

# 다운로드된 모델 목록 확인
ollama list
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
| **동시 처리 성능** | 매우 높음 (PagedAttention) | 보통 |
| **모델 포맷** | HuggingFace (Safetensors) | GGUF (양자화 특화) |
| **커스터마이징** | 코드 레벨 | Modelfile (선언적) |
| **OpenAI API 호환** | ✅ 완전 호환 | ✅ 호환 (실험적) |
| **적합한 환경** | 팀/서비스 운영 | 개인 개발/학습 |

> **한 줄 요약**: 동시 접속자가 많은 **프로덕션 서비스**라면 vLLM, **빠르게 모델을 테스트**하고 프로토타이핑하고 싶다면 Ollama!

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
| `OLLAMA_MAX_LOADED_MODELS` | `1` | 동시에 메모리에 로드할 모델 수 |
| `OLLAMA_DEBUG` | `false` | 디버그 로깅 활성화 |
| `OLLAMA_FLASH_ATTENTION` | `true` | Flash Attention 사용 여부 |

> **참고**: 환경변수 목록은 [공식 FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.md)를 참고하세요.

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
              value: "/root/.ollama/models"
            # 로그 레벨 설정 (디버깅 시 DEBUG로 변경)
            - name: OLLAMA_DEBUG
              value: "false"
            # [WSL2 필수] 호스트 드라이버가 먼저 로딩되도록 경로 우선 배치
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
            - name: ollama-data
              mountPath: /root/.ollama
      volumes:
        - name: ollama-data
          hostPath:
            # 호스트(WSL2)의 Ollama 데이터 디렉토리
            path: /root/.ollama
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

*   `image: ollama/ollama:latest`: Ollama 공식 Docker 이미지입니다. vLLM과 달리 별도의 태그(버전) 지정 없이도 GPU를 자동으로 감지합니다.
*   `containerPort: 11434`: Ollama의 기본 포트입니다. (vLLM은 8000번)
*   `OLLAMA_HOST: "0.0.0.0:11434"`: **중요!** 기본값이 `127.0.0.1`이라 Pod 외부에서 접근할 수 없습니다. 반드시 `0.0.0.0`으로 바꿔야 Service를 통해 접근할 수 있습니다.
*   `OLLAMA_MODELS`: 모델이 저장되는 경로입니다. `hostPath` 볼륨과 매칭하여 파드를 재시작해도 모델을 다시 다운로드하지 않습니다.
*   `args`가 **없다**는 점에 주목하세요! vLLM과 달리 Ollama는 서버만 띄우면 됩니다. 모델은 나중에 `pull` 명령으로 다운로드합니다.
*   `LD_LIBRARY_PATH`: **(WSL2 필수)** vLLM과 동일하게 WSL2 호스트 드라이버가 먼저 로딩되도록 경로를 설정합니다.
*   `livenessProbe`의 `path: /`: Ollama는 루트 경로(`/`)에 접근하면 `"Ollama is running"` 메시지를 반환합니다. vLLM의 `/health`와 다릅니다.

> **vLLM과의 핵심 차이**: vLLM은 Deployment 시점에 `--model` 옵션으로 모델까지 지정하고 한번에 로딩합니다.
> Ollama는 서버만 먼저 띄우고, 모델은 이후에 `ollama pull`로 다운로드합니다. 마치 Docker 데몬을 먼저 띄우고, 이미지를 나중에 pull 하는 것과 같은 개념입니다.

### 3.2 배포 및 모델 다운로드

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

파드가 `Running` 상태가 되면, Ollama 서버가 준비된 것입니다.
이제 모델을 다운로드합니다.

```bash
# Pod 내부에서 모델 다운로드 실행
kubectl exec -n llm-serving deploy/ollama-qwen3 -- ollama pull qwen3:4b
```

**[실행 결과 예시]**

```
pulling manifest
pulling 3e4cb1417446: 100% ▕██████████████████▏ 2.5 GB
pulling 2d54db2b9bb2: 100% ▕██████████████████▏ 1.5 KB
pulling d18a5cc71b84: 100% ▕██████████████████▏  11 KB
pulling cff3f395ef37: 100% ▕██████████████████▏  120 B
pulling e18a783aae55: 100% ▕██████████████████▏  487 B
verifying sha256 digest
writing manifest
success
```

다운로드가 완료되면, 모델이 정상적으로 등록되었는지 확인합니다.

```bash
kubectl exec -n llm-serving deploy/ollama-qwen3 -- ollama list
```

```
NAME        ID              SIZE      MODIFIED
qwen3:4b    359d7dd4bcda    2.5 GB    21 seconds ago
```

> **💡 Tip**: `hostPath`로 `/root/.ollama`를 마운트했기 때문에, 파드를 삭제하고 다시 만들어도 모델이 유지됩니다. 다시 다운로드할 필요가 없습니다!

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

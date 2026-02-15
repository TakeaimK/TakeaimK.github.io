---
slug: k3s-vllm-serving
title: "[Infra] K3s에 vLLM으로 LLM 서빙하기"
authors: [me]
tags: [k3s, vllm, qwen, llm, serving, gpu, nvidia]
---

지난 포스팅에서 **K3s + NVIDIA GPU** 환경을 구축하고, 필수 명령어(`kubectl`)까지 마스터했습니다.
이제 드디어 **실전**입니다! 이번 포스팅부터 2회에 걸쳐, 대표적인 LLM 서빙 도구인 **vLLM**과 **Ollama**를 사용하여 최신 모델을 배포해보겠습니다.

**1탄: 압도적인 성능과 확장성, vLLM 편**
2탄: 가볍고 간편한 로컬 실행, Ollama 편

이번 글에서는 엔터프라이즈 환경에서 표준처럼 자리 잡은 고성능 추론 엔진 **vLLM**을 사용하여, 가볍고 강력한 **Qwen3-4B-Thinking** 모델을 서빙하는 방법을 다릅니다.

<!--truncate-->

## 1. 왜 vLLM인가? (Why vLLM?)

LLM을 서빙할 때 단순히 `transformers` 라이브러리로 모델을 로드해서 추론하면 속도가 매우 느리고, 동시 접속자가 늘어날 때 메모리 부족(OOM) 현상이 빈번하게 발생합니다.

**vLLM**은 이러한 문제를 해결하기 위해 등장한 초고속 LLM 추론 엔진입니다.

### 1.1 압도적인 처리량 (Throughput)
vLLM의 핵심 기술인 **PagedAttention** 알고리즘은 운영체제의 가상 메모리 관리 기법에서 영감을 받았습니다.
이를 통해 KV Cache(Key-Value 캐시) 메모리 낭비를 줄여, 같은 GPU에서도 **최대 24배 더 많은 요청**을 동시에 처리할 수 있습니다.

### 1.2 최신 모델의 발 빠른 지원
새로운 모델 아키텍처(Llama 3, Qwen 2.5/3, Mistral 등)가 출시되면, vLLM 커뮤니티는 거의 실시간으로 이를 지원합니다.
따라서 최신 SOTA(State-of-the-Art) 모델을 가장 먼저, 가장 빠르게 서비스에 적용하고 싶다면 vLLM 사용법을 익히는 것이 필수입니다.

### 1.3 다양한 데이터 타입과 양자화 지원
vLLM은 다양한 정밀도(Precision)와 압축 기술을 지원하여, 리소스 상황에 맞게 최적화할 수 있습니다.

*   **FP16 / BF16**: 기본 반정밀도. BF16은 A100/H100 등 Ampere 이상 아키텍처에서 더 넓은 표현 범위로 안정적인 학습/추론이 가능합니다.
*   **FP8**: 최신 Hopper 아키텍처(H100) 등에서 지원하며, 성능 저하 없이 모델 크기를 절반으로 줄이고 속도를 높입니다. [^1]
*   **GPTQ / AWQ / INT4**: 가중치(Weight)를 4비트 정수로 양자화하거나, 활성화(Activation)까지 고려하여 압축하는 기술입니다. VRAM 용량이 적은 소비자용 GPU(RTX 30/40 시리즈)에서도 거대 모델을 돌릴 수 있게 해줍니다. [^2][^3]
*   **MXFP4**: 최신 Blackwell 아키텍처를 위한 4비트 부동소수점 포맷으로, 극도로 효율적인 대역폭 활용을 가능하게 합니다.
*   **Multi-LoRA**: 하나의 베이스 모델에 여러 개의 LoRA 어댑터를 동적으로 로드하여, 요청마다 다른 페르소나의 봇을 서빙할 수 있습니다.

[^1]: [FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433)
[^2]: [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323)
[^3]: [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://arxiv.org/abs/2306.00978)

---

## 2. vLLM 주요 옵션 (Quick Reference)

vLLM은 매우 많은 실행 옵션을 제공합니다. 실무에서 가장 자주 마주치게 될 핵심 옵션 3가지는 다음과 같습니다.

| 옵션 | 설명 | 권장 설정과 팁 |
| :--- | :--- | :--- |
| `--model` | HuggingFace 모델 ID 또는 로컬 경로 | 예: `Qwen/Qwen3-4B-Thinking` |
| `--gpu-memory-utilization` | GPU 메모리 중 KV Cache에 할당할 비율 | 기본값 `0.9`. OOM이 발생하면 `0.85`, `0.8` 등으로 조금씩 낮춰보세요. |
| `--max-model-len` | 최대 컨텍스트 길이 (토큰 수) | 모델의 스펙을 넘길 수 없습니다. GPU VRAM이 부족하면 이 값을 줄여서 OOM을 방지할 수 있습니다. (예: 4096, 8192) |

<details>
<summary>🔽 <strong>(클릭) vLLM v0.15.1 Stable 전체 옵션 정리</strong></summary>

이 섹션은 **vLLM v0.15.1 Stable** 버전을 기준으로 작성되었습니다. 상세한 내용은 별도 문서인 **[vLLM 옵션 완벽 정리](./vLLM_OPTIONS.md)** 를 참고하세요.

### 2.1 Model Arguments (모델 관련 설정)

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--model` | (필수) | 사용할 모델의 HuggingFace ID 또는 로컬 경로입니다. |
| `--tokenizer` | `None` | 모델과 다른 토크나이저를 사용할 경우 지정합니다. 미지정 시 `--model`과 동일하게 설정됩니다. |
| `--skip-tokenizer-init` | `False` | 토크나이저 초기화를 건너뛸지 여부입니다. 임베딩 모델 등 특수 목적 시 사용됩니다. |
| `--revision` | `None` | HuggingFace 모델의 특정 리비전(브랜치, 태그)을 고정하여 사용합니다. |
| `--trust-remote-code` | `False` | 원격 코드를 신뢰하고 실행할지 여부입니다. (새로운 아키텍처 모델 사용 시 필수) |
| `--dtype` | `auto` | 모델 가중치 및 연산 데이터 타입입니다. Ampere 이상 GPU는 `bfloat16`을 권장합니다. |
| `--max-model-len` | `None` | 모델의 최대 컨텍스트 길이를 제한하여 OOM을 방지합니다. |

### 2.2 Parallel Arguments (병렬 처리 설정)

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--tensor-parallel-size`, `-tp` | `1` | 텐서 병렬 처리(Tensor Parallelism)에 사용할 GPU 개수입니다. |
| `--pipeline-parallel-size`, `-pp` | `1` | 파이프라인 병렬 처리(Pipeline Parallelism)에 사용할 GPU 개수입니다. |
| `--gpu-memory-utilization` | `0.9` | vLLM 프로세스가 사용할 GPU 메모리 비율(0~1)입니다. OOM 발생 시 낮춰야 합니다. |

### 2.3 KV Cache Arguments (캐시 메모리 관리)

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--block-size` | `16` | PagedAttention 블록 크기입니다. |
| `--enable-prefix-caching` | `False` | 프롬프트 접두사(Prefix) 캐싱을 활성화하여 반복 요청 속도를 높입니다. |
| `--swap-space` | `4` | GPU 메모리 부족 시 KV 캐시를 오프로딩할 CPU 메모리 크기(GiB)입니다. |

### 2.4 Scheduler Arguments (스케줄러 설정)

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--max-num-batched-tokens` | `None` | 한 번의 반복 당 처리할 최대 토큰 수입니다. |
| `--max-num-seqs` | `256` | 한 번의 반복 당 처리할 최대 시퀀스(요청) 개수입니다. |
| `--chunked-prefill-enabled` | `False` | 긴 프롬프트를 청크로 나누어 처리하여 지연 시간을 줄입니다. |

### 2.5 LoRA & Quantization (기타 설정)

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--enable-lora` | `False` | LoRA 어댑터 사용을 활성화합니다. |
| `--max-loras` | `1` | 동시에 활성화할 수 있는 LoRA 어댑터의 최대 개수입니다. |
| `--quantization`, `-q` | `None` | 양자화 방식을 지정합니다. (`awq`, `gptq`, `fp8` 등) |
| `--kv-cache-dtype` | `auto` | KV 캐시 저장 데이터 타입입니다. `fp8` 사용 시 메모리를 절약할 수 있습니다. |

> **참고**: vLLM은 업데이트 속도가 매우 빠르므로, 최신 옵션은 [공식 문서](https://docs.vllm.ai/en/v0.15.1/models/engine_args.html)를 참고하세요.

</details>

---

## 3. 실습: Qwen3-4B-Thinking 서빙하기

이제 이론은 충분합니다. 실제로 K3s 클러스터에 배포해 봅시다.
이번에 사용할 모델은 `Qwen/Qwen3-4B-Thinking-2507` 입니다. (최근 유행하는 Thinking 프로세스가 내장된 4B 사이즈의 모델입니다.)

### 3.1 Deployment Manifest 작성

먼저 `vllm-qwen3.yaml` 파일을 작성합니다.
지난 시간에 만든 `llm-serving` 네임스페이스에 배포하겠습니다.

<details>
<summary>📄 <strong>(클릭) vllm-qwen3.yaml 파일 전체 내용 보기</strong></summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-qwen3            # 디플로이먼트 이름
  namespace: llm-serving      # 배포할 네임스페이스
  labels:
    app: vllm-qwen3           # 라벨 (서비스와 연결하기 위함)
spec:
  replicas: 1                 # 파드 복제본 개수 (GPU 1개당 1개가 적절)
  selector:
    matchLabels:
      app: vllm-qwen3         # 어떤 파드를 관리할지 선택하는 라벨
  template:
    metadata:
      labels:
        app: vllm-qwen3       # 생성될 파드의 라벨
    spec:
      runtimeClassName: nvidia  # [중요] NVIDIA GPU 사용을 위해 필수!
      hostIPC: true             # [권장] GPU 간 메모리 공유 및 성능 최적화
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest  # 사용할 vLLM 이미지
        imagePullPolicy: IfNotPresent   # 이미지가 로컬에 없으면 다운로드
        securityContext:
          privileged: true      # [참고] 일부 환경에서 GPU 접근을 위해 필요할 수 있음
        
        # [리소스 할당]
        resources:
          limits:
            nvidia.com/gpu: 1   # GPU 1개를 전용으로 할당 (필수)
            memory: "16Gi"      # 최대 메모리 제한
          requests:
            nvidia.com/gpu: 1   # GPU 1개 요청
            memory: "8Gi"       # 최소 메모리 보장
            
        # [환경 변수 설정]
        env:
          - name: HUGGING_FACE_HUB_TOKEN
            value: "hf_YOUR_TOKEN_HERE" # (Optional) Gated Model 사용 시 토큰 필요
          - name: VLLM_LOGGING_LEVEL
            value: "INFO"       # 로그 레벨 설정
          - name: VLLM_WORKER_MULTIPROC_METHOD # [중요] Worker 프로세스 시작 방식 (Python 3.12+ 필수)
            value: "spawn"
          - name: NCCL_P2P_DISABLE
            value: "1"          # 소비자용 GPU(RTX 시리즈)에서 P2P 이슈 방지
          - name: NCCL_CUMEM_HOST_ENABLE # WSL2/Docker 환경 호환성
            value: "0"
          - name: NCCL_NVLS_ENABLE    # WSL2/Docker 환경 호환성
            value: "0"
          # [핵심 - WSL2 필수] 이미지 내 compat 드라이버 대신 호스트 드라이버를 우선 로드
          - name: LD_LIBRARY_PATH
            value: "/usr/lib/wsl/lib:/usr/local/nvidia/lib64:/usr/local/cuda/lib64"
            
        # [실행 옵션: command 없이 args만 사용]
        args:
          # (1) 모델 설정
          # 로컬 모델 경로 사용 (볼륨 마운트 경로 기준)
          - --model=/models/Qwen/Qwen3-4B-Thinking-2507
          # HuggingFace에서 다운로드하려면: --model=Qwen/Qwen3-4B-Thinking-2507
          - --served-model-name=qwen3-4b  # API 호출 시 사용할 모델 이름 별칭
          
          # (2) GPU 및 메모리 설정
          - --gpu-memory-utilization=0.85  # VRAM의 85%를 KV 캐시로 사용
          - --max-model-len=8192          # 최대 컨텍스트 길이 제한 (OOM 방지)
          - --dtype=auto                  # 데이터 타입 자동 설정 (BF16 등)
          
          # (3) 기타 설정
          - --trust-remote-code           # 새로운 아키텍처 모델 사용 시 필요
          
        # [포트 설정]
        ports:
        - containerPort: 8000   # vLLM 기본 포트
          name: http
          
        # [상태 검사 (Health Check)]
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 120 # 모델 로딩 시간 동안 대기 (넉넉하게)
          periodSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 5
          failureThreshold: 3
        startupProbe:             # 초기 기동 시에만 체크 (성공할 때까지 liveness 실패 무시)
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 10
          failureThreshold: 30    # 10초*30회 = 최대 5분까지 대기
          
        # [볼륨 마운트]
        volumeMounts:
          - name: hf-cache
            mountPath: /root/.cache/huggingface # 컨테이너 내부 캐시 경로
          - name: models-volume
            mountPath: /models                  # 컨테이너 내부 로컬 모델 경로
            readOnly: true
            
      # [볼륨 정의]
      volumes:
      - name: hf-cache
        hostPath:
          path: /root/.cache/huggingface        # 호스트(WSL2)의 캐시 경로 공유
          type: DirectoryOrCreate
      - name: models-volume
        hostPath:
          # [중요] 로컬 모델이 있는 실제 호스트 경로로 수정하세요!
          path: /mnt/c/Users/takeaim/models 
          type: DirectoryOrCreate
---
apiVersion: v1
kind: Service
metadata:
  name: vllm-qwen3-service    # 서비스 이름
  namespace: llm-serving
spec:
  selector:
    app: vllm-qwen3           # 연결할 파드 라벨
  ports:
    - protocol: TCP
      port: 80                # 외부에서 접속할 포트
      targetPort: 8000        # 내부 파드 포트 (vLLM)
  type: ClusterIP             # 클러스터 내부 IP 할당
```

</details>

#### 📄 YAML 파일 상세 설명 (초보자 필독!)

이전 포스팅에서 `Deployment`와 `Service`의 개념만 간단히 짚고 넘어갔는데, 위 설정 파일의 각 부분이 어떤 의미인지 상세히 알아봅시다.

*   `runtimeClassName: nvidia`: **가장 중요합니다!** K3s가 파드를 만들 때 NVIDIA 컨테이너 런타임을 사용하도록 강제합니다. 이게 없으면 GPU가 있어도 인식하지 못합니다.
*   `args`: vLLM 실행 옵션을 설정합니다. `--key=value` 형식을 사용하여 가독성을 높였습니다.
*   `--model`: 모델 경로를 지정합니다. **로컬 모델**을 사용하려면 볼륨 마운트 경로(예: `--model=/models/...`)로, **HuggingFace**에서 다운로드하려면 모델 ID(예: `--model=Qwen/Qwen3-4B-Thinking-2507`)로 지정합니다. 로컬 모델을 쓰면 다운로드 시간을 생략할 수 있습니다.
*   `LD_LIBRARY_PATH`: **(WSL2 필수)** vLLM 이미지 내의 compat 드라이버 대신 WSL2 호스트 드라이버가 먼저 로딩되도록 경로를 우선시합니다. 이 설정이 없으면 `No CUDA GPUs are available` 에러가 발생합니다.
*   `livenessProbe` / `readinessProbe` / `startupProbe`: 쿠버네티스가 파드의 상태를 체크하는 기능입니다. `startupProbe`는 초기 기동 시에만 체크하며, 이 프로브가 성공할 때까지 `livenessProbe` 실패를 무시합니다.
*   `volumeMounts` & `volumes`:
    *   **hf-cache**: 호스트(`WSL2 Ubuntu`)의 캐시 폴더를 공유하여 모델 다운로드 시간을 단축합니다.
    *   **models-volume**: 로컬에 이미 다운로드된 모델이 있다면, 해당 경로를 마운트하여 인터넷 다운로드 없이 즉시 로딩할 수 있습니다. (`--model=/models/...`로 경로 지정 필요)

### 3.2 배포 및 로그 확인

작성한 YAML 파일을 K3s 클러스터에 적용합니다.

```bash
# 네임스페이스가 없다면 먼저 생성
kubectl create namespace llm-serving

# 배포 적용
kubectl apply -f vllm-qwen3.yaml
```

#### 🚧 트러블슈팅: 파드가 뜨지 않나요?

GPU가 1개뿐인 환경에서는 자원 경합으로 인해 새 파드가 바로 실행되지 못할 수 있습니다.

> **증상 1: 자원 부족 (Pending)**
> 기존 파드가 완전히 종료되기 전까지 새 파드는 GPU를 할당받지 못해 `Pending` 상태로 대기합니다.

> **증상 2: GPU 인식 실패 (CrashLoopBackOff)**
> 로그에 `RuntimeError: No CUDA GPUs are available` 에러가 뜨는 경우입니다.
>
> 이 에러는 다음 두 가지 원인으로 발생합니다:
> 1. **CDI 스펙 미생성**: [K3s 설치 가이드](./2026-02-07-k3s-wsl-install/index.md)의 1단계에서 `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml` 명령을 실행했는지 확인하세요.
> 2. **CUDA compat 드라이버 충돌**: YAML의 `env`에 `LD_LIBRARY_PATH: "/usr/lib/wsl/lib:..."` 설정이 포함되어 있는지 확인하세요. (WSL2 환경 필수)

> **증상 3: 무한 재시작 (CrashLoopBackOff) - 기존 파드 충돌**
> 기존 파드가 에러로 인해 계속 재시작(`Running` -> `Error` -> `CrashLoopBackOff`)되는 경우에도 GPU를 점유하고 있어, 새 파드는 실행되지 못합니다.
> **해결 방법:** 문제가 있는 기존 파드를 **수동으로 삭제**하세요.


```bash
# 1. 파드 목록 확인
kubectl get pods -n llm-serving

# 2. 문제 있거나 종료되지 않은 기존 파드 삭제 (이름을 확인해서 넣으세요)
kubectl delete pod vllm-qwen3-xxxx... -n llm-serving
```

만약 상태가 너무 복잡해서 해결이 안 된다면, 아예 싹 지우고 다시 시작하는 것도 방법입니다.

```bash
# 생성했던 자원(Deployment, Service) 모두 삭제 (Reset)
kubectl delete -f vllm-qwen3.yaml

# (잠시 후 파드가 사라진 것을 확인하고) 다시 배포
kubectl apply -f vllm-qwen3.yaml
```

<details>
<summary>🔽 <strong>(클릭) 'kubectl apply'를 하면 내부에서 무슨 일이 일어나나요?</strong></summary>

이 과정을 이해하면 디버깅 실력이 쑥쑥 늡니다!

1.  **API 서버 요청**: `kubectl`이 YAML 내용을 K3s API 서버에 보냅니다 ("이대로 만들어줘!").
2.  **Deployment 생성**: Deployment 컨트롤러가 이를 접수하고, "파드 1개를 만들어야겠군" 하고 ReplicaSet을 만듭니다.
3.  **Scheduler 할당**: 스케줄러가 등장합니다. "GPU가 필요한 파드네? GPU가 있는 노드가 어디지?" 하고 적절한 노드에 파드를 배정합니다.
4.  **Kubelet 실행**: 해당 노드의 Kubelet이 지시를 받고, 컨테이너 런타임(containerd)에게 컨테이너 생성을 명령합니다.
5.  **이미지 풀(Pull)**: `vllm/vllm-openai:latest` 이미지가 없으면 다운로드 받습니다. (시간이 좀 걸림)
6.  **컨테이너 시작**: 이미지가 준비되면 컨테이너를 띄우고, 우리가 정의한 `args` 옵션으로 vLLM을 실행합니다.
7.  **vLLM 초기화**: vLLM 프로세스가 뜨면서 모델 가중치를 로드하고, GPU 메모리를 확보하고, 추론 준비를 마칩니다.
8.  **Ready 상태**: 모든 준비가 끝나면 파드 상태가 `Running`이 되고, `Ready` 조건이 만족됩니다.

</details>

#### 🔍 진행 상황 모니터링 (가장 중요!)

배포 직후에는 파드 상태가 `ContainerCreating` 일 것입니다. vLLM 이미지가 워낙 크기 때문에(몇 GB) 다운로드에 시간이 꽤 걸립니다.

```bash
# [-w] 옵션으로 상태 변화를 실시간으로 지켜봅니다.
kubectl get pods -n llm-serving -w
```

파드가 `Running` 상태가 되면, 실제로 모델이 로딩되고 있는지 로그를 확인해야 합니다.

```bash
# Pod 이름으로 로그 확인
kubectl logs -f vllm-qwen3-xxxx... -n llm-serving
# 라벨을 사용하여 로그 확인 (추천)
kubectl logs -f -l app=vllm-qwen3 -n llm-serving
```

**성공 로그 예시:**
로그 마지막에 다음과 같은 문구가 떠야 성공입니다.

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

만약 중간에 `OOM(Out Of Memory)` 에러가 뜨거나 프로세스가 죽는다면, `gpu-memory-utilization` 값을 조금 줄이거나 `max-model-len`을 줄여서 다시 `apply` 해보세요. ( Deployment는 내용이 바뀌면 알아서 파드를 재시작해줍니다! 👍 )

---

## 4. API 테스트: Thinking 프로세스 확인

vLLM은 OpenAI 호환 API를 제공하므로, 기존 OpenAI 클라이언트를 그대로 사용할 수 있습니다.
포트 포워딩을 통해 로컬에서 API를 호출해 보겠습니다.

### 4.1 포트 포워딩 설정

```bash
# 로컬 포트 8000번을 서비스 포트 80번에 연결
kubectl port-forward svc/vllm-qwen3-service 8000:80 -n llm-serving
```
이제 터미널을 하나 더 열어서 테스트를 진행합니다.

### 4.2 간단한 API 테스트 (Python One-liner)

파일을 따로 만들 필요 없이, 터미널에서 파이썬 표준 라이브러리(`urllib`)를 이용해 바로 결과를 확인해 보세요.
Thinking 모델의 특징인 사고 과정(`<think>...</think>`)이 출력되는지 확인할 수 있습니다.

```bash
# 아래 명령어를 터미널에 복사해서 붙여넣으세요.
python3 -c "import urllib.request, json; \
print(json.load(urllib.request.urlopen(urllib.request.Request( \
    'http://localhost:8000/v1/chat/completions', \
    data=json.dumps({ \
        'model': 'qwen3-4b', \
        'messages': [{'role': 'user', 'content': '3.11과 3.9 중 어느 숫자가 더 큰가요?'}], \
        'temperature': 0.7 \
    }).encode('utf-8'), \
    headers={'Content-Type': 'application/json'} \
)))['choices'][0]['message']['content'])"
```

**[실행 결과 예시]**

```
"
<think>
Okay, let me try to figure out which number is bigger between 3.11 and 3.9. Hmm, so both numbers start with 3, right? So the whole number part is the same for both. That means I need to look at the decimal parts to tell which one is larger.

Let me write them out: 3.11 and 3.9. Wait, 3.9 is the same as 3.90 if I add a zero at the end to make it two decimal places, right? So comparing 3.11 and 3.90.

In decimal numbers, the first digit after the decimal point is the tenths place. So for 3.11, the tenths digit is 1, and for 3.9, the tenths digit is 9. Since 9 is greater than 1, that would make 3.9 larger than 3.11.

Wait, but maybe I should check if there's a trick here. Sometimes people get confused with the number of decimal places. Let me think. For example, 3.11 is three and eleven hundredths, which is 3 + 11/100. And 3.9 is three and nine tenths, which is 3 + 9/10. Converting 9/10 to hundredths would be 90/100. So 90/100 is bigger than 11/100. Therefore, 3.9 is bigger than 3.11.

Another way to think about it: if I subtract them, 3.9 - 3.11 = 0.79, which is positive, so 3.9 is larger.

Wait, but maybe someone might think that because 3.11 has two decimal places and 3.9 has one, so 3.11 is more precise? But no, when comparing the numbers, the number of decimal places doesn't matter as much as the actual values. Even though 3.9 is written with one decimal, it's equivalent to 3.90, so it's 3.90 which is larger than 3.11.

Let me visualize them on a number line. Starting from 3, the next number is 3.1, then 3.2, up to 3.9. So 3.11 is just a bit past 3.1, whereas 3.9 is almost 4. So yeah, 3.9 is definitely bigger.

I think that's solid. So the answer should be 3.9 is larger than 3.11.
</think>

3.9은 3.11보다 더 크습니다.
**근거**:
- 두 수의 정수 부분(3)은 동일하므로, 소수 부분을 비교합니다.
- 3.9는 3.90과 동일하며, 소수 첫째 자리(9)가 3.11의 소수 첫째 자리(1)보다 크기 때문에 **3.9 > 3.11**입니다.

**정답**: 3.9가 더 큽니다.
...
```

모델이 답변을 내놓기 전에 `<think>` 태그 안에서 스스로 추론하는 과정을 볼 수 있습니다.

---

## 5. 마치며: 다음 예고

오늘은 **vLLM**을 활용해 고성능 추론 환경을 구축하고, 최신 Thinking 모델을 서빙하는 방법까지 알아봤습니다.
특히 `Deployment`와 `Service`를 사용하여 쿠버네티스 환경에서 안정적으로 운영할 수 있는 기반을 닦았습니다.

하지만, "나는 복잡한 설정 없이 그냥 로컬에서 간단하게 모델 한번 돌려보고 싶어!" 하는 분들도 계시겠죠?
그런 분들을 위해 **2탄**에서는 **Ollama**를 활용한 초간단 서빙 방법을 소개하겠습니다.

> **Next Post**: 🦙 **Ollama**로 로컬 LLM 정복하기 (feat. Modelfile 커스터마이징)

기대해 주세요! 🚀

---
slug: vllm-options-reference
title: "[Infra] vLLM 옵션 완벽 정리 (v0.15.1 Stable 기준)"
authors: [me]
tags: [vllm, options, infra, gpu, reference]
---

vLLM은 매우 다양한 실행 옵션을 제공하여, 사용자의 환경과 모델 특성에 맞춰 세밀하게 튜닝할 수 있습니다.
이 문서는 **vLLM v0.15.1 Stable (2026.02)** 버전을 기준으로, [공식 문서(Engine Args)](https://docs.vllm.ai/en/v0.15.1/models/engine_args.html)를 참고하여 정리했습니다.

<!--truncate-->

## 1. Model Arguments (모델 관련 설정)

모델 로딩 경로, 데이터 타입, 토크나이저 설정 등 가장 기본적인 옵션들입니다.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--model` | (필수) | 사용할 모델의 HuggingFace ID 또는 로컬 경로입니다. (예: `Qwen/Qwen3-4B-Thinking`) |
| `--tokenizer` | `None` | 모델과 다른 토크나이저를 사용할 경우 지정합니다. 미지정 시 `--model`과 동일하게 설정됩니다. |
| `--skip-tokenizer-init` | `False` | 토크나이저 초기화를 건너뛸지 여부입니다. 임베딩 모델 등 특수 목적 시 사용됩니다. |
| `--revision` | `None` | HuggingFace 모델의 특정 리비전(브랜치, 태그, 커밋 해시)을 고정하여 사용합니다. |
| `--code-revision` | `None` | 모델 코드(Python 파일)의 리비전을 별도로 지정할 때 사용합니다. |
| `--tokenizer-revision` | `None` | 토크나이저의 리비전을 별도로 지정할 때 사용합니다. |
| `--tokenizer-mode` | `auto` | 토크나이저 로딩 모드입니다. `auto`, `slow`, `mistral` 중 선택 가능합니다. |
| `--trust-remote-code` | `False` | `config.py` 등 모델 저장소에 포함된 원격 코드를 신뢰하고 실행할지 여부입니다. (새로운 아키텍처 모델 사용 시 필수) |
| `--download-dir` | `None` | 모델을 다운로드할 로컬 디렉토리 경로입니다. (기본: `~/.cache/huggingface`) |
| `--load-format` | `auto` | 모델 가중치 로딩 방식입니다. `auto`, `pt`, `safetensors`, `npcache`, `dummy` 등. `safetensors` 사용을 권장합니다. |
| `--dtype` | `auto` | 모델 가중치 및 연산의 데이터 타입입니다. `auto`, `half`, `float16`, `bfloat16`, `float`, `float32`. Ampere 이상 GPU는 `bfloat16`을 권장합니다. |
| `--kv-cache-dtype` | `auto` | KV 캐시 저장 데이터 타입입니다. `auto`, `fp8` 등을 지원하며, `fp8` 사용 시 메모리 사용량을 줄일 수 있습니다. |
| `--quantization-param-path` | `None` | 양자화 파라미터가 포함된 JSON 파일 경로입니다. |
| `--max-model-len` | `None` | 모델의 최대 컨텍스트 길이(토큰 수)를 제한합니다. OOM 방지 및 메모리 최적화를 위해 자주 사용됩니다. |
| `--guided-decoding-backend` | `outlines` | 가이드 디코딩(JSON Schema 강제 등)에 사용할 백엔드 엔진입니다. |

## 2. Parallel Arguments (병렬 처리 설정)

대규모 모델을 여러 GPU에 나누어 띄우기 위한 핵심 설정입니다.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--distributed-executor-backend` | `ray` | 분산 처리를 위한 백엔드입니다. `ray` 또는 `mp`(multiprocessing)를 선택할 수 있습니다. |
| `--worker-use-ray` | `False` | 워커 프로세스 관리에 Ray를 사용할지 여부입니다. 멀티 노드 환경에서는 필수입니다. |
| `--pipeline-parallel-size`, `-pp` | `1` | 파이프라인 병렬 처리(Pipeline Parallelism)에 사용할 GPU 개수입니다. 모델 레이어를 여러 GPU에 나누어 처리합니다. |
| `--tensor-parallel-size`, `-tp` | `1` | 텐서 병렬 처리(Tensor Parallelism)에 사용할 GPU 개수입니다. 단일 레이어의 연산을 여러 GPU가 나누어 처리합니다. |
| `--max-parallel-loading-workers` | `None` | 모델 가중치를 로드할 때 사용할 최대 병렬 워커 수입니다. |
| `--ray-workers-use-nsight` | `False` | Ray 워커에서 Nsight 프로파일링을 활성화할지 여부입니다. |

## 3. KV Cache Arguments (캐시 메모리 관리)

vLLM의 핵심인 PagedAttention 성능을 조절하는 옵션들입니다.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--block-size` | `16` | PagedAttention에서 사용할 토큰 블록 크기입니다. `16` 또는 `32`가 일반적입니다. |
| `--enable-prefix-caching` | `False` | 프롬프트의 공통 접두사(Prefix)를 캐싱하여, 동일한 문맥의 반복 요청 처리 속도를 획기적으로 높입니다. (RAG, 챗봇에 유용) |
| `--disable-sliding-window` | `False` | 슬라이딩 윈도우 어텐션 기능을 비활성화합니다. |
| `--gpu-memory-utilization` | `0.9` | vLLM 프로세스가 사용할 GPU 메모리 비율(0~1)입니다. 남은 메모리는 PyTorch 컨텍스트 등을 위해 예약됩니다. OOM 발생 시 이 값을 `0.85` 등으로 낮추세요. |
| `--swap-space` | `4` | GPU 메모리 부족 시 KV 캐시를 오프로딩할 CPU 메모리 크기(GiB)입니다. |
| `--cpu-offload-gb` | `0` | 모델 가중치를 CPU로 오프로드할 크기(GiB)입니다. VRAM이 부족한 경우 사용하지만 속도가 느려집니다. |

## 4. Scheduler Arguments (스케줄러 설정)

요청 처리량(Throughput)과 지연 시간(Latency)의 균형을 맞추는 옵션입니다.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--max-num-batched-tokens` | `None` | 한 번의 반복(Iteration) 당 처리할 최대 토큰 수입니다. |
| `--max-num-seqs` | `256` | 한 번의 반복 당 처리할 최대 시퀀스(요청) 개수입니다. |
| `--max-paddings` | `256` | 배치 내 최대 패딩 크기입니다. |
| `--disable-log-stats` | `False` | 주기적으로 출력되는 vLLM 통계 로그를 끕니다. |
| `--chunked-prefill-enabled` | `False` | 긴 프롬프트를 여러 배치로 나누어 처리(Chunked Prefill)하여, 전체적인 응답 지연 시간을 줄입니다. (v0.15.x에서는 기본값 False일 수 있음) |

## 5. LoRA Arguments (어댑터 설정)

LoRA(Low-Rank Adaptation)를 사용하는 경우 필요한 설정입니다.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--enable-lora` | `False` | LoRA 어댑터 사용을 활성화합니다. |
| `--max-loras` | `1` | 동시에 활성화할 수 있는 LoRA 어댑터의 최대 개수입니다. |
| `--max-lora-rank` | `16` | 지원할 최대 LoRA Rank입니다. 랭크가 높을수록 메모리 사용량이 늘어납니다. |
| `--lora-extra-vocab-size` | `256` | LoRA 어댑터에서 추가로 사용할 수 있는 어휘(Vocabulary) 크기입니다. |
| `--lora-dtype` | `auto` | LoRA 어댑터의 데이터 타입입니다. |

## 6. Quantization Arguments (양자화 설정)

모델의 메모리 사용량을 줄이고 속도를 높이는 양자화 관련 설정입니다.

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--quantization`, `-q` | `None` | 양자화 방식을 지정합니다. `awq`, `gptq`, `squeezellm`, `marlin`, `fp8`, `bitsandbytes` 등 다양한 방식을 지원합니다. |
| `--kv-cache-dtype` | `auto` | (중복 설명이지만 중요) KV 캐시를 `fp8` 등으로 양자화하여 저장합니다. |

---

> **주의**: vLLM은 업데이트 속도가 매우 빠릅니다. 옵션 이름이나 기본값이 변경될 수 있으므로, 실행 시 에러가 발생하면 반드시 `--help` 명령어로 확인하세요.

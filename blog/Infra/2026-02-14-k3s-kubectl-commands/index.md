---
slug: k3s-essential-commands
title: "[Infra] K3s/Kubernetes 필수 명령어 모음 (feat. LLM 서빙 준비)"
authors: [me]
tags: [k3s, kubernetes, kubectl, infra, llm]
---

지난 포스팅에서 **WSL2 + K3s + NVIDIA GPU** 환경을 성공적으로 구축했습니다.
이제 본격적으로 LLM(Large Language Model)을 서빙하기 위해, **K3s 환경에서 자주 사용하는 필수 명령어**를 정리해 보려 합니다.

특히 다음 포스팅에서 진행할 **vLLM과 Ollama를 활용한 Qwen 모델 서빙**을 염두에 두고, 실무에서 자주 쓰이는 명령어와 팁 위주로 구성했습니다.

<!--truncate-->

## 0. 들어가며: kubectl alias 설정 (필수!)

K3s를 설치하면 기본 명령어는 `k3s kubectl`입니다. 매번 입력하기 번거로우므로, 지난번에 설정한 **alias**가 잘 적용되어 있는지 확인합니다.

더 나아가, 실무에서는 **`k` 한 글자**로 줄여서 사용하는 것이 국룰입니다.

```bash
# ~/.bashrc 파일 마지막에 추가
alias kubectl="k3s kubectl"
alias k="kubectl"

# 설정 적용
source ~/.bashrc
```

이제부터는 `k get pods` 처럼 아주 간편하게 명령어를 입력할 수 있습니다!
> **참고**: 이 글의 모든 명령어는 `kubectl`을 기준으로 작성되었습니다. 편의상 `k`로 치셔도 무방합니다.

---

## 1. 네임스페이스 (Namespace) 이해하기

명령어를 배우기 전에, 가장 먼저 알아야 할 개념이 **네임스페이스**입니다. 리눅스의 폴더처럼, 쿠버네티스 자원들을 논리적으로 격리하는 공간입니다.

LLM 관련 자원들은 시스템 자원과 섞이지 않도록 **별도의 네임스페이스(`llm-serving`)** 를 만들어 관리하는 것을 강력 추천합니다.

```bash
# 네임스페이스 생성
kubectl create namespace llm-serving

# 해당 네임스페이스의 자원만 조회
kubectl get pods -n llm-serving
```

---

## 2. 클러스터 상태 확인 (Health Check)

LLM 배포 전, 노드와 GPU가 정상인지 확인하는 것이 가장 중요합니다.

### 2.1 노드 상태 조회
클러스터의 노드 목록과 상태(Ready 여부)를 확인합니다.

```bash
kubectl get nodes -o wide
```

### 2.2 GPU 인식 여부 확인 (핵심!)
K3s가 GPU를 제대로 인식하고 있는지 확인하려면 노드의 **상세 정보(Describe)**를 조회해야 합니다.

```bash
# 노드 상세 정보 전체 조회
kubectl describe node [노드이름]
```

정보가 너무 많아서 찾기 힘들다면, `grep`을 활용해 GPU 할당량 부분만 쏙 뽑아낼 수 있습니다.

```bash
# 할당 가능한 자원 조회 (Allocatable)
kubectl describe node [노드이름] | grep -A 10 Allocatable
```
**출력 예시:**
```yaml
Allocatable:
  cpu:                12
  ephemeral-storage:  244302636Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             16394468Ki
  nvidia.com/gpu:     1  <-- 이 부분이 보여야 GPU 사용 가능!
  pods:               110
  ...(이하 생략)
```

---

## 3. K3s 핵심 컴포넌트 살펴보기 (get pods -A)

K3s를 처음 설치하고 `kubectl get pods -A` 명령어를 치면 여러 시스템 파드들이 보입니다. 각각 어떤 역할을 하는지 알아봅시다.

```bash
kubectl get pods -A
```

**[실행 결과 예시]**

| NAMESPACE | NAME | READY | STATUS | RESTARTS | AGE |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **kube-system** | **coredns-7f496c8d7d-pfwmp** | 1/1 | Running | 3 | 6d13h |
| **kube-system** | **helm-install-traefik-crd...** | 0/1 | Completed | 0 | 6d13h |
| **kube-system** | **local-path-provisioner...** | 1/1 | Running | 3 | 6d13h |
| **kube-system** | **metrics-server...** | 1/1 | Running | 3 | 6d13h |
| **kube-system** | **nvidia-device-plugin...** | 1/1 | Running | 3 | 6d13h |
| **kube-system** | **traefik-6f5f87584-jtsz9** | 1/1 | Running | 3 | 6d13h |

### 주요 컴포넌트 설명
1. **coredns**: 클러스터 내부의 DNS 서버입니다. 파드끼리 도메인 이름으로 통신할 수 있게 해줍니다.
2. **traefik**: K3s에 기본 내장된 **인그레스 컨트롤러(Ingress Controller)**입니다. 외부 트래픽을 클러스터 내부 서비스로 연결해주는 관문 역할을 합니다.
3. **metrics-server**: 파드와 노드의 CPU/메모리 사용량을 수집합니다. (`kubectl top` 명령어 사용 시 필요)
4. **local-path-provisioner**: 로컬 스토리지를 동적으로 프로비저닝 해줍니다. PVC(PersistentVolumeClaim)를 만들 때 자동으로 호스트 경로를 연결해주는 고마운 녀석입니다.
5. **nvidia-device-plugin**: 우리가 지난 시간에 설치한 녀석입니다! GPU를 파드에 할당해주는 역할을 합니다.

> **💡 파드 이름 뒤의 난수(`-7f496c8d7d-pfwmp`)는 뭔가요?**
> - 이는 쿠버네티스가 파드를 고유하게 식별하기 위해 자동으로 붙이는 **해시(Hash)**값입니다.
> - `Deployment`나 `DaemonSet`으로 파드를 생성하면, 이름 충돌을 방지하기 위해 무작위 문자열이 자동으로 붙습니다.

---

## 4. 자원 생성 및 관리 (Create & Apply)

쿠버네티스(K3s 포함)에서는 다양한 워크로드를 관리합니다.

- **Pod**: 가장 기본적인 배포 단위 (1개 이상의 컨테이너)
- **Deployment**: 웹 서버(Nginx, vLLM) 처럼 계속 떠있어야 하는 애플리케이션을 관리 (가장 많이 씀)
- **DaemonSet**: 모든 노드(또는 특정 노드)에 **하나씩 반드시 실행**되어야 하는 파드.
    - *예시: 이전 포스팅에서 설치한 `nvidia-device-plugin`이 바로 DaemonSet입니다. 모든 GPU 노드에 설치되어야 하니까요!*
- **Job/CronJob**: 한 번 실행되고 종료되는 배치 작업(데이터 전처리, 모델 튜닝 등)을 관리
- **Service**: 파드에 네트워크 접근을 가능하게 해주는 로드밸런서

### 4.1 YAML 파일로 자원 생성
```bash
# 단일 파일 적용
kubectl apply -f my-pod.yaml

# 폴더 내 모든 파일 적용
kubectl apply -f ./manifests/
```
> **Tip**: 쿠버네티스 설정 파일(`yaml`)들은 보통 프로젝트 내 `manifests` 또는 `k8s`라는 이름의 폴더에 모아서 관리하는 것이 관례입니다.

### 4.2 현재 실행 중인 자원 조회
```bash
# 파드 조회
kubectl get pods

# 서비스 및 디플로이먼트 조회 (동시에 여러 종류 조회 가능!)
kubectl get svc,deploy

# 실시간 감시 (Watch) - 배포 진행 상황 볼 때 유용
kubectl get pods -w
```

---

## 5. 디버깅 및 로그 확인 (Troubleshooting)

LLM 모델이 로딩되지 않거나 에러가 발생할 때 사용하는 3대장 명령어입니다.

### 5.1 로그 확인 (logs)
파드의 표준 출력(stdout)을 실시간으로 확인합니다. 가장 많이 씁니다.

```bash
kubectl logs -f [파드이름]
```

> **🔥 꿀팁: 파드 이름 쉽게 입력하기**
> 1. `kubectl get pods`로 이름을 복사해서 붙여넣기 (가장 기본)
> 2. **라벨(Label) 사용하기**: 파드 이름이 매번 바뀌므로, 라벨로 선택하는 것이 훨씬 편합니다.
>    ```bash
>    # app=vllm 라벨을 가진 파드의 로그 보기
>    kubectl logs -f -l app=vllm
>    ```

### 5.2 파드 상세 상태 조회 (describe)
파드가 시작조차 안 될 때(Pending), 그 **이유(Events)** 를 확인할 때 씁니다.

```bash
kubectl describe pod [파드이름]
```
맨 아래 **Enable** 섹션을 보면 "이미지를 못 찾음", "GPU 부족함" 등의 원인이 나옵니다.

### 5.3 파드 내부 접속 (exec)
컨테이너 안으로 직접 들어가서 파일을 확인하거나 명령어를 실행해 봅니다.

```bash
kubectl exec -it [파드이름] -- /bin/bash
```

**접속 종료 방법:**
작업을 마치고 나오려면 `exit` 명령어를 입력하거나 `Ctrl + D` 단축키를 누르면 됩니다.
> **주의**: 파드 내부에서 `rm -rf /` 같은 위험한 명령어나, 시스템 설정 파일을 건드리는 작업은 신중해야 합니다. 파드가 재시작되면 데이터가 날아갈 수 있습니다 (일회성).

---

## 6. YAML 파일 생성 및 추출 꿀팁

처음부터 YAML 파일을 작성하는 건 어렵습니다. 다음 두 가지 방법을 활용하세요.

### 6.1 실행 전 미리보기 (Dry Run)
명령어로 YAML 뼈대를 생성합니다. 실제로 리소스를 만들지는 않습니다.

```bash
# "이런 파드를 만들고 싶은데, YAML 파일 좀 만들어줘"
kubectl run my-ai-app --image=vllm/vllm-openai --restart=Never --dry-run=client -o yaml > my-pod.yaml
```

### 6.2 실행 중인 리소스 추출 (Export)
이미 잘 돌아가고 있는 파드의 설정을 YAML 파일로 뽑아내서 재사용합니다. 백업할 때도 유용합니다.

```bash
# "지금 돌고 있는 저 파드, 설정 파일로 저장해줘"
kubectl get pod [실행중인_파드이름] -o yaml > backup.yaml
```
> **주의**: 이렇게 추출한 파일에는 상태 정보(`status`)나 불필요한 메타데이터가 포함되므로, 사용하기 전에 `dop`로 정리해주는 것이 좋습니다.

---

## 7. 자원 삭제 (Cleanup)

```bash
# YAML 파일로 삭제 (가장 권장)
kubectl delete -f my-pod.yaml

# 이름으로 삭제
kubectl delete pod gpu-test
```

---

## 마무리

이제 K3s를 다루기 위한 기본기는 모두 갖췄습니다!
다음 시간에는 이 명령어들을 실제로 사용해서, **Qwen 모델을 vLLM 위에 띄우고 API를 호출**하는 실습을 진행하겠습니다.

준비되셨나요? 다음 포스팅에서 만나요! 🚀

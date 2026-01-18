---
slug: aks-finetuning-pipeline-part1
title: "[MLOps] 밑바닥부터 시작하는 AKS 기반 파인튜닝 파이프라인 구축기 (1/2)"
authors: [me]
tags: [cloud, aks, mlops, docker]
date: 2026-01-18
---

> **들어가며:**
> 클라우드 네이티브 환경(K8s)이 처음인 엔지니어가 Azure Kubernetes Service(AKS) 위에 Prefect와 MLflow를 구축하고, 파이썬 기반의 파인튜닝 파이프라인을 돌리는 PoC(개념 증명) 과정을 기록합니다. 
> 1편에서는 **로컬 개발 환경 세팅부터 인프라 생성(AKS, ACR), 그리고 도커 이미지 빌드까지**의 과정을 다룹니다.

<!-- truncate -->

---

## 0. 사전 준비 (Prerequisites)

항해를 시작하기 전, 내 컴퓨터(Local)를 클라우드 조종석으로 만들기 위해 필수 도구들을 설치합니다.

* **OS 환경:** Mac / Windows (WSL2 또는 PowerShell)
* **필수 도구:**
    * `Azure CLI`: Azure 리소스 관리
    * `Kubectl`: Kubernetes 클러스터 제어
    * `Helm`: K8s 패키지 매니저
    * `Docker Desktop`: 컨테이너 빌드 및 실행

**설치 확인:**
```bash
az version       # Azure CLI 버전 확인
kubectl version --client # Kubectl 클라이언트 버전 확인
helm version     # Helm 버전 확인
docker --version # Docker 버전 확인
```

---

## 1. 클라우드 인프라 구축 (Infrastructure)

복잡한 Azure Portal GUI 대신, 재현 가능하고 명확한 **Azure CLI** 명령어를 사용해 인프라를 생성합니다.

### 1-1. 전략: "ACR과 AKS는 한 몸처럼"

Kubernetes가 이미지를 가져오려면 이미지 저장소(ACR)에 대한 접근 권한이 필수입니다. 나중에 권한 설정을 따로 하려면 복잡하므로, **클러스터 생성 시점에 `attach-acr` 옵션으로 한 번에 연결**하는 것이 시니어의 꿀팁입니다.

### 1-2. 인프라 생성 명령어

```bash
# 1. 리소스 그룹 생성 (프로젝트의 폴더 역할)
az group create --name rg-mlops-dev --location koreacentral

# 2. Azure Container Registry (ACR) 생성
# 주의: ACR 이름은 전 세계에서 유일해야 합니다. (영문 소문자+숫자)
az acr create --resource-group rg-mlops-dev --name acrmlopsdev001 --sku Basic

# 3. AKS 클러스터 생성 (+ ACR 연동)
# PoC 단계이므로 비용 절감을 위해 노드 2개로 시작하며, GPU 노드는 추후 추가합니다.
az aks create \
  --resource-group rg-mlops-dev \
  --name aks-mlops-dev \
  --node-count 2 \
  --generate-ssh-keys \
  --attach-acr acrmlopsdev001
```

### 1-3. 내 컴퓨터와 연결 (Connection)

클러스터가 생성되었다면, 내 로컬의 `kubectl`이 AKS를 바라보도록 자격 증명을 가져옵니다.

```bash
az aks get-credentials --resource-group rg-mlops-dev --name aks-mlops-dev --overwrite-existing

# 연결 확인 (Ready 상태의 노드 2개가 보여야 성공)
kubectl get nodes
```

---

## 2. 애플리케이션 Dockerization

인프라가 준비되었으니, 파이썬 파인튜닝 코드를 K8s가 이해할 수 있는 **'컨테이너 이미지(도시락)'** 로 포장할 차례입니다.

### 2-1. 프로젝트 구조

```text
mlops-poc/
├── main.py           # 실제 학습 코드 (또는 테스트용 스크립트)
├── config.yaml       # 학습 파라미터 설정
├── requirements.txt  # 의존성 라이브러리 목록
├── Dockerfile        # 이미지 빌드 명세서
└── <기타 소스코드 등>
```

### 2-2. Dockerfile 작성 (Best Practice 적용)

빌드 속도를 최적화하기 위해 `COPY` 명령어를 분리하는 **레이어 캐싱(Layer Caching)** 기법을 적용했습니다. 소스 코드가 바뀌어도 라이브러리 설치 과정은 생략되므로 빌드가 매우 빨라집니다.

```dockerfile
# Base Image: 가볍고 안정적인 Python 3.9 Slim 버전
FROM python:3.12-slim

WORKDIR /app

# 1. 의존성 파일만 먼저 복사 -> 라이브러리 설치 (캐싱 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 나머지 소스 코드 복사
COPY . .

# 3. 실행 명령어 정의
CMD ["python", "main.py", "--config", "config.yaml"]
```

### 2-3. 빌드 및 ACR 업로드

로컬에서 만든 이미지를 클라우드 저장소(ACR)로 업로드(Push)합니다.

```bash
# 1. ACR 로그인
az acr login --name acrmlopsdev001

# 2. 이미지 빌드 (태그: v1)
# 주의: 마지막의 점(.)은 현재 디렉토리를 의미하므로 필수!
docker build -t acrmlopsdev001.azurecr.io/finetuning-job:v1 .

# 3. 이미지 푸시 (업로드)
docker push acrmlopsdev001.azurecr.io/finetuning-job:v1
```

**확인:** `az acr repository list` 명령어로 `finetuning-job`이 조회되면 성공입니다.

---

## 트러블슈팅 및 시니어의 조언 (Troubleshooting & Tips)

**Q1. `az aks get-credentials` 후에도 `kubectl` 연결이 안 돼요.**

> **A.** Azure 구독(Subscription)이 여러 개인 경우 발생할 수 있습니다. `az account list`로 구독 목록을 확인하고, `az account set --subscription "구독ID"`로 올바른 구독을 활성화한 후 다시 시도해 보세요.

**Q2. 왜 처음부터 GPU 노드를 안 만드나요?**

> **A.** **비용 효율화(Cost Optimization)** 때문입니다. MLflow나 Prefect 같은 관리형 도구를 세팅하는 동안에는 비싼 GPU가 필요 없습니다. 시스템 구축이 끝나고 실제 학습을 돌리기 직전에 노드 풀(Node Pool)을 추가하는 것이 정석입니다.

**Q3. `docker push` 시 `unauthorized` 에러가 납니다.**

> **A.** `az acr login` 명령어를 실행하지 않았거나, 세션이 만료된 경우입니다. 로그인을 다시 수행해 주세요.

---

**다음 편 예고:**
이제 재료 준비는 끝났습니다. 2편에서는 **Helm** 을 사용하여 AKS 위에 **Prefect와 MLflow** 를 원터치배포하고, 실제 파이썬 파이프라인을 돌려 학습 로그가 모니터링되는 전체 워크플로우를 완성해 보겠습니다.

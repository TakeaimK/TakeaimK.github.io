---
slug: k3s-wsl-install-guide
title: "[Infra] WSL2 + K3s + NVIDIA GPU 완전 정복 가이드"
authors: [me]
tags: [k3s, wsl, gpu, nvidia, infra]
---

이 문서는 **Windows 11 (WSL2 Ubuntu)** 환경에서 **K3s**를 설치하고, **NVIDIA GPU**를 파드에서 사용할 수 있도록 설정하는 최종 정리본입니다.

> ⚠️ **중요**: 이 가이드는 **K3s v1.34.x** 버전 기준으로 작성되었습니다. 버전에 따라 containerd 설정 형식이 다를 수 있습니다.

### ✅ 전제 조건

1. **Windows 호스트**에 최신 NVIDIA 드라이버가 설치되어 있어야 합니다.
2. **WSL2 터미널**에서 `nvidia-smi` 명령어가 정상적으로 실행되어야 합니다.
3. 일부 작업에 **sudo 권한**이 필요합니다. (일반 사용자로도 수행 가능)

---

## 0단계: kubectl alias 설정 (권장)

K3s 설치 시 `/usr/local/bin/kubectl` 심볼릭 링크가 생성됩니다. 만약 `kubectl` 명령어가 작동하지 않는다면 alias를 설정합니다.

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'alias kubectl="k3s kubectl"' >> ~/.bashrc
source ~/.bashrc
```

> **참고**: 아래 명령어들은 alias 설정이 되어있다는 가정 하에 `kubectl`로 표기합니다. alias 설정이 안 되어 있다면 `k3s kubectl`로 대체하세요.

---

## 1단계: NVIDIA Container Toolkit 설치

K3s가 GPU를 인식하려면 **NVIDIA 컨테이너 툴킷**이 필요합니다.

```bash
# 1. NVIDIA Container Toolkit 저장소 추가
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/libnvidia-container.list

# 2. 툴킷 설치
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 3. [WSL2 필수] CDI(Container Device Interface) 스펙 생성
#    이 단계를 빠뜨리면, 나중에 vLLM 등 GPU 워크로드에서
#    "No CUDA GPUs are available" 에러가 발생합니다.
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
```

> **⚠️ 중요 (2026-02-15 추가)**
> WSL2 환경에서는 반드시 `nvidia-ctk cdi generate` 명령으로 **CDI 스펙 파일**을 생성해야 합니다.
> CDI 스펙이 없으면 `nvidia-container-runtime`이 GPU 디바이스(`/dev/dxg`)를 컨테이너에 올바르게 주입하지 못합니다.
> 이 명령어는 **최초 1회만** 실행하면 됩니다. (GPU 드라이버를 업데이트한 경우 다시 실행하세요.)

---

## 2단계: K3s 설치

먼저 K3s를 설치합니다. K3s가 시작되면 기본 containerd 설정 파일이 생성됩니다.

```bash
curl -sfL https://get.k3s.io | sh -

# (일반 사용자인 경우) kubeconfig 파일 읽기 권한 부여
sudo chmod 644 /etc/rancher/k3s/k3s.yaml

# 노드가 Ready 상태가 될 때까지 대기 (약 30초-1분)
sleep 30
k3s kubectl get nodes
```

> **⚠️ 주의**: K3s는 기본적으로 kubeconfig 파일을 root만 읽을 수 있도록 설정합니다. 일반 사용자로 kubectl을 사용하려면 위와 같이 권한을 변경하거나, K3s 설치 시 `--write-kubeconfig-mode 644` 옵션을 추가하세요.

---

## 3단계: containerd 설정 템플릿 생성 (핵심!)

K3s가 생성한 기본 config.toml을 복사하여 **nvidia runtime을 기본으로** 설정합니다.

```bash
# 1. K3s가 생성한 기본 config.toml을 템플릿으로 복사
sudo cp /var/lib/rancher/k3s/agent/etc/containerd/config.toml /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl

# 2. default_runtime_name = "nvidia" 설정 추가
sudo sed -i "/\[plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc\]/i [plugins.'io.containerd.cri.v1.runtime'.containerd]\n  default_runtime_name = \"nvidia\"\n" /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl

# 3. K3s 재시작하여 설정 적용
sudo systemctl restart k3s

# 4. (일반 사용자인 경우) kubeconfig 권한 재설정 (K3s 재시작 시 리셋됨)
sudo chmod 644 /etc/rancher/k3s/k3s.yaml

# 5. 노드가 Ready 상태인지 확인
sleep 20
k3s kubectl get nodes
```

> **💡 참고**: K3s v1.34+ 버전에서는 containerd v3 설정 형식(`plugins.'io.containerd.cri.v1.runtime'`)을 사용합니다. 이전 버전(v1.28 이하)에서는 `plugins.cri` 형식을 사용할 수 있습니다.

---

## 4단계: WSL2 전용 NVIDIA Device Plugin 배포 (핵심)

기본 Helm 차트의 설정값은 WSL2 환경에 맞지 않습니다. **WSL2의 특수 경로(`/dev/dxg`, `/usr/lib/wsl`)와 runtimeClassName이 적용된 커스텀 YAML**을 사용합니다.

```bash
# 아래 내용을 통째로 복사해서 터미널에 붙여넣으세요.
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nvidia-device-plugin-daemonset
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: nvidia-device-plugin-ds
  template:
    metadata:
      labels:
        name: nvidia-device-plugin-ds
    spec:
      tolerations:
      - key: CriticalAddonsOnly
        operator: Exists
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
      priorityClassName: system-node-critical
      # [K3s 핵심] nvidia runtime 사용 명시
      runtimeClassName: nvidia
      containers:
      - image: nvcr.io/nvidia/k8s-device-plugin:v0.17.0
        name: nvidia-device-plugin-ctr
        securityContext:
          privileged: true
        env:
          - name: FAIL_ON_INIT_ERROR
            value: "false"
          # [WSL2 필수] 드라이버 라이브러리 경로 강제 지정
          - name: LD_LIBRARY_PATH
            value: "/usr/lib/wsl/lib"
          # [WSL2 필수] 모든 GPU 및 드라이버 기능 활성화
          - name: NVIDIA_VISIBLE_DEVICES
            value: "all"
          - name: NVIDIA_DRIVER_CAPABILITIES
            value: "all"
        volumeMounts:
          - name: device-plugin
            mountPath: /var/lib/kubelet/device-plugins
          - name: wsl
            mountPath: /usr/lib/wsl
            readOnly: true
          - name: dxg
            mountPath: /dev/dxg
      volumes:
        - name: device-plugin
          hostPath:
            path: /var/lib/kubelet/device-plugins
        - name: wsl
          hostPath:
            path: /usr/lib/wsl
        - name: dxg
          hostPath:
            path: /dev/dxg
EOF
```

> **⚠️ 변경사항 (2026-02-08 검증)**:
> - `runtimeClassName: nvidia` 추가 - K3s에서 nvidia runtime을 명시적으로 사용
> - 이미지 버전 `v0.17.0`으로 업그레이드 - 최신 GPU 지원 및 안정성 개선
> - `DEVICE_LIST_STRATEGY`, `DEVICE_ID_STRATEGY` 환경변수 제거 - v0.17.0에서 자동 감지

---

## 5단계: 최종 검증 (Verification)

설치 후 약 30초~1분 뒤에 아래 명령어로 확인합니다.

### 1. Device Plugin 상태 확인

```bash
kubectl get pods -n kube-system | grep nvidia
```

> **성공 기준:** Pod 상태가 `Running`이어야 합니다.

### 2. 노드 인식 확인

노드 상세 정보에서 GPU가 보여야 합니다.

```bash
kubectl get node -o jsonpath='{.items[0].status.capacity}' | tr ',' '\n'
```

> **성공 기준:** 출력 결과에 `"nvidia.com/gpu":"1"`이 포함되어야 합니다.

또는:

```bash
kubectl describe node | grep "Allocatable" -A 10
```

### 3. 실제 동작 테스트 (Smoke Test)

실제 파드를 생성하여 `nvidia-smi` 명령어가 작동하는지 확인합니다.

```bash
# 테스트 파드 생성
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: gpu-test
spec:
  restartPolicy: Never
  # [K3s 핵심] nvidia runtime 사용 명시
  runtimeClassName: nvidia
  containers:
  - name: cuda-container
    image: nvidia/cuda:12.3.1-base-ubuntu22.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/gpu: 1
EOF

# (잠시 대기 후) 로그 확인
sleep 20
kubectl logs gpu-test
```

> **성공 기준:** 로그에 호스트와 동일한 **GPU 표(예: RTX 5060 Ti)**가 출력되면 성공입니다.

### 4. 테스트 리소스 정리

검증이 완료되면 테스트용 파드는 삭제하여 클러스터를 정리합니다.

```bash
kubectl delete pod gpu-test
```

> **참고**: `nvidia-device-plugin-daemonset`은 GPU 사용을 위해 계속 실행되어야 하므로 삭제하지 마세요.

---

## 🔧 트러블슈팅

### 1. 노드가 NotReady 상태인 경우

containerd 설정 템플릿이 잘못되었을 수 있습니다. 템플릿을 삭제하고 K3s를 재시작하세요:

```bash
sudo rm /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
sudo systemctl restart k3s
```

그 후 3단계부터 다시 진행하세요.

### 2. Device Plugin에서 "No devices found" 에러

Pod 내에서 nvidia-smi가 작동하는지 확인:

```bash
kubectl exec -n kube-system <nvidia-device-plugin-pod-name> -- nvidia-smi
```

- 작동하면: `runtimeClassName: nvidia`가 제대로 적용된 것입니다.
- 작동하지 않으면: containerd 설정에서 nvidia runtime이 기본으로 설정되지 않았습니다.

### 3. gpu-test Pod에서 GPU가 보이지 않는 경우

Pod 정의에 `runtimeClassName: nvidia`가 있는지 확인하세요. K3s에서는 이 설정이 필수입니다.

### 4. vLLM 등에서 `No CUDA GPUs are available` 에러

`nvidia-smi`는 작동하는데 PyTorch에서 `torch.cuda.is_available()`이 `False`를 반환하는 경우입니다.

**원인 1: CDI 스펙 미생성**

1단계에서 `nvidia-ctk cdi generate` 명령을 실행했는지 확인하세요.

```bash
# CDI 스펙 파일 존재 여부 확인
ls /etc/cdi/nvidia.yaml

# 없다면 생성
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
sudo systemctl restart k3s
```

**원인 2: CUDA compat 드라이버 충돌 (WSL2)**

vLLM 이미지 내부의 `/usr/local/cuda-xx.x/compat/libcuda.so.1`이 WSL2 호스트의 실제 드라이버보다 먼저 로딩되어 CUDA 초기화가 실패할 수 있습니다.
이 경우 Pod의 `env`에 다음을 추가하여 WSL2 드라이버 경로를 우선시해야 합니다.

```yaml
env:
  - name: LD_LIBRARY_PATH
    value: "/usr/lib/wsl/lib:/usr/local/nvidia/lib64:/usr/local/cuda/lib64"
```

> 자세한 내용은 [vLLM 서빙 가이드](/blog/k3s-vllm-serving)의 트러블슈팅 섹션을 참고하세요.

---

## 📋 검증 환경

- **OS**: Windows 11 + WSL2 Ubuntu 24.04
- **K3s**: v1.34.3+k3s1
- **NVIDIA Driver**: 591.44 (Windows) / 590.44.01 (WSL2)
- **NVIDIA Container Toolkit**: 1.18.2
- **GPU**: NVIDIA GeForce RTX 5060 Ti
- **검증일**: 2026-02-08
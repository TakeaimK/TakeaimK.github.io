---
slug: oracle-cloud-openclaw-install
title: "[Cloud] Oracle Cloud 무료 티어 VM 생성 및 Openclaw 설치"
authors: [me]
tags: [oracle, cloud, vm, openclaw, ubuntu]
---

오라클 클라우드(Oracle Cloud)는 놀랍게도 평생 무료(Always Free) 티어를 제공합니다. 이번 포스팅에서는 오라클 클라우드에서 무료 VM(가상 머신)을 생성하고 고정 퍼블릭 IP를 할당받는 방법부터, 최근 핫한 **OpenClaw**를 설치하는 과정까지 함께 살펴봅니다. ☁️

<!--truncate-->

## 1. 회원가입 및 VM 인스턴스 생성 (Create VM Instance)

가장 먼저 오라클 클라우드에 가입하고 컴퓨트 인스턴스를 생성해야 합니다.

1. [Oracle Cloud](https://cloud.oracle.com)에 접속하여 회원가입을 진행합니다. (신용카드 등록이 필요합니다)
   > **Important**: 오라클 가입 시 지역(Region)을 동아시아(춘천 등)로 선택할 경우, 사용자가 많아 무료 티어 자원(Capacity)이 부족해서 인스턴스 생성이 거절될 수 있습니다.
2. 왼쪽 상단 메뉴 아이콘을 눌러 **컴퓨트(Compute) > 인스턴스(Instances)**를 클릭합니다. Free Tier로 최대 2개까지 무료 인스턴스를 만들 수 있습니다.
3. `인스턴스 생성`을 클릭하고 설정을 시작합니다. 기본 서버 이미지는 Oracle Linux 8이지만, 패키지 관리나 네트워크 설정이 좀 더 익숙한 **Ubuntu** 혹은 **CentOS**로 이미지를 변경하는 것을 추천합니다.

### 🔑 SSH 키 생성 및 권한 설정

인스턴스 생성 시 자동으로 SSH 키 쌍을 생성할 수 있습니다. **Private Key**를 다운로드 받아 안전하게 보관해 둡니다.

다운로드한 전용 키를 관리하기 위해 사용자 홈 디렉터리에 `~/keys/` 폴더를 만들고, 아래 명령어처럼 키 권한을 읽기 전용으로 수정합니다. 

```bash
# 예를 들어 다운받은 키 파일명이 ssh-key-2023-07-09.key 일 경우
mkdir -p ~/keys/
mv 다운로드경로/ssh-key-2023-07-09.key ~/keys/
chmod 400 ~/keys/ssh-key-2023-07-09.key
```

#### 📄 권한(400) 상세 설명
`chmod 400` 은 이 키 파일에 대해 파일 소유자 본인에게만 최소한의 **'읽기' 권한**을 부여하는 설정입니다. SSH 환경에서는 키 파일 권한이 넓게 부여되어 있으면 보안 위험으로 판단해 접속을 아예 거부하므로 이 과정이 필수적입니다.


## 2. 퍼블릭 IP 발급 (Public IP)

인스턴스 생성 직후에는 임시 공용 IP가 자동으로 붙습니다. 하지만 인스턴스를 껐다 켤 경우 IP가 변경되어 서버 운영이 까다로워질 수 있습니다. 오라클 프리티어에서는 **고정 퍼블릭 IP**를 1개 무료로 제공합니다.

1. **메뉴 > 네트워킹(Networking) > IP 관리(IP Management) > 예약된 퍼블릭 IP**로 진입합니다.
2. `공용 IP 주소 예약(Reserve Public IP)`을 클릭하여 영구적으로 사용할 IP를 발급받습니다.
   * *참고: 무료 제공량이 1회선 뿐이라, 만약 운이 없이 풀이 꽉 찼다면 "Too many requests" 에러가 날 수 있습니다.*
3. 안정적으로 IP를 받아냈다면, 기존 컴퓨트 인스턴스로 돌아와 네트워크 설정에서 기본으로 잡힌 임시 공용 IP를 **[공용 IP 없음]**으로 변경하여 해제합니다. 이후 방금 취득한 **[예약된 공용 IP]**로 다시 연결해줍니다.


## 3. SSH 접속하기 (SSH Connection)

드디어 서버 콘솔에 원격으로 접속해볼 차례입니다!

터미널에서 `ssh -i ~/keys/ssh-key-2026-00-00.key opc@<발급 받은 Public IP>` 명령으로 접속할 수 있습니다. fingerprint 저장은 `yes` 라고 답합니다. 윈도우의 경우 Git Bash창에서 같은 명령을 사용할 수 있습니다. 우분투 이미지는 opc@ 대신 ubuntu@ 아이디로 접속할 수 있습니다.

```bash
# CentOS 및 Oracle Linux 인스턴스 접속
ssh -i ~/keys/ssh-key-2026-00-00.key opc@<발급_받은_Public_IP>

# Ubuntu 인스턴스 접속
ssh -i ~/keys/ssh-key-2026-00-00.key ubuntu@<발급_받은_Public_IP>
```
> **Tip:** 명령어 입력 후 `Are you sure you want to continue connecting (yes/no/[fingerprint])?` 라는 문구가 나오면 `yes`를 입력하면 됩니다.


## 4. OpenClaw 설치 (Install OpenClaw)

새 클라우드 PC가 생겼으니 이제 **OpenClaw**를 올려보겠습니다.

### 📦 사전 준비 사항
먼저 런타임 환경으로 **Node.js 22 버전 이상**이 필요합니다. 터미널에서 버전을 확인해주세요.
```bash
node --version
```

### 🚀 CLI (명령줄) 간편 설치
Linux 환경에서는 아래 명령어 한 줄로 편리하게 설치 스크립트를 다운받아 실행할 수 있습니다.
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

설치가 완료되면, 초기 온보딩 스크립트를 통해 백그라운드 데몬(Daemon)까지 함께 구성해 줍니다.
```bash
openclaw onboard --install-daemon
```

### ✅ 무결성 검증 (Verification)
설치 및 설정이 성공적으로 이루어졌는지 게이트웨이 상태를 확인하고 대시보드를 열어봅니다.

```bash
# 1. Gateway 상태 확인
openclaw gateway status

# 2. Control UI 띄우기
openclaw dashboard
```
> 상태 명령어 입력 시 Gateway가 정상 동작 중인지 로그나 Active 상태를 확인해 주세요. 대시보드를 통해 브라우저 환경에서 OpenClaw 설정을 직관적으로 제어할 수 있습니다!


## 5. 마무리 (Conclusion)

이렇게 하여 클라우드 상에 무료 호스팅 서버를 띄우고 OpenClaw까지 안전하게 올려보았습니다. 고생 많으셨습니다! 

이후의 OpenClaw 나머지 세부 설정이나 채널 연동에 관련해서는 아래 작성된 기존 로컬 블로그 가이드를 참고하여 진행해 주시기 바랍니다. 😊
* **참고 글:** `AI\2026-02-21-openclaw-설치`

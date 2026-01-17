# Git 하나로 두 곳의 원격 저장소에 동시에 배포하기 (feat. 다중 계정 충돌 해결)

개발을 하다 보면 하나의 로컬 프로젝트를 **두 곳의 GitHub 저장소**에 동시에 올려야 할 때가 있습니다. 예를 들어, 개인 포트폴리오용 저장소와 회사/조직의 저장소 양쪽에 최신 코드를 유지하고 싶은 경우죠.

이번 글에서는 **`git remote` 설정을 통해 한 번의 푸시로 두 저장소에 업로드하는 방법**과, 그 과정에서 발생할 수 있는 **서로 다른 계정 간의 인증 충돌 문제, 권한 문제 해결법**을 정리해 보았습니다.

---

## 1. 목표 시나리오

- **현재 상태**: 로컬 프로젝트가 개인 저장소(`origin`)에 연결되어 있음.
- **목표**: 새로운 조직(Organization) 저장소에도 똑같이 코드를 올리고 싶음.
- **조건**: `git push` 명령어 한 번으로 두 곳 모두에 반영되어야 함.

## 2. 기본 설정: Push URL 추가하기

Git은 하나의 리모트(`origin`)에 여러 개의 Push URL을 가질 수 있습니다. 이를 이용하면 됩니다.

먼저, 현재 설정을 확인해 봅니다.
```bash
git remote -v
# 출력 예시
# origin  https://github.com/user-one/my-project.git (fetch)
# origin  https://github.com/user-one/my-project.git (push)
```

이제 두 번째 저장소 주소를 **Push용 URL**로 추가합니다. 이때 기존 저장소 주소도 한 번 더 명시적으로 추가해 주는 것이 좋습니다.

```bash
# 1. (필요 시) 기존 저장소도 push 목록에 명시적으로 추가
git remote set-url --add --push origin https://github.com/user-one/my-project.git

# 2. 새로운 저장소 추가
git remote set-url --add --push origin https://github.com/organization-two/new-project.git
```

이제 `git remote -v`를 쳐보면 `(push)` 항목이 두 개가 된 것을 볼 수 있습니다. 이론상으로는 이제 `git push`만 하면 양쪽에 다 올라가야 합니다. **하지만...**

---

## 3. 트러블슈팅: 계정이 다를 때 발생하는 문제들

만약 두 저장소의 소유자가 같고 계정도 같다면 위 설정만으로 끝납니다. 하지만 **하나는 개인 계정, 하나는 회사 계정**을 써야 한다면 문제가 복잡해집니다.

### 문제 1: 인증 충돌 (Authentication failed)
GitHub는 기본적으로 `github.com`이라는 도메인 하나에 대해 하나의 인증 정보만 기억합니다. 그래서 두 번째 계정으로 푸시하려고 할 때 자격 증명 오류가 발생할 수 있습니다.

**해결책: URL에 아이디 명시하기**
URL 앞에 사용자 아이디를 붙여주면 Git이 서로 다른 주소로 인식하게 되어 각각 로그인을 처리할 수 있습니다.

```bash
# 잘못된 예 (이메일 사용 X, 도메인 누락 X)
# https://user@email.com@github.com/... (X)

# 올바른 예 (GitHub 사용자명 사용)
git remote set-url --add --push origin https://user-one@github.com/user-one/my-project.git
git remote set-url --add --push origin https://user-two@github.com/organization-two/new-project.git
```
기존에 등록했던 URL을 `set-url --delete`로 지우고, 위와 같이 아이디가 포함된 주소로 다시 등록해 주세요.

### 문제 2: 비밀번호 인증 불가 (미리 토큰 준비!)
2021년 8월부터 GitHub는 터미널에서 **비밀번호 인증을 지원하지 않습니다.**
`Password`를 입력하라는 창이 뜨면, 실제 비밀번호 대신 **Personal Access Token (PAT)**을 입력해야 합니다.

1. GitHub 웹사이트 > Settings > Developer settings > Personal access tokens
2. **Tokens (classic)** 생성
3. **`repo`** 권한 체크 후 생성
4. 생성된 토큰(`ghp_...`)을 복사해서 비밀번호 창에 붙여넣기

### 문제 3: Workflow 권한 오류
만약 프로젝트 안에 GitHub Actions 설정 파일(`.github/workflows/*.yml`)이 포함되어 있다면, 일반 토큰으로는 푸시가 거절될 수 있습니다.

```text
refusing to allow a Personal Access Token to create or update workflow ... without `workflow` scope
```

**해결책: 토큰 권한 추가**
토큰 생성/수정 페이지에서 **`workflow`** 항목을 찾아서 체크해 줍니다. 이 권한이 있어야 `.github` 폴더 내용을 수정하거나 업로드할 수 있습니다.

---

## 4. 최종 결과

모든 설정과 권한 부여가 끝났다면, 이제 한 번의 명령으로 두 저장소 동기화가 가능합니다.

```bash
git push origin --all
```

터미널 로그에서 두 개의 URL로 각각 객체를 전송(Writing objects)하는 메시지가 뜬다면 성공입니다!
이제 번거롭게 두 번 푸시할 필요 없이 편리하게 코드를 관리하세요.

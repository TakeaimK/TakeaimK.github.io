---
slug: ccstatusline-setup
title: "[AI] Claude Code Statusline 설정으로 사용량 확인하기"
authors: [me]
tags: [ai, claude code, statusline, productivity, settings]
---

AI 코딩 어시스턴트인 Claude Code를 터미널에서 사용하다 보면, 현재 모델이 무엇인지, 오늘 혹은 이번 주 토큰 사용량이 얼마나 남았는지 직관적으로 확인하고 싶을 때가 많습니다. 이번 글에서는 **Claude Code 하단에 모델명, Git 정보, 토큰 사용량, 세션 및 주간 사용량을 표시해 주는 상태줄(Statusline) 설정 방법**을 살펴봅니다. 함께 따라 해 보며 터미널을 더 유용하게 꾸며 봅시다!

<!--truncate-->

## 1. 사전 준비 (Prerequisites)

이 설정은 OS 환경에 따라 방법이 약간 다릅니다.

*   **공통 요구사항**: Claude Code 실행 환경 (Windows Terminal, VSCode Git Bash 또는 macOS Terminal)
*   **Windows 사용자**: Node.js 및 npm 설치 필수 (`npx` 명령어를 사용합니다)

> **Tip**: Windows의 경우, bash 스크립트 방식은 Node.js가 Windows 환경 변수(PATH)에서 bash를 제대로 찾지 못해 오류가 발생하기 쉽습니다. 따라서 이미 PATH에 등록되어 있는 `npx`를 활용해 **ccstatusline** 패키지를 사용하는 것을 권장합니다.

---

## 2. Windows 환경 설정 (Git Bash)

Windows에서는 오픈소스인 `ccstatusline` 패키지를 이용해 빠르고 안정적으로 상태줄을 구성해 봅니다.

### 2.1 Claude 설정 수정
먼저, `~/.claude/settings.json` 파일을 열고 다음과 같이 설정합니다. 여기서 주의할 점은 키를 `statusCommand`가 아닌 **`statusLine`** (객체 형식)으로 지정해야 한다는 점입니다.

<details>
<summary>📄 (클릭) ~/.claude/settings.json 보기</summary>

```json
{
  "autoUpdatesChannel": "latest",
  "effortLevel": "high",
  "statusLine": {
    "type": "command",
    "command": "npx -y ccstatusline@latest",
    "padding": 0
  }
}
```

</details>

### 2.2 커스텀 위젯 스크립트 작성 (선택사항)

Mac 버전처럼 `[Model]`, effort 레벨, wall-clock 리셋 시간을 표시하려면 Node.js 스크립트를 추가로 생성해야 합니다. `~/.claude/scripts/` 디렉토리를 만들고 아래 4개의 JavaScript 파일을 작성합니다.

<details>
<summary>📄 (클릭) 스크립트 4종 소스 코드 보기</summary>

**`model-widget.js`** — `[Model]` 형식으로 모델명 출력
```javascript
#!/usr/bin/env node
// Outputs "[Model]" in blue — reads Claude Code JSON from stdin
const fs = require('fs');
try {
  const data = JSON.parse(fs.readFileSync(0, 'utf8'));
  const model = data?.model?.display_name || 'Claude';
  process.stdout.write(`\x1b[38;2;0;153;255m[${model}]\x1b[0m`);
} catch (e) {
  process.stdout.write('\x1b[38;2;0;153;255m[Claude]\x1b[0m');
}
```

**`effort-widget.js`** — effort 레벨 색상 출력
```javascript
#!/usr/bin/env node
// Outputs "effort: high/med/low" in color — reads from settings.json
const fs = require('fs');
const os = require('os');
const path = require('path');

let effort = process.env.CLAUDE_CODE_EFFORT_LEVEL || 'high';
try {
  const s = JSON.parse(fs.readFileSync(path.join(os.homedir(), '.claude', 'settings.json'), 'utf8'));
  if (s.effortLevel) effort = s.effortLevel;
} catch (e) {}

const RST = '\x1b[0m';
const color = effort === 'low'    ? '\x1b[2m'
            : effort === 'medium' ? '\x1b[38;2;255;176;85m'
            :                       '\x1b[38;2;0;160;0m';
const label = effort === 'medium' ? 'med' : effort;

process.stdout.write(`effort: ${color}${label}${RST}`);
```

**`usage-5h.js`** — `⏰ 5h X% @H:MMam` 출력 (Anthropic OAuth API, 60s 캐시)
```javascript
#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const https = require('https');

const CACHE = path.join(os.tmpdir(), 'ccstatusline-usage.json');
const TTL = 60 * 1000;
const RST = '\x1b[0m', DIM = '\x1b[2m', WHT = '\x1b[38;2;220;220;220m';

function color(pct) {
  if (pct >= 90) return '\x1b[38;2;255;85;85m';
  if (pct >= 70) return '\x1b[38;2;255;176;85m';
  if (pct >= 50) return '\x1b[38;2;230;200;0m';
  return '\x1b[38;2;0;160;0m';
}

function getToken() {
  try {
    const c = JSON.parse(fs.readFileSync(path.join(os.homedir(), '.claude', '.credentials.json'), 'utf8'));
    return c?.claudeAiOauth?.accessToken || null;
  } catch (e) { return null; }
}

function fetchUsage(token) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.anthropic.com', path: '/api/oauth/usage', method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'anthropic-beta': 'oauth-2025-04-20',
        'User-Agent': 'claude-code/2.1.34'
      }
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.setTimeout(7000, () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

async function getData() {
  try {
    const stat = fs.statSync(CACHE);
    if (Date.now() - stat.mtimeMs < TTL) return JSON.parse(fs.readFileSync(CACHE, 'utf8'));
  } catch (e) {}
  const token = getToken();
  if (!token) return null;
  try {
    const data = await fetchUsage(token);
    fs.writeFileSync(CACHE, JSON.stringify(data));
    return data;
  } catch (e) {
    try { return JSON.parse(fs.readFileSync(CACHE, 'utf8')); } catch (e2) { return null; }
  }
}

async function main() {
  const data = await getData();
  if (!data?.five_hour) return;

  // utilization은 이미 퍼센트 값 (예: 15.0 = 15%) — * 100 하면 안 됨
  const pct = Math.round(data.five_hour.utilization || 0);
  const c = color(pct);

  let resetStr = '';
  if (data.five_hour.resets_at) {
    const d = new Date(data.five_hour.resets_at);
    let h = d.getHours();
    const m = d.getMinutes().toString().padStart(2, '0');
    const ampm = h >= 12 ? 'pm' : 'am';
    h = h % 12 || 12;
    resetStr = ` ${DIM}@${h}:${m}${ampm}${RST}`;
  }

  process.stdout.write(`\u23f0 ${WHT}5h${RST} ${c}${pct}%${RST}${resetStr}`);
}
main().catch(() => {});
```

**`usage-7d.js`** — `📅 7d X% @mon D` 출력 (usage-5h.js와 캐시 공유)
```javascript
#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const https = require('https');

const CACHE = path.join(os.tmpdir(), 'ccstatusline-usage.json');
const TTL = 60 * 1000;
const RST = '\x1b[0m', DIM = '\x1b[2m', WHT = '\x1b[38;2;220;220;220m';

function color(pct) {
  if (pct >= 90) return '\x1b[38;2;255;85;85m';
  if (pct >= 70) return '\x1b[38;2;255;176;85m';
  if (pct >= 50) return '\x1b[38;2;230;200;0m';
  return '\x1b[38;2;0;160;0m';
}

function getToken() {
  try {
    const c = JSON.parse(fs.readFileSync(path.join(os.homedir(), '.claude', '.credentials.json'), 'utf8'));
    return c?.claudeAiOauth?.accessToken || null;
  } catch (e) { return null; }
}

function fetchUsage(token) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.anthropic.com', path: '/api/oauth/usage', method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'anthropic-beta': 'oauth-2025-04-20',
        'User-Agent': 'claude-code/2.1.34'
      }
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.setTimeout(7000, () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

async function getData() {
  try {
    const stat = fs.statSync(CACHE);
    if (Date.now() - stat.mtimeMs < TTL) return JSON.parse(fs.readFileSync(CACHE, 'utf8'));
  } catch (e) {}
  const token = getToken();
  if (!token) return null;
  try {
    const data = await fetchUsage(token);
    fs.writeFileSync(CACHE, JSON.stringify(data));
    return data;
  } catch (e) {
    try { return JSON.parse(fs.readFileSync(CACHE, 'utf8')); } catch (e2) { return null; }
  }
}

async function main() {
  const data = await getData();
  if (!data?.seven_day) return;

  // utilization은 이미 퍼센트 값 (예: 15.0 = 15%) — * 100 하면 안 됨
  const pct = Math.round(data.seven_day.utilization || 0);
  const c = color(pct);

  const MONTHS = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'];
  let resetStr = '';
  if (data.seven_day.resets_at) {
    const d = new Date(data.seven_day.resets_at);
    resetStr = ` ${DIM}@${MONTHS[d.getMonth()]} ${d.getDate()}${RST}`;
  }

  process.stdout.write(`\ud83d\udcc5 ${WHT}7d${RST} ${c}${pct}%${RST}${resetStr}`);
}
main().catch(() => {});
```
</details>

> **주의:** API 응답의 `utilization` 필드는 이미 퍼센트 값(예: `15.0`)이므로 스크립트에서 `* 100`을 추가로 하지 않습니다.

### 2.3 ccstatusline 세부 설정 (`settings.json`)
이제 ccstatusline 전용 설정 파일을 만들어 줍니다. 위에서 만든 커스텀 위젯을 적용해 3줄로 화면이 구성되도록 지정할 수 있습니다. (`[Model]`/Git/effort → 컨텍스트 바 → 토큰/사용량)

<details>
<summary>📄 (클릭) ~/.config/ccstatusline/settings.json 보기</summary>

```json
{
  "version": 3,
  "lines": [
    [
      {
        "id": "1",
        "type": "custom-command",
        "commandPath": "node C:/Users/YOUR_USERNAME/.claude/scripts/model-widget.js",
        "preserveColors": true,
        "timeout": 3000
      },
      {
        "id": "2",
        "type": "separator"
      },
      {
        "id": "3",
        "type": "git-branch",
        "color": "green"
      },
      {
        "id": "4",
        "type": "separator"
      },
      {
        "id": "5",
        "type": "git-changes",
        "color": "yellow"
      },
      {
        "id": "6",
        "type": "separator"
      },
      {
        "id": "7",
        "type": "custom-command",
        "commandPath": "node C:/Users/YOUR_USERNAME/.claude/scripts/effort-widget.js",
        "preserveColors": true,
        "timeout": 3000
      }
    ],
    [
      {
        "id": "8",
        "type": "context-bar",
        "color": "green"
      }
    ],
    [
      {
        "id": "9",
        "type": "tokens-total",
        "color": "brightWhite"
      },
      {
        "id": "10",
        "type": "separator"
      },
      {
        "id": "11",
        "type": "custom-command",
        "commandPath": "node C:/Users/YOUR_USERNAME/.claude/scripts/usage-5h.js",
        "preserveColors": true,
        "timeout": 10000
      },
      {
        "id": "12",
        "type": "separator"
      },
      {
        "id": "13",
        "type": "custom-command",
        "commandPath": "node C:/Users/YOUR_USERNAME/.claude/scripts/usage-7d.js",
        "preserveColors": true,
        "timeout": 10000
      }
    ]
  ],
  "flexMode": "full-minus-40",
  "compactThreshold": 60,
  "colorLevel": 2,
  "inheritSeparatorColors": false,
  "globalBold": false,
  "powerline": {
    "enabled": false,
    "separators": [""],
    "separatorInvertBackground": [false],
    "startCaps": [],
    "endCaps": [],
    "autoAlign": false
  }
}
```

</details>

> **Important**: `YOUR_USERNAME`을 실제 Windows 사용자명으로 교체해야 하며, 경로는 반드시 슬래시 대신 **백슬래시가 아닌 슬래시(`/`)** 를 사용해 주세요!

#### 📄 파일 상세 설명

위 설정 파일에 나오는 주요 위젯 타입은 다음과 같습니다 (타입명은 모두 **kebab-case**로 작성됩니다).

| 위젯 타입명 | 설명 |
|---|---|
| `custom-command` | Node.js 스크립트 등 외부 명령 실행 필드 |
| `model` | 현재 사용 중인 Claude 모델명 (기본 위젯) |
| `git-branch` | 적용 중인 프로젝트 Git 브랜치 |
| `git-changes` | 삽입/삭제된 코드 줄 수 |
| `context-bar` | 컨텍스트 윈도우 한계 대비 진행바, 사용 토큰수 |
| `tokens-total` | 입력/출력/캐시를 모두 합친 누적 토큰 |

> **Note**: `tokens-total`은 출력을 포함한 전체 누적이지만, `context-bar`의 토큰 수는 입력과 캐시만 고려한 컨텍스트 윈도우 기준입니다.

### 2.4 검증 및 결과 확인
설정을 마친 후 Claude Code를 실행하면 커스텀 위젯이 적용되어 아래와 같이 더욱 향상된 상태줄을 볼 수 있습니다.

```bash
# 출력 예시
[Claude Sonnet 4.6] | main | (+0 ~2) | effort: high
Context: [████░░░░░░░░░░░░] 6k/200k (3%)
Total: 11.3k | ⏰ 5h 31% @7:59pm | 📅 7d 16% @mar 11
```

---

## 3. macOS 환경 설정 (Bash 스크립트)

macOS에서는 커스텀 **Bash 스크립트** 방식을 적용해 볼 수 있습니다. 직접 Anthropic OAuth API를 호출하므로 남은 리셋 시간을 wall-clock(벽시계) 형식(`@5:00pm`)으로 직관적으로 표시해 주는 장점이 있습니다.

### 3.1 Claude 설정 수정
`~/.claude/settings.json`을 열어 `statusline.sh` 스크립트를 바라보도록 설정합니다.

<details>
<summary>📄 (클릭) ~/.claude/settings.json 보기</summary>

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh",
    "padding": 0
  }
}
```

</details>

### 3.2 Bash 스크립트 작성
아래 스크립트 내용을 복사하여 `~/.claude/statusline.sh` 파일로 저장합니다. 꽤 긴 스크립트이므로 토글 기능으로 접어두었습니다!

<details>
<summary>📄 (클릭) ~/.claude/statusline.sh 보기</summary>

```bash
#!/usr/bin/env bash
# Claude Code status line — 2-line output
# Line 1: [Model] | repo@branch (git status) | effort: level
# Line 2: ██████░░░░ 50k/200k (25%) | 5h 12% @3:30pm | 7d 45% @mar 8 | extra $2.50/$10.00

set -f  # disable globbing

# ── Colors ───────────────────────────────────────────────────────────────────
ESC=$'\033'
blue="${ESC}[38;2;0;153;255m"
orange="${ESC}[38;2;255;176;85m"
green="${ESC}[38;2;0;160;0m"
cyan="${ESC}[38;2;46;149;153m"
red="${ESC}[38;2;255;85;85m"
yellow="${ESC}[38;2;230;200;0m"
white="${ESC}[38;2;220;220;220m"
dim="${ESC}[2m"
reset="${ESC}[0m"

# OSC 8 hyperlink components
OSC_OPEN="${ESC}]8;;"
OSC_ST="${ESC}\\"

# ── Helpers ───────────────────────────────────────────────────────────────────

format_tokens() {
    local num=$1
    if [ "$num" -ge 1000000 ]; then
        awk "BEGIN {printf \"%.1fm\", $num / 1000000}"
    elif [ "$num" -ge 1000 ]; then
        awk "BEGIN {printf \"%.0fk\", $num / 1000}"
    else
        printf "%d" "$num"
    fi
}

usage_color() {
    local pct=$1
    if [ "$pct" -ge 90 ]; then echo "$red"
    elif [ "$pct" -ge 70 ]; then echo "$orange"
    elif [ "$pct" -ge 50 ]; then echo "$yellow"
    else echo "$green"
    fi
}

get_oauth_token() {
    if [ -n "$CLAUDE_CODE_OAUTH_TOKEN" ]; then
        echo "$CLAUDE_CODE_OAUTH_TOKEN"
        return 0
    fi

    if command -v security >/dev/null 2>&1; then
        local blob
        blob=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null)
        if [ -n "$blob" ]; then
            local token
            token=$(echo "$blob" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
            if [ -n "$token" ] && [ "$token" != "null" ]; then
                echo "$token"
                return 0
            fi
        fi
    fi

    local creds_file="${HOME}/.claude/.credentials.json"
    if [ -f "$creds_file" ]; then
        local token
        token=$(jq -r '.claudeAiOauth.accessToken // empty' "$creds_file" 2>/dev/null)
        if [ -n "$token" ] && [ "$token" != "null" ]; then
            echo "$token"
            return 0
        fi
    fi

    if command -v secret-tool >/dev/null 2>&1; then
        local blob
        blob=$(timeout 2 secret-tool lookup service "Claude Code-credentials" 2>/dev/null)
        if [ -n "$blob" ]; then
            local token
            token=$(echo "$blob" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
            if [ -n "$token" ] && [ "$token" != "null" ]; then
                echo "$token"
                return 0
            fi
        fi
    fi

    echo ""
}

iso_to_epoch() {
    local iso_str="$1"
    local epoch

    # Try GNU date first (Linux)
    epoch=$(date -d "${iso_str}" +%s 2>/dev/null)
    if [ -n "$epoch" ]; then echo "$epoch"; return 0; fi

    # BSD date (macOS) — strip fractional seconds and timezone
    local stripped="${iso_str%%.*}"
    stripped="${stripped%%Z}"
    stripped="${stripped%%+*}"
    stripped="${stripped%%-[0-9][0-9]:[0-9][0-9]}"

    if [[ "$iso_str" == *"Z"* ]] || [[ "$iso_str" == *"+00:00"* ]] || [[ "$iso_str" == *"-00:00"* ]]; then
        epoch=$(env TZ=UTC date -j -f "%Y-%m-%dT%H:%M:%S" "$stripped" +%s 2>/dev/null)
    else
        epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$stripped" +%s 2>/dev/null)
    fi

    [ -n "$epoch" ] && echo "$epoch" && return 0
    return 1
}

# style: "time" → "3:30pm"  |  "date" → "mar 8"
format_reset_time() {
    local iso_str="$1"
    local style="$2"
    [ -z "$iso_str" ] || [ "$iso_str" = "null" ] && return

    local epoch
    epoch=$(iso_to_epoch "$iso_str")
    [ -z "$epoch" ] && return

    case "$style" in
        time)
            LC_TIME=C date -j -r "$epoch" +"%l:%M%p" 2>/dev/null | sed 's/^ //' | tr '[:upper:]' '[:lower:]' || \
            LC_TIME=C date -d "@$epoch" +"%l:%M%P" 2>/dev/null | sed 's/^ //'
            ;;
        date)
            LC_TIME=C date -j -r "$epoch" +"%b %-d" 2>/dev/null | sed 's/^ //; s/  / /g' | tr '[:upper:]' '[:lower:]' || \
            LC_TIME=C date -d "@$epoch" +"%b %-d" 2>/dev/null | sed 's/^ //; s/  / /g'
            ;;
    esac
}

# ── Read input ────────────────────────────────────────────────────────────────

JSON=$(cat)

if [ -z "$JSON" ]; then
    printf "Claude\n"
    exit 0
fi

# ── Parse JSON ────────────────────────────────────────────────────────────────

MODEL=$(echo "$JSON" | jq -r '.model.display_name // "Claude"')
CURRENT_DIR=$(echo "$JSON" | jq -r '.workspace.current_dir // .cwd // ""')

# Token counts
CTX_SIZE=$(echo "$JSON" | jq -r '.context_window.context_window_size // 200000')
[ "$CTX_SIZE" -eq 0 ] 2>/dev/null && CTX_SIZE=200000

INPUT_TOKENS=$(echo "$JSON" | jq -r '.context_window.current_usage.input_tokens // 0')
CACHE_CREATE=$(echo "$JSON" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
CACHE_READ=$(echo "$JSON" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
CURRENT=$(( INPUT_TOKENS + CACHE_CREATE + CACHE_READ ))

USED_TOKENS=$(format_tokens "$CURRENT")
TOTAL_TOKENS=$(format_tokens "$CTX_SIZE")

if [ "$CTX_SIZE" -gt 0 ]; then
    PCT_USED=$(( CURRENT * 100 / CTX_SIZE ))
else
    PCT_USED=$(echo "$JSON" | jq -r '.context_window.used_percentage // 0' | awk '{printf "%.0f", $1}')
fi

# Effort level
EFFORT="high"
if [ -n "$CLAUDE_CODE_EFFORT_LEVEL" ]; then
    EFFORT="$CLAUDE_CODE_EFFORT_LEVEL"
elif [ -f "$HOME/.claude/settings.json" ]; then
    eff_val=$(jq -r '.effortLevel // empty' "$HOME/.claude/settings.json" 2>/dev/null)
    [ -n "$eff_val" ] && EFFORT="$eff_val"
fi

# ── Git info (5s cache) ───────────────────────────────────────────────────────

GIT_CACHE="/tmp/statusline-git-cache"
NOW=$(date +%s)
CACHE_AGE=999

if [[ -f "$GIT_CACHE" ]]; then
    CACHE_MTIME=$(stat -f %m "$GIT_CACHE" 2>/dev/null || stat -c %Y "$GIT_CACHE" 2>/dev/null)
    CACHE_AGE=$(( NOW - CACHE_MTIME ))
fi

IS_GIT=0
BRANCH=""
STAGED=0
MODIFIED=0
UNTRACKED=0
REMOTE_URL=""
REPO_NAME=""

if [[ $CACHE_AGE -lt 5 && -f "$GIT_CACHE" ]]; then
    source "$GIT_CACHE"
elif [[ -n "$CURRENT_DIR" ]] && git --no-optional-locks -C "$CURRENT_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
    IS_GIT=1
    BRANCH=$(git --no-optional-locks -C "$CURRENT_DIR" branch --show-current 2>/dev/null)

    STATUS=$(git --no-optional-locks -C "$CURRENT_DIR" status --porcelain 2>/dev/null)
    STAGED=$(echo "$STATUS" | grep -c '^[MADRC]' || true)
    MODIFIED=$(echo "$STATUS" | grep -c '^ [MD]' || true)
    UNTRACKED=$(echo "$STATUS" | grep -c '^??' || true)

    REMOTE_URL=$(git --no-optional-locks -C "$CURRENT_DIR" remote get-url origin 2>/dev/null || true)
    if [[ "$REMOTE_URL" =~ ^git@([^:]+):(.+) ]]; then
        REMOTE_URL="https://${BASH_REMATCH[1]}/${BASH_REMATCH[2]%.git}"
    elif [[ "$REMOTE_URL" =~ \.git$ ]]; then
        REMOTE_URL="${REMOTE_URL%.git}"
    fi

    REPO_NAME=$(basename "$CURRENT_DIR")

    cat > "$GIT_CACHE" <<EOF
IS_GIT=$IS_GIT
BRANCH=$(printf '%q' "$BRANCH")
STAGED=$STAGED
MODIFIED=$MODIFIED
UNTRACKED=$UNTRACKED
REMOTE_URL=$(printf '%q' "$REMOTE_URL")
REPO_NAME=$(printf '%q' "$REPO_NAME")
EOF
fi

# ── LINE 1: [Model] | repo@branch (git status) | effort: level ───────────────

LINE1="${blue}[${MODEL}]${reset}"

if [[ $IS_GIT -eq 1 ]]; then
    if [[ -n "$REMOTE_URL" ]]; then
        REPO_LINK="${OSC_OPEN}${REMOTE_URL}${OSC_ST}${REPO_NAME}${OSC_OPEN}${OSC_ST}"
    else
        REPO_LINK="$REPO_NAME"
    fi

    GIT_INDICATORS=""
    [[ $STAGED -gt 0 ]]    && GIT_INDICATORS+="${green}+${STAGED}${reset}"
    [[ $MODIFIED -gt 0 ]]  && { [[ -n "$GIT_INDICATORS" ]] && GIT_INDICATORS+=" "; GIT_INDICATORS+="${yellow}~${MODIFIED}${reset}"; }
    [[ $UNTRACKED -gt 0 ]] && { [[ -n "$GIT_INDICATORS" ]] && GIT_INDICATORS+=" "; GIT_INDICATORS+="${red}?${UNTRACKED}${reset}"; }

    DIR_PART="📁 ${cyan}${REPO_LINK}${reset} ${dim}|${reset} 🌿 ${green}${BRANCH}${reset}"
    [[ -n "$GIT_INDICATORS" ]] && DIR_PART+=" ${dim}(${reset}${GIT_INDICATORS}${dim})${reset}"

    LINE1+=" ${dim}|${reset} ${DIR_PART}"
elif [[ -n "$CURRENT_DIR" ]]; then
    LINE1+=" ${dim}|${reset} 📁 ${cyan}$(basename "$CURRENT_DIR")${reset}"
fi

LINE1+=" ${dim}|${reset} effort: "
case "$EFFORT" in
    low)    LINE1+="${dim}low${reset}" ;;
    medium) LINE1+="${orange}med${reset}" ;;
    *)      LINE1+="${green}high${reset}" ;;
esac

# ── LINE 2: Context bar | 5h | 7d | extra ────────────────────────────────────

FILLED=$(( PCT_USED / 10 ))
EMPTY=$(( 10 - FILLED ))
BAR=""
for (( i=0; i<FILLED; i++ )); do BAR+="█"; done
for (( i=0; i<EMPTY; i++ )); do BAR+="░"; done

BAR_COLOR=$(usage_color "$PCT_USED")
SEP=" ${dim}|${reset} "

LINE2="${BAR_COLOR}${BAR}${reset} ${white}${USED_TOKENS}/${TOTAL_TOKENS}${reset} ${dim}(${reset}${BAR_COLOR}${PCT_USED}%${reset}${dim})${reset}"

# ── Usage limits from API (60s cache) ────────────────────────────────────────

USAGE_CACHE="/tmp/claude/statusline-usage-cache.json"
mkdir -p /tmp/claude

NEEDS_REFRESH=true
USAGE_DATA=""

if [ -f "$USAGE_CACHE" ]; then
    USAGE_MTIME=$(stat -f %m "$USAGE_CACHE" 2>/dev/null || stat -c %Y "$USAGE_CACHE" 2>/dev/null)
    USAGE_AGE=$(( NOW - USAGE_MTIME ))
    if [ "$USAGE_AGE" -lt 60 ]; then
        NEEDS_REFRESH=false
        USAGE_DATA=$(cat "$USAGE_CACHE" 2>/dev/null)
    fi
fi

if $NEEDS_REFRESH; then
    TOKEN=$(get_oauth_token)
    if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
        RESPONSE=$(curl -s --max-time 10 \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -H "anthropic-beta: oauth-2025-04-20" \
            -H "User-Agent: claude-code/2.1.34" \
            "https://api.anthropic.com/api/oauth/usage" 2>/dev/null)
        if [ -n "$RESPONSE" ] && echo "$RESPONSE" | jq . >/dev/null 2>&1; then
            USAGE_DATA="$RESPONSE"
            echo "$RESPONSE" > "$USAGE_CACHE"
        fi
    fi
    if [ -z "$USAGE_DATA" ] && [ -f "$USAGE_CACHE" ]; then
        USAGE_DATA=$(cat "$USAGE_CACHE" 2>/dev/null)
    fi
fi

if [ -n "$USAGE_DATA" ] && echo "$USAGE_DATA" | jq -e . >/dev/null 2>&1; then
    FIVE_PCT=$(echo "$USAGE_DATA" | jq -r '.five_hour.utilization // 0' | awk '{printf "%.0f", $1}')
    FIVE_RESET=$(format_reset_time "$(echo "$USAGE_DATA" | jq -r '.five_hour.resets_at // empty')" "time")
    FIVE_COLOR=$(usage_color "$FIVE_PCT")

    LINE2+="${SEP}⏰ ${white}5h${reset} ${FIVE_COLOR}${FIVE_PCT}%${reset}"
    [ -n "$FIVE_RESET" ] && LINE2+=" ${dim}@${FIVE_RESET}${reset}"

    SEVEN_PCT=$(echo "$USAGE_DATA" | jq -r '.seven_day.utilization // 0' | awk '{printf "%.0f", $1}')
    SEVEN_RESET=$(format_reset_time "$(echo "$USAGE_DATA" | jq -r '.seven_day.resets_at // empty')" "date")
    SEVEN_COLOR=$(usage_color "$SEVEN_PCT")

    LINE2+="${SEP}📅 ${white}7d${reset} ${SEVEN_COLOR}${SEVEN_PCT}%${reset}"
    [ -n "$SEVEN_RESET" ] && LINE2+=" ${dim}@${SEVEN_RESET}${reset}"

    EXTRA_ENABLED=$(echo "$USAGE_DATA" | jq -r '.extra_usage.is_enabled // false')
    if [ "$EXTRA_ENABLED" = "true" ]; then
        EXTRA_PCT=$(echo "$USAGE_DATA" | jq -r '.extra_usage.utilization // 0' | awk '{printf "%.0f", $1}')
        EXTRA_USED=$(echo "$USAGE_DATA" | jq -r '.extra_usage.used_credits // 0' | awk '{printf "%.2f", $1/100}')
        EXTRA_LIMIT=$(echo "$USAGE_DATA" | jq -r '.extra_usage.monthly_limit // 0' | awk '{printf "%.2f", $1/100}')
        EXTRA_COLOR=$(usage_color "$EXTRA_PCT")

        LINE2+="${SEP}${white}extra${reset} ${EXTRA_COLOR}\$${EXTRA_USED:-0.00}/\$${EXTRA_LIMIT:-0.00}${reset}"
    fi
fi

# ── Output ────────────────────────────────────────────────────────────────────

printf "%s\n" "$LINE1"
printf "%s\n" "$LINE2"
```

</details>

#### 📄 파일 상세 설명
해당 쉘 스크립트는 `jq` 명령어로 JSON을 파싱하고, 터미널 색상 출력, OAuth 토큰을 활용한 API 통신 기능까지 모두 포함하고 있어 꽤 유용합니다. 스크립트 특성상, 작성한 후에는 반드시 **실행 권한을 부여**해 주어야 합니다.

<br/>

터미널에서 아래 명령어로 권한을 부여해 주세요.

```bash
chmod +x ~/.claude/statusline.sh
```

### 3.3 검증 및 결과 확인
설정 후 출력되는 모습은 아래와 같습니다.

```bash
# 출력 예시
[claude-opus-4-5] | 📁 my-repo | 🌿 main (+2 ~1) | effort: high
░░░░░░████ 32k/200k (15%) | ⏰ 5h 24% @5:00pm | 📅 7d 53% @mar 6
```


## 마무리 및 트러블슈팅 (Troubleshooting)

만약 `~/.claude/settings.json` 설정에 `statusCommand`를 사용하게 되면 인식하지 않는 문제가 알려져 있습니다. 반드시 `statusLine` 키를 통해 객체 타입으로 적용해 주시기 바랍니다.
또한 Windows 사용 시 bash 스크립트를 직접 실행하려고 하면 오류가 발생할 수 있으므로, Node 기반의 `npx ccstatusline@latest` 사용 패턴을 잊지 마세요.

이제 좀 더 시각화된 Claude Code 환경에서 생산성 높은 개발 작업을 이어가 보세요!

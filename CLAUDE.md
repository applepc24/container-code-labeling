# 프로젝트 가이드라인

> 이 문서는 Claude Code가 자동으로 읽는 프로젝트 가이드라인입니다.

## 프로젝트 개요

**프로젝트명**: 영상 프레임 추출 및 바운딩 박스 어노테이션 ML 파이프라인

**목적**: 영상에서 프레임을 추출하고, 추출된 프레임에 대해 바운딩 박스 어노테이션을 수행하여 객체 탐지 모델 학습용 데이터셋을 구축하는 파이프라인 개발

**기술 스택**:
- Python 3.10+
- OpenCV, FFmpeg (영상 처리)
- PyTorch (딥러닝)
- LabelStudio/Supervision (어노테이션)

**팀 규모**: 3명 협업

---

## 디렉토리 구조

```
labeling_project/
├── data/                      # 데이터 저장 (영상별로 폴더 구분)
│   ├── video1/                # 영상1 작업 폴더
│   │   ├── raw/               # 원본 영상 파일
│   │   ├── frames/            # 추출된 프레임 이미지
│   │   └── annotations/       # 어노테이션 결과 (JSON, XML 등)
│   ├── video2/                # 영상2 작업 폴더
│   │   ├── raw/
│   │   ├── frames/
│   │   └── annotations/
│   ├── video3/                # 영상3 작업 폴더
│   │   ├── raw/
│   │   ├── frames/
│   │   └── annotations/
│   └── work_allocation.md     # 작업 할당 관리 파일 (Git 추적)
├── src/                       # 소스 코드
│   ├── extraction/            # 프레임 추출 모듈
│   ├── annotation/            # 어노테이션 관련 모듈
│   ├── utils/                 # 유틸리티 함수
│   └── __init__.py
├── models/                    # 학습된 모델 저장 (Git 제외)
├── notebooks/                 # Jupyter 노트북 (EDA, 실험)
├── tests/                     # 단위 테스트
├── requirements.txt           # Python 의존성 패키지
├── .gitignore                 # Git 제외 파일 목록
├── CLAUDE.md                  # 이 파일 (프로젝트 가이드라인)
└── README.md                  # 프로젝트 설명 (사용자용)
```

### 폴더 구조 설명

- **영상별 폴더**: 각 영상마다 독립적인 폴더(`video1/`, `video2/`, ...)를 생성하여 작업
- **작업자별 할당**: `data/work_allocation.md`에서 누가 어떤 영상을 작업하는지 관리
- **Git 충돌 방지**: 각 작업자가 서로 다른 폴더에서 작업하므로 파일 충돌 없음
- **유연한 작업 분배**: 작업자가 여러 영상을 담당하거나, 한 영상을 여러 명이 나눠서 작업 가능

---

## 코딩 컨벤션

### 네이밍 규칙
- **함수명, 변수명**: `snake_case` (예: `extract_frames`, `video_path`)
- **클래스명**: `PascalCase` (예: `VideoExtractor`, `AnnotationManager`)
- **상수**: `UPPER_SNAKE_CASE` (예: `MAX_FRAME_COUNT`, `DEFAULT_FPS`)
- **Private 변수/함수**: 앞에 `_` (예: `_internal_helper`)

### 타입 힌트
- **모든 함수는 타입 힌트 필수**
  ```python
  def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> list[str]:
      """영상에서 프레임을 추출합니다."""
      pass
  ```

### Docstring
- **모든 함수와 클래스에 docstring 작성** (Google 스타일 권장)
  ```python
  def process_video(video_path: str) -> None:
      """
      영상 파일을 처리하여 프레임을 추출합니다.

      Args:
          video_path: 처리할 영상 파일 경로

      Returns:
          None

      Raises:
          FileNotFoundError: 영상 파일이 존재하지 않을 때
      """
      pass
  ```

### 임포트 순서
1. 표준 라이브러리
2. 서드파티 라이브러리
3. 로컬 모듈

```python
import os
from pathlib import Path

import cv2
import numpy as np
import torch

from src.utils.helpers import validate_path
```

---

## Git 브랜치 전략

### 브랜치 구조
- **`main`**: 안정적인 메인 브랜치 (작업 완료 후 병합)
- **`feature/<기능명>`**: 새로운 기능 개발 (예: `feature/frame-extraction`)
- **`bugfix/<버그명>`**: 버그 수정 (예: `bugfix/video-path-error`)

### 작업 흐름
1. `main` 브랜치에서 `feature/<기능명>` 브랜치 생성
2. 기능 개발 완료 후 `main`으로 Pull Request
3. 코드 리뷰 후 Merge

### 커밋 메시지 형식
```
<타입>: <제목>

<본문 (선택사항)>
```

**타입**:
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `refactor`: 코드 리팩토링
- `docs`: 문서 수정
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드, 설정 파일 수정

**예시**:
```
feat: 영상 프레임 추출 기능 추가

OpenCV를 사용하여 영상에서 지정된 FPS로 프레임을 추출하는 함수 구현
```

---

## Claude Code 사용 규칙

### 병렬 작업 시 주의사항
- **동일한 파일을 동시에 수정하지 않기**: Claude Code를 여러 명이 사용할 때 파일 충돌 방지
- **작업 범위 명시**: Claude에게 작업 요청 시 "src/extraction/video.py의 extract_frames 함수만 수정해줘" 처럼 구체적으로 지시

### 작업 범위 예시
- ✅ "src/extraction/ 폴더에 프레임 추출 함수 추가해줘"
- ✅ "tests/test_extraction.py에 단위 테스트 작성해줘"
- ❌ "전체 프로젝트 리팩토링 해줘" (범위가 너무 넓음)

### 코드 리뷰 요청
- Claude Code가 작성한 코드는 팀원이 리뷰 후 Merge
- 중요한 로직 변경은 반드시 팀원과 논의

---

## 데이터 관리 규칙

### 영상별 폴더 구조 원칙
- **영상마다 독립적인 폴더**: `data/video1/`, `data/video2/`, `data/video3/` 등
- **작업 할당 파일**: `data/work_allocation.md`에 누가 어떤 영상을 작업하는지 기록
  ```markdown
  # 작업 할당

  - video1: 김철수 (진행중) - 2026-04-17 시작
  - video2: 이영희 (완료) - 2026-04-17 완료
  - video3: 박민수 (대기)
  ```

### 원본 영상 파일
- **저장 위치**: 각 영상 폴더의 `raw/` (예: `data/video1/raw/video1.mp4`)
- **Git 제외**: 용량이 크므로 Git에 커밋하지 않음
- **로컬 작업**: 공유 드라이브에서 다운로드하여 해당 폴더에 저장

### 추출된 프레임
- **저장 위치**: 각 영상 폴더의 `frames/` (예: `data/video1/frames/`)
- **Git 제외**: 용량이 크므로 Git에 커밋하지 않음
- **필요 시 재생성**: 원본 영상이 있으면 언제든 프레임 재추출 가능

### 어노테이션 결과
- **저장 위치**: 각 영상 폴더의 `annotations/` (예: `data/video1/annotations/`)
- **Git 추적 권장**: JSON 파일은 용량이 작으므로 Git에 커밋하여 팀원과 공유
- **백업 필수**: 어노테이션 작업은 시간이 많이 소요되므로 주기적으로 Git push

### 작업 흐름 예시
1. 김철수가 `video1` 담당 → `data/video1/` 폴더에서 작업
2. 이영희가 `video2` 담당 → `data/video2/` 폴더에서 작업
3. 박민수가 `video3` 담당 → `data/video3/` 폴더에서 작업
4. 각자 독립적인 폴더에서 작업하므로 **Git 충돌 없음**

---

## 의존성 관리

### Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 새로운 패키지 추가 시
1. `pip install <패키지명>`
2. `pip freeze > requirements.txt` (또는 수동으로 `requirements.txt` 업데이트)
3. Git에 변경사항 커밋

### 가상환경 사용 권장
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 테스트 규칙

- **단위 테스트 작성**: `tests/` 폴더에 테스트 코드 작성
- **테스트 실행**: `pytest tests/`
- **커버리지 확인**: `pytest --cov=src tests/`

---

## 참고 사항

- **이슈 트래킹**: GitHub Issues 또는 Notion 사용
- **문서화**: 주요 기능은 README.md에 사용법 정리
- **코드 품질**: Black, isort, flake8 등 Linter 사용 권장

---

**마지막 업데이트**: 2026-04-17

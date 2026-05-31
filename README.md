# 영상 프레임 추출 & 바운딩 박스 어노테이션 파이프라인

> 객체 탐지 모델 학습용 데이터셋 구축을 위한 영상 처리 파이프라인

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=flat&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243?style=flat&logo=numpy&logoColor=white)

---

## 프로젝트 개요

항만 CCTV 영상을 분석하여 **컨테이너 객체 탐지 모델** 학습에 필요한 고품질 어노테이션 데이터셋을 구축하는 파이프라인입니다. 3인 팀이 협업하여 영상 프레임 추출부터 수작업 선별, 바운딩 박스 어노테이션까지 전 과정을 체계적으로 관리합니다.

### 핵심 문제 및 해결

| 문제 | 해결 방법 |
|------|----------|
| 수천 장의 프레임 중 유효 프레임 선별 필요 | 인터랙티브 프레임 선택 GUI 구현 (Y/N/B 키보드 제어) |
| 3명이 동시 작업 시 Git 충돌 발생 | 영상별 독립 폴더 구조로 충돌 원천 차단 |
| 프레임 파일 관리 및 추적 어려움 | 날짜/카메라각도/타임스탬프 기반 파일명 체계화 |

---

## 파이프라인 흐름

```
원본 영상 (MP4)
      │
      ▼
[1단계] 프레임 추출 (extract_frames.py)
      │  - 설정 가능한 추출 간격 (기본 5초)
      │  - 자동 파일명 생성: {날짜}_{카메라각도}_{타임스탬프}.jpg
      │
      ▼
[2단계] 프레임 선별 (select_frames.py)
      │  - OpenCV GUI로 프레임 시각적 검토
      │  - Y: 선택 / N: 스킵 / B: 이전으로 / Q: 종료
      │
      ▼
[3단계] 바운딩 박스 어노테이션
      │  - 선별된 프레임에 대해 어노테이션 작업
      │  - JSON/XML 형식으로 결과 저장
      │
      ▼
객체 탐지 모델 학습 데이터셋 완성
```

---

## 주요 기능

### 프레임 추출 (`extract_frames.py`)

- 영상 FPS를 기반으로 **정밀한 시간 간격 추출** (기본 5초, 조절 가능)
- 파일명에 카메라 각도와 영상 내 타임스탬프 자동 포함
- 추출 진행상황 실시간 출력

```bash
python3 src/extraction/extract_frames.py \
  --video data/video1/raw/101.mp4 \
  --output data/video1/frames \
  --record-time 20260420 \
  --interval 5
```

**출력 파일명 예시**: `20260420_101_02m30s.jpg`
- `20260420`: 녹화 날짜
- `101`: 카메라 각도 (영상 파일명에서 자동 추출)
- `02m30s`: 영상 내 타임스탬프

---

### 인터랙티브 프레임 선택기 (`select_frames.py`)

OpenCV GUI를 활용한 수작업 프레임 선별 도구입니다. 뒤로가기 기능을 통해 실수한 선택을 즉시 수정할 수 있습니다.

```bash
python3 src/extraction/select_frames.py \
  --input data/video1/frames \
  --output data/video1/selected
```

| 키 | 동작 |
|----|------|
| `Y` | 현재 프레임 선택 (selected 폴더에 복사) |
| `N` | 현재 프레임 스킵 |
| `B` | 이전 프레임으로 돌아가기 (선택 취소 가능) |
| `Q` | 선별 종료 |

---

## 프로젝트 구조

```
labeling_project/
├── src/
│   └── extraction/
│       ├── extract_frames.py   # 프레임 추출 스크립트
│       └── select_frames.py    # 인터랙티브 프레임 선택기
├── data/
│   ├── video1/                 # 영상별 독립 작업 공간
│   │   ├── raw/                # 원본 영상
│   │   ├── frames/             # 추출된 전체 프레임
│   │   ├── selected/           # 선별된 프레임
│   │   └── annotations/        # 바운딩 박스 어노테이션 결과
│   ├── video2/
│   ├── video3/
│   └── work_allocation.md      # 팀원별 작업 할당 현황
├── tests/
├── requirements.txt
└── README.md
```

---

## 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/applepc24/labeling_project.git
cd labeling_project

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt
```

---

## 기술 스택

| 분류 | 기술 |
|------|------|
| 언어 | Python 3.10+ |
| 영상 처리 | OpenCV 4.8+ |
| 이미지 처리 | Pillow, NumPy |
| 코드 품질 | Ruff (포맷팅 + 린팅), Mypy (타입 체크) |

---

## 팀 협업 전략

3인 팀이 동시에 작업할 때 Git 충돌을 방지하기 위해 **영상별 독립 폴더 구조**를 도입했습니다.

- 각 팀원은 서로 다른 `videoN/` 폴더에서 작업 → **파일 충돌 원천 차단**
- `data/work_allocation.md`로 작업 할당 현황을 팀 전체가 공유
- 어노테이션 결과(JSON)만 Git 추적, 원본 영상/프레임은 로컬 보관



**마지막 업데이트**: 2026-05-31

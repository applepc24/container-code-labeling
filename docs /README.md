# 영상 프레임 추출 & 바운딩 박스 어노테이션 프로젝트

> 영상에서 프레임을 추출하고 바운딩 박스 어노테이션을 진행하는 ML 데이터 구축 프로젝트

---

## 빠른 시작

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# # 패키지 설치(필수 아님!!!!)
# # 우리가 사용해야할 패키지가 정해지지않아서 걍 무시무시무시!!!
# pip install -r requirements.txt
# ```

### 2. 작업 방식

**각 팀원은 독립적인 영상 폴더에서 작업합니다**

1. `data/work_allocation.md` 열어서 본인이 담당할 영상 확인
2. 해당 영상 폴더(예: `data/video1/`)에서 작업 진행
3. 작업 완료 후 Git commit & push

---

## 폴더 구조

```
data/
├── video1/              # 영상1 작업 폴더
│   ├── raw/            # 원본 영상 넣는 곳
│   ├── frames/         # 프레임 추출 결과
│   └── annotations/    # 어노테이션 결과
├── video2/              # 영상2 작업 폴더
├── video3/              # 영상3 작업 폴더
└── work_allocation.md   # 작업 할당 현황
```

**핵심**: 각자 다른 `videoN/` 폴더에서 작업하므로 **Git 충돌 없음**

---

## 작업 흐름

### 1단계: 작업 할당 확인
```bash
# data/work_allocation.md 파일 열기
cat data/work_allocation.md
```

담당 영상 확인하고 본인 이름과 시작일 기록

### 2단계: 원본 영상 준비
```bash
# 공유 드라이브에서 영상 다운로드 후
# data/video1/raw/ 폴더에 복사
```

### 3단계: 프레임 추출
```bash
# src/extraction/ 폴더의 스크립트 사용
# (개발 예정)
```

### 4단계: 어노테이션 작업
- LabelMe 또는 다른 도구 사용
- 결과를 `data/videoN/annotations/` 폴더에 저장

### 5단계: 작업 완료 후
```bash
# 1. work_allocation.md 상태 업데이트
# 2. Git commit
git add data/video1/annotations/
git add data/work_allocation.md
git commit -m "feat: video1 어노테이션 완료"

# 3. Push
git push origin main
```

---

## Git 브랜치 전략

### 간단한 흐름
```
main → feature/작업명 → main
```

### 예시
```bash
# 1. main 브랜치에서 최신 코드 받기
git checkout main
git pull origin main

# 2. feature 브랜치 생성
git checkout -b feature/video1-annotation

# 3. 작업 진행 후 commit
git add data/video1/
git commit -m "feat: video1 어노테이션 50% 완료"

# 4. push
git push origin feature/video1-annotation

# 5. GitHub에서 Pull Request 생성
#    - GitHub 페이지 접속
#    - "Compare & pull request" 버튼 클릭
#    - PR 제목/내용 작성 후 "Create pull request"

# 6. 리뷰 후 Merge
#    - 팀원이 리뷰 완료하면 "Merge pull request" 클릭
#    - "Confirm merge" 클릭
#    - "Delete branch" 버튼 클릭 (GitHub에서 원격 브랜치 삭제)

# 7. 로컬에서 main 브랜치로 돌아가기
git checkout main

# 8. 최신 코드 받기 (merge된 내용 반영)
git pull origin main

# 9. 로컬 feature 브랜치 삭제 (선택사항)
git branch -d feature/video1-annotation
```

---

## 주의사항

### ✅ 해야 할 것
- 작업 시작 전 `data/work_allocation.md` 업데이트
- 본인 담당 영상 폴더에서만 작업
- 어노테이션 파일은 Git에 커밋 (JSON, XML 등)
- 주기적으로 commit & push (백업 목적)

### ❌ 하지 말아야 할 것
- 다른 사람의 영상 폴더 건드리기
- 원본 영상을 Git에 커밋 (.gitignore에 이미 제외됨)
- 프레임 이미지를 Git에 커밋 (용량 큼, 필요시 재생성)

---

## 파일 설명

| 파일 | 설명 |
|------|------|
| `CLAUDE.md` | Claude Code가 읽는 개발 가이드라인 (개발자용) |
| `README.md` | 이 파일, 프로젝트 사용 방법 (팀원용) |
| `requirements.txt` | Python 패키지 목록 |
| `.gitignore` | Git 제외 파일 (영상, 이미지, 모델 등) |
| `data/work_allocation.md` | 작업 할당 및 진행 현황 |

---

## 문제 발생 시

### Git 충돌이 발생했어요
→ 다른 팀원과 같은 영상 폴더를 동시에 작업했을 가능성
→ `data/work_allocation.md`에서 담당 영상 다시 확인

### 프레임 추출이 안 돼요
→ `src/extraction/` 폴더의 스크립트 확인 또는 팀원에게 문의

### 어노테이션 결과가 어디 있죠?
→ `data/videoN/annotations/` 폴더 확인

---

## 기술 스택

- **Python 3.10+**
- **OpenCV**: 영상 처리, 프레임 추출
- **LabelStudio/Supervision**: 바운딩 박스 어노테이션
- **PyTorch**: 추후 모델 학습용

---

## 팀원

| 이름 | 담당 영상 |
|------|----------|
| -    | -        |
| -    | -        |
| -    | -        |

**마지막 업데이트**: 2026-04-17

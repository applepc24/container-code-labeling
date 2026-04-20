import os
import shutil
import argparse

import cv2

# ========================================
# 실행 방법
# ========================================
# python3 select_frames.py \
#   --input ../../data/video1/frames \
#   --output ../../data/video1/selected
# ========================================
#
# 키보드 조작
# Y : 선택 (selected 폴더에 저장)
# N : 스킵
# Q : 종료


def select_frames(input_dir: str, output_dir: str):
    """
    추출된 프레임을 보면서 컨테이너 있는 것만 선택해서 저장합니다.

    Args:
        input_dir: 추출된 프레임 폴더 경로
        output_dir: 선택된 프레임 저장 폴더 경로
    """

    # 저장 폴더 없으면 자동 생성
    os.makedirs(output_dir, exist_ok=True)

    # jpg 파일 목록 가져오기(이름 순서대로 정렬)
    images = sorted([f for f in os.listdir(input_dir) if f.endswith(".jpg")])

    if not images:
        print("이미지가 없습니다.")
        return

    print(f"총 {len(images)}장 검토 시작")
    print("Y: 선택 | N: 스킵 | Q: 종료")
    print("-" * 40)

    selected_count = 0

    for idx, filename in enumerate(images):
        image_path = os.path.join(input_dir, filename)
        frame = cv2.imread(image_path)

        if frame is None:
            print(f"이미지를 읽을 수 없습니다: {filename}")
            continue

        # 이미지 위에 안내 텍스트 표시
        cv2.putText(
            frame,
            f"[{idx + 1}/{len(images)}] Y:선택  N:스킵  Q:종료  선택됨:{selected_count}장",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Frame Selector", frame)

        # 키보드 입력 대기 (키 누를 때까지 무한 대기)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("y"):
            save_path = os.path.join(output_dir, filename)
            shutil.copy(image_path, save_path)
            selected_count += 1
            print(f"✅ 선택: {filename} ({selected_count}장)")

        elif key == ord("n"):
            print(f"⏭️  스킵: {filename}")

        elif key == ord("q"):
            print("종료!")
            break

    cv2.destroyAllWindows()
    print("-" * 40)
    print(f"완료! {selected_count}장 선택됨 → {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="프레임 선택 도구")
    parser.add_argument("--input", type=str, required=True, help="프레임 폴더 경로")
    parser.add_argument(
        "--output", type=str, required=True, help="선택된 프레임 저장 폴더 경로"
    )
    args = parser.parse_args()

    select_frames(
        input_dir=args.input,
        output_dir=args.output,
    )

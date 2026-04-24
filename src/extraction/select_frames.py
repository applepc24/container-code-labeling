import argparse
import shutil
import os

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
# B : 뒤로가기 (이전 프레임으로 돌아가서 다시 선택)
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

    selected: dict[str, bool] = {}  # {filename: True/False} 선택 상태 기록
    idx = 0

    while 0 <= idx < len(images):
        filename = images[idx]
        image_path = os.path.join(input_dir, filename)
        frame = cv2.imread(image_path)

        if frame is None:
            print(f"이미지를 읽을 수 없습니다: {filename}")
            idx += 1
            continue

        # 현재 선택된 총 개수
        selected_count = sum(1 for v in selected.values() if v)

        # 이전 상태 표시 (cv2.putText는 한글 미지원이므로 영어로 표시)
        label_status = ""
        if filename in selected:
            label_status = " [Selected]" if selected[filename] else " [Skipped]"

        cv2.putText(
            frame,
            f"[{idx + 1}/{len(images)}] Y:Select N:Skip B:Back Q:Quit | {selected_count} selected{label_status}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Frame Selector", frame)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("y"):
            #이전에 선택 안 했으면 파일 복사
            save_path = os.path.join(output_dir, filename)
            if not os.path.exists(save_path):
                shutil.copy(image_path, save_path)
            selected[filename] = True
            print(f"✅ 선택: {filename}")
            idx += 1
        elif key == ord("n"):
            # 이전에 선택했었으면 파일 삭제
            save_path = os.path.join(output_dir, filename)
            if os.path.exists(save_path):
                os.remove(save_path)
            selected[filename] = False
            print(f"⏭️   스킵: {filename}")
            idx += 1
        
        elif key == ord("b"):
            if idx > 0:
                idx -= 1
                print(f"⏪ 뒤로: {images[idx]}")
            else:
                print("첫 번째 프레임입니다.")
        
        elif key == ord("q"):
            print("종료!")
            break

    cv2.destroyAllWindows()
    selected_count = sum(1 for v in selected.values() if v)
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

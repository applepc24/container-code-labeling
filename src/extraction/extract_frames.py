import argparse
import os
from pathlib import Path

import cv2

  # ========================================                                                    
  # 실행 방법                                                                                 
  # ========================================
  # 기본 실행 (5초마다 1장)
  # python3 extract_frames.py \                                                                 
  #   --video ../../data/video1/raw/101.mp4 \
  #   --output ../../data/video1/frames \                                                       
  #   --record-time 20260420                                                                    
  #
  # 간격 조절 (2초마다 1장)                                                                     
  # python3 extract_frames.py \                                                               
  #   --video ../../data/video1/raw/101.mp4 \
  #   --output ../../data/video1/frames \                                                       
  #   --record-time 20260420 \
  #   --interval 2                                                                              
  #                                                                                           
  # 저장 파일명 형식: {record-time}_{카메라각도}_{영상시각}.jpg
  # 예시: 20260420_101_02m30s.jpg                                                               
  # ========================================


def extract_frames(video_path: str, output_dir: str, record_time: str, interval_sec: float = 5.0):
    """
    영상에서 일정 간격으로 프레임을 추출해서 저장합니다.

    Args:
        video_path: 영상 파일 경로
        output_dir: 저장할 폴더 경로
        record_time: 녹화 날짜 (폴더명, 예: 20260420)
        interval_sec: 몇 초마다 1장 추출할지 (기본값: 5초)
    """

    # 저장 폴더 없으면 자동 생성
    os.makedirs(output_dir, exist_ok=True)

    # 카메라 각도 : 영상 파일명에서 추출 (101.mp4 -> 101)
    camera_angle = Path(video_path).stem

    # 영상 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"영상을 열 수 없습니다: {video_path}")
        return

    # 영상 정보
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 몇 프레임마다 저장할지 계산
    frame_interval = max(1, int(fps * interval_sec))

    print(f"FPS: {fps}")
    print(f"총 프레임: {total_frames}")
    print(f"영상 길이: {total_frames / fps:.1f}초")
    print(f"{interval_sec}초마다 추출 = {frame_interval}프레임마다 1장")
    print(f"예상 추출 장수: {total_frames // frame_interval}장")
    print("-" * 40)

    frame_idx = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_idx % frame_interval == 0:
            # 영상 시각 계산 (프레임 -> 분, 초)
            total_sec = int(frame_idx / fps)
            minutes = total_sec // 60
            seconds = total_sec % 60
            timestamp = f"{minutes:02d}m{seconds:02d}s"
            
            filename = f"{record_time}_{camera_angle}_{timestamp}.jpg"                        
            save_path = os.path.join(output_dir, filename)
            cv2.imwrite(save_path, frame)                                                     
            saved_count += 1                                                                
            print(f"저장: {filename} ({saved_count}장)")  

        frame_idx += 1

    cap.release()
    print("-" * 40)
    print(f"완료! 총 {saved_count}장 저장됨 → {output_dir}/")


if __name__ == "__main__":                                                                    
      parser = argparse.ArgumentParser(description="영상에서 프레임 추출")                    
      parser.add_argument("--video", type=str, required=True, help="영상 파일 경로")            
      parser.add_argument("--output", type=str, required=True, help="저장할 폴더 경로")
      parser.add_argument(                                                                      
          "--record-time", type=str, required=True, help="녹화 날짜 (폴더명, 예: 20260420)"   
      )                                                                                         
      parser.add_argument(                                                                    
          "--interval", type=float, default=5.0, help="추출 간격(초), 기본값: 5.0"              
      )                                                                                       
      args = parser.parse_args()

      extract_frames(                                                                           
          video_path=args.video,
          output_dir=args.output,                                                               
          record_time=args.record_time,                                                       
          interval_sec=args.interval,
      )

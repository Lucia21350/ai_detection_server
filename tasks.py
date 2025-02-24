from celery import Celery
import os
import json
import requests
import time
from config import STATIC_FOLDER, CALLBACK_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from utils import save_image, load_image, draw_detections, run_detection

# Celery 인스턴스 생성
celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task
def process_image(photo_uid, image_data, start_time):
    print(f"Task received at: {start_time}")
    
    # 이미지 저장 및 로드
    filepath, filename = save_image(image_data)
    image = load_image(filepath)

    # 객체 탐지
    detections = run_detection(image)

    # 탐지 결과 이미지 생성
    output_image = draw_detections(image, detections)
    output_path = os.path.join(STATIC_FOLDER, filename)
    output_image.save(output_path)

    # 탐지 결과 정리
    results = [{"startX": det["bbox"][0], "startY": det["bbox"][1], 
                "endX": det["bbox"][2], "endY": det["bbox"][3]} for det in detections]

    response_data = {
        "photoUid": photo_uid,
        "cariesCount": len(results),
        "positions": results
    }

    # 이미지 파일 전송
    try:
        with open(output_path, "rb") as image_file:
            files = {"files": (filename, image_file, "image/png")}
            data = {"photoUid": photo_uid, "cariesCount": len(results), "positions": json.dumps(results)}
            response = requests.post(CALLBACK_URL, data=data, files=files, timeout=5)
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error sending results: {e}")
    
    end_time = time.time()  # 결과 전송 완료 시간 기록
    print(f"Task completed at: {end_time}")
    print(f"Total processing time: {end_time - start_time} seconds")

    return response_data

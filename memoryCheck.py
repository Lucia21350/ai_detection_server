import requests
import multiprocessing
import time

API_URL = "http://localhost:5000/detect"
IMAGE_PATH = "C:/Users/ljh86/Documents/ai_detection_server/uploads/1.jpg"
NUM_REQUESTS = 50  # 동시에 보낼 요청 개수

# API 호출 함수
def send_request(i, results):
    start_time = time.time()
    with open(IMAGE_PATH, "rb") as img:
        files = {"image": img}
        data = {"photoUid": f"test_{i}"}
        try:
            response = requests.post(API_URL, files=files, data=data, timeout=10)  # 타임아웃 설정
            end_time = time.time()
            results[i] = (response.status_code, end_time - start_time)
            print(f"[{i}] Status Code: {response.status_code}, Time Taken: {results[i][1]:.2f} sec")
        except requests.exceptions.RequestException as e:
            results[i] = (None, None)
            print(f"[{i}] Request Failed: {e}")

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    results = manager.dict()
    
    start_time = time.time()
    
    processes = []
    for i in range(NUM_REQUESTS):
        p = multiprocessing.Process(target=send_request, args=(i, results))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time()

    print("\n--- Individual Task Processing Times ---")
    for i in range(NUM_REQUESTS):
        if results[i][0] is not None:
            print(f"Task {i}: Status {results[i][0]}, {results[i][1]:.2f} sec")
        else:
            print(f"Task {i}: Failed")

    print(f"\nTotal Execution Time: {end_time - start_time:.2f} sec")

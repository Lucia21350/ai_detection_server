MODEL_PATH = "model/11n_train7_best.pt"
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"
ALLOWED_EXTENSIONS = {"jpg", "png"}

# Celery 설정
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CALLBACK_URL = "https://eofmqrcm45aaw8s.m.pipedream.net" #"http://4.230.16.220:8081/ai/advance-diagnosis" # 테스트 서버: "https://eofmqrcm45aaw8s.m.pipedream.net" "http://192.168.0.125:8080/ai/advance-diagnosis"

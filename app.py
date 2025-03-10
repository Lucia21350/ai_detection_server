from flask import Flask, request, jsonify, send_file
import os
from config import UPLOAD_FOLDER, STATIC_FOLDER
from utils import save_image
import time
from tasks import process_image

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask 서버 실행 중!"

@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files or "photoUid" not in request.form:
        return jsonify({"error": "Image and photoUid are required"}), 400

    file = request.files["image"]
    photo_uid = request.form["photoUid"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    start_time = time.time()  # 요청을 받은 시점 기록
    process_image.delay(photo_uid, file.read(), start_time)

    return jsonify({"message": "Processing started", "photoUid": photo_uid})


@app.route("/result/<filename>")
def result(filename):
    return send_file(os.path.join(STATIC_FOLDER, filename), mimetype="image/png")

@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(STATIC_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)

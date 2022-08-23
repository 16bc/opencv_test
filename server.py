# Первая самая простая и сырая версия. Рассинхрон потока и перегрузка, но работает.

from flask import Response
from flask import Flask
from flask import render_template
import time
from videosource import VideoSource

VIDEO_URL = "https://cams.is74.ru/live/main/cam19385.m3u8"

app = Flask(__name__)
vs = VideoSource(VIDEO_URL)
time.sleep(2)


def get_stream():
	while True:
		if not vs.status:
			continue
		yield vs.encoded_frame
		time.sleep(1 / 30)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/video")
def video():
	return Response(get_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
	app.run(debug=True, threaded=True, use_reloader=False)

from flask import Response
from flask import Flask
from flask import render_template
import time
from videosource import VideoSource


VIDEO_URL = "https://cams.is74.ru/live/main/cam19385.m3u8"
TRAFICK_LIGHT_COORDS = [520, 529, 634, 641]

vs = VideoSource(video_url=VIDEO_URL, tl=TRAFICK_LIGHT_COORDS)
time.sleep(2)
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/video")
def video():
	return Response(vs.get_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
	app.run(debug=True)

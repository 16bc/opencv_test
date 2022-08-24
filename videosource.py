
import cv2
import time
from threading import Thread


class VideoSource:
    def __init__(self, video_url: str):
        self.fps = 30
        self.period = 1/self.fps
        self.output_frame = None
        self.cap = None
        self.traficLight_value = ''
        self.status = False
        self.frame = None
        while True:
            # self.cap = cv2.VideoCapture(video_url, cv2.CAP_FFMPEG, [cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY ])
            self.cap = cv2.VideoCapture(video_url)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
            if not self.cap.isOpened():
                print('!!! Unable to open URL')
                time.sleep(5)
                continue
            break

        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.process = Thread(target=self._process_frame, args=())
        self.process.daemon = True
        self.process.start()

    def _process_frame(self):
        every_second_frame = True  # Флаг каждого второго кадра для обработки
        while True:
            start_time = time.time()
            if self.cap.isOpened():
                _status, _raw_frame = self.cap.read()
                if not _status:
                    continue
                _raw_frame = cv2.resize(_raw_frame, (1280, 800))

                # Определяем цвет светофора каждый второй кадр для снижения нагрузки
                if every_second_frame:
                    traficLight_frame = _raw_frame[521:531, 634:644]
                    traficLight = cv2.resize(traficLight_frame, (1, 1))
                    self.traficLight_value = 'Красный' if traficLight[0, 0][2] > 150 else 'Зеленый'
                cv2.rectangle(_raw_frame, (90, 40), (420, 120),
                              (0,0,0), -1)
                cv2.putText(_raw_frame, self.traficLight_value, (100, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255))
                self.frame = _raw_frame
                self.status = _status
                self._encode_image()
                every_second_frame = not every_second_frame
                dt = time.time() - start_time
                if self.period - dt > 0:
                    time.sleep(self.period - dt)

    def _encode_image(self):
        _, encodedImage = cv2.imencode(".jpg", self.frame)
        self.encoded_frame = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'

    def show_frame(self):
        while True:
            if self.status:
                cv2.imshow('frame', self.frame)
            cv2.waitKey(int(1000 / self.fps))

    def get_stream(self):
        while True:
            if not self.status:
                continue
            yield self.encoded_frame
            time.sleep(1 / self.fps)


if __name__ == '__main__':
    video_url = "https://cams.is74.ru/live/main/cam19385.m3u8"
    vs = VideoSource(video_url)
    vs.show_frame()








from threading import Thread
import cv2


class WebcamThread:
    def __init__(self, source=0):
        self.__capture = cv2.VideoCapture(source)
        self.__thread = Thread(target=self.update, args=())
        self.__thread.daemon = True
        self.__status = False
        self.__frame = None
        _, temp_frame = self.__capture.read()
        self.__height = temp_frame.shape[0]
        width = temp_frame.shape[1]
        self.__top_left_x = (width - self.__height) // 2
        self.__top_left_y = 0

    def start(self):
        self.__thread.start()

    def update(self):
        while True:
            if self.__capture.isOpened():
                (self.__status, self.__frame) = self.__capture.read()

    def grab_frame(self):
        if self.__status:
            return self.__frame
        return None

    @property
    def top_left_x(self):
        return self.__top_left_x

    @property
    def top_left_y(self):
        return self.__top_left_y

    @property
    def square_side_length(self):
        return self.__height

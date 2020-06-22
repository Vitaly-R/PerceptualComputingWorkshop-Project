from Parameters import RIGHT, LEFT
import os
import sys
try:
    cwd = os.getcwd()
    openpose_python_dir = os.path.join(cwd, "openpose", "python", "openpose", "Release")
    openpose_bin_dir = os.path.join(cwd, "openpose", "bin")
    sys.path.append(openpose_python_dir)
    os.environ['PATH'] = os.environ['PATH'] + ';' + openpose_bin_dir + ";"
    import pyopenpose as op
except ImportError as e:
    print("Failed to initialize openpose \n" + str(e), file=sys.stderr)
    op = None


class HandDetector:

    def __init__(self, webcamObject, hand=RIGHT):
        self.__online = op is not None
        if self.__online:
            self.__hand = RIGHT if hand else LEFT
            self.__top_left_x = webcamObject.top_left_x
            self.__top_left_y = webcamObject.top_left_y
            self.__side_length = webcamObject.square_side_length
            params = dict()
            params["model_folder"] = os.path.join(cwd, "openpose", "models")
            params["hand"] = True
            params["hand_detector"] = 2
            params["body"] = 0
            self.__opWrapper = op.WrapperPython()
            self.__opWrapper.configure(params)
            self.__opWrapper.start()
            self.__datum = op.Datum()
            if self.__hand:
                self.__datum.handRectangles = [[op.Rectangle(0, 0, 0, 0),
                                                op.Rectangle(self.__top_left_x, self.__top_left_y, self.__side_length, self.__side_length)]]
            else:
                self.__datum.handRectangles = [[op.Rectangle(self.__top_left_x, self.__top_left_y, self.__side_length, self.__side_length),
                                                op.Rectangle(0, 0, 0, 0)]]

    def detect(self, image):
        if self.__online:
            self.__datum.cvInputData = image
            self.__opWrapper.emplaceAndPop([self.__datum])
            return self.__datum.handKeypoints[self.__hand][0]

    def set_hand(self, hand):
        if self.__online:
            self.__hand = RIGHT if hand else LEFT
            if self.__hand:
                self.__datum.handRectangles = [[op.Rectangle(0, 0, 0, 0),
                                                op.Rectangle(self.__top_left_x, self.__top_left_y, self.__side_length, self.__side_length)]]
            else:
                self.__datum.handRectangles = [[op.Rectangle(self.__top_left_x, self.__top_left_y, self.__side_length, self.__side_length),
                                                op.Rectangle(0, 0, 0, 0)]]

import numpy as np
from Parameters import RIGHT, LEFT


class GestureEngine:

    NO_GESTURE = 0
    OPEN_HAND = 1
    METAL = 2

    __WRIST = 0
    __PALM = [1, 5, 9, 13, 17]
    __THUMB = [1, 2, 3, 4]
    __INDEX = [5, 6, 7, 8]
    __MIDDLE = [9, 10, 11, 12]
    __RING = [13, 14, 15, 16]
    __PINKIE = [17, 18, 19, 20]
    __FINGERS = [__THUMB, __INDEX, __MIDDLE, __RING, __PINKIE]
    __KEYPOINTS = 21
    __METAL_GESTURE = [False, True, False, False, True]
    THRESHOLD = 0.3

    def __init__(self, hand=RIGHT):
        self.__gesture_memory = None
        self.__x_s = np.zeros((self.__KEYPOINTS, ))
        self.__y_s = np.zeros((self.__KEYPOINTS, ))
        self.__c_s = np.zeros((self.__KEYPOINTS,))
        self.__hand_on_screen = False
        self.__hand = RIGHT if hand == RIGHT else LEFT
        self.__open_fingers = {finger[0]: False for finger in self.__FINGERS}

    def analyze(self, handKeypoints):
        self.__x_s = handKeypoints[:, 0]
        self.__y_s = handKeypoints[:, 1]
        self.__c_s = handKeypoints[:, 2]
        if self.THRESHOLD < self.__c_s[self.__WRIST]:
            gesture = self.__determine_gesture()
            cx, cy = self.__calculate_center()
            dx, dy = self.__calculate_diff(cx, cy)
            gesture_tuple = (gesture, cx, cy, dx, dy)
        else:
            gesture_tuple = (self.NO_GESTURE, -1, -1, 0, 0)
        self.__gesture_memory = (gesture_tuple[1], gesture_tuple[2])
        return gesture_tuple

    def __determine_gesture(self):
        self.__check_open_fingers()
        open_fingers = list(self.__open_fingers.values())
        if False not in open_fingers:
            return self.OPEN_HAND
        if open_fingers == self.__METAL_GESTURE:
            return self.METAL
        return self.NO_GESTURE

    def __check_open_fingers(self):
        if self.__hand == LEFT:
            self.__open_fingers[self.__THUMB[0]] = (self.__x_s[self.__THUMB[-1]] < self.__x_s[self.__THUMB[0]])
        else:
            self.__open_fingers[self.__THUMB[0]] = (self.__x_s[self.__THUMB[0]] < self.__x_s[self.__THUMB[-1]])
        for finger in self.__FINGERS[1:]:
            self.__open_fingers[finger[0]] = (50 <= (self.__y_s[finger[0]] - self.__y_s[finger[-1]]))

    def __calculate_center(self):
        cx = 0
        cy = 0
        for finger in self.__FINGERS:
            cx += self.__x_s[finger[0]]
            cy += self.__y_s[finger[0]]
        cx //= len(self.__FINGERS)
        cy //= len(self.__FINGERS)
        return int(cx), int(cy)

    def __calculate_diff(self, cx, cy):
        dx = 0
        dy = 0
        if self.__gesture_memory is not None:
            prev_cx, prev_cy = self.__gesture_memory
            if 0 <= prev_cx and 0 <= prev_cy:
                dx = prev_cx - cx
                dy = cy - prev_cy
        return dx, dy

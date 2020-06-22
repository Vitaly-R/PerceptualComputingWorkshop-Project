from WebcamReader import WebcamThread
from HandDetector import HandDetector
from GestureEngine import GestureEngine
from Parameters import RIGHT
import cv2

gesture_dict = {GestureEngine.NO_GESTURE: "no gesture",
                GestureEngine.OPEN_HAND: "open hand",
                GestureEngine.METAL: "metal"}

hand = RIGHT
capture = WebcamThread()
hand_detector = HandDetector(capture, hand)
gesture_engine = GestureEngine(hand)

capture.start()

while True:
    frame = capture.grab_frame()
    if frame is not None:
        cv2.rectangle(frame, (capture.top_left_x, capture.top_left_y),
                      (capture.top_left_x + capture.square_side_length, capture.top_left_y + capture.square_side_length),
                      (0, 255, 0), 4)
        keypoints = hand_detector.detect(frame)
        gesture, cx, cy, dx, dy = gesture_engine.analyze(keypoints)
        i = 0
        for x, y, c in keypoints:
            if i == 0:
                cv2.circle(frame, (x, y), 4, (255, 255, 255), -1)
            elif i in [1, 5, 9, 13, 17]:
                cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
            else:
                cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
            i += 1
        cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)
        cv2.imshow("", frame)
        print(gesture_dict[gesture])
    if cv2.waitKey(10) == ord('q'):
        break

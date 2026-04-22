import cv2
import mediapipe as mp
import math
import numpy as np
import time
import pygame

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ---------------- MUSIC SETUP ----------------
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")  # put your file in same folder
pygame.mixer.music.play(-1)  # loop music forever

# ---------------- VOLUME SETUP ----------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol = volume.GetVolumeRange()[:2]

# ---------------- MEDIAPIPE SETUP ----------------
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpDraw = mp.solutions.drawing_utils

# ---------------- WEBCAM ----------------
cap = cv2.VideoCapture(0)
cap.set(10, 100)

# ---------------- FPS ----------------
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            if len(lmList) != 0:
                # Thumb (4) & Index (8)
                x1, y1 = lmList[4]
                x2, y2 = lmList[8]

                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                length = math.hypot(x2 - x1, y2 - y1)

                # ---------------- MUTE FIX ----------------
                if length < 25:
                    volume.SetMasterVolumeLevel(minVol, None)

                    # Also mute music
                    pygame.mixer.music.set_volume(0)

                    cv2.putText(img, "MUTED", (200, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                else:
                    # Volume control
                    vol = np.interp(length, [30, 200], [minVol, maxVol])
                    volume.SetMasterVolumeLevel(vol, None)

                    # Control music volume (0.0 to 1.0)
                    volPer = np.interp(length, [30, 200], [0, 100])
                    pygame.mixer.music.set_volume(volPer / 100)

                # ---------------- VOLUME BAR ----------------
                volBar = np.interp(length, [30, 200], [400, 150])
                volPer = np.interp(length, [30, 200], [0, 100])

                cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

                cv2.putText(img, f'{int(volPer)} %', (40, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # ---------------- FPS ----------------
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # ---------------- TITLE ----------------
    cv2.putText(img, "Hand Gesture Volume + Music Control", (80, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Hand Volume Control", img)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
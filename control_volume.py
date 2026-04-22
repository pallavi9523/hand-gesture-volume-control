import cv2
import mediapipe as mp
import math
import numpy as np
import time
import pygame

# ---------------- MUSIC SETUP ----------------
pygame.mixer.init()

songs = ["song1.mp3", "song2.mp3", "song3.mp3"]  # add your songs
current_song = 0

pygame.mixer.music.load(songs[current_song])
pygame.mixer.music.play(-1)

# ---------------- MEDIAPIPE SETUP ----------------
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1, 0.7, 0.7)
mpDraw = mp.solutions.drawing_utils

# ---------------- WEBCAM ----------------
cap = cv2.VideoCapture(0)

# ---------------- VARIABLES ----------------
pTime = 0
gesture_delay = 0
delay_time = 1
is_playing = True

# ---------------- FUNCTION ----------------
def count_fingers(lmList):
    fingers = []

    # Thumb
    if lmList[4][0] > lmList[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8, 12, 16, 20]
    for tip in tips:
        if lmList[tip][1] < lmList[tip - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# ---------------- MAIN LOOP ----------------
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmList) != 0:
        # ---------------- FINGER COUNT ----------------
        finger_count = count_fingers(lmList)
        current_time = time.time()

        # ---------------- PLAY / PAUSE ----------------
        if finger_count == 0 and is_playing:
            pygame.mixer.music.pause()
            is_playing = False

        elif finger_count == 5 and not is_playing:
            pygame.mixer.music.unpause()
            is_playing = True

        # ---------------- NEXT SONG ----------------
        elif finger_count == 3 and current_time - gesture_delay > delay_time:
            current_song = (current_song + 1) % len(songs)
            pygame.mixer.music.load(songs[current_song])
            pygame.mixer.music.play(-1)
            gesture_delay = current_time

        # ---------------- PREVIOUS SONG ----------------
        elif finger_count == 4 and current_time - gesture_delay > delay_time:
            current_song = (current_song - 1) % len(songs)
            pygame.mixer.music.load(songs[current_song])
            pygame.mixer.music.play(-1)
            gesture_delay = current_time

        # ---------------- VOLUME CONTROL ----------------
        x1, y1 = lmList[4]
        x2, y2 = lmList[8]

        length = math.hypot(x2 - x1, y2 - y1)

        volPer = np.interp(length, [30, 200], [0, 100])
        pygame.mixer.music.set_volume(volPer / 100)

        # ---------------- MUTE ----------------
        if length < 25:
            pygame.mixer.music.set_volume(0)
            cv2.putText(img, "MUTED", (200, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        # ---------------- UI ----------------
        volBar = np.interp(length, [30, 200], [400, 150])

        cv2.rectangle(img, (50, 150), (85, 400), (0,255,0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0,255,0), cv2.FILLED)

        cv2.putText(img, f'{int(volPer)} %', (40, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

        # ---------------- STATUS ----------------
        status = "Playing" if is_playing else "Paused"
        cv2.putText(img, status, (350, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        cv2.putText(img, f"Song: {songs[current_song]}", (300, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # ---------------- FPS ----------------
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.putText(img, "Gesture Music Controller", (100, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.imshow("AI Music Controller", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
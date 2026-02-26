import cv2
import mediapipe as mp
import numpy as np
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Get default speakers
devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, c = img.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Thumb tip (4) and Index tip (8)
            x1 = int(hand_landmarks.landmark[4].x * w)
            y1 = int(hand_landmarks.landmark[4].y * h)
            x2 = int(hand_landmarks.landmark[8].x * w)
            y2 = int(hand_landmarks.landmark[8].y * h)

            # Draw circles
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), -1)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), -1)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Calculate distance
            length = math.hypot(x2 - x1, y2 - y1)

            # Convert distance to volume range
            vol = np.interp(length, [30, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Hand Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

h, w, c = frame.shape

print("Camera Resolution:", w, "x", h)

cap.release()
import cv2
import numpy as np
import pyttsx3
import time
import speech_recognition as sr
import threading
from color_logic import get_color_name  #  Import shared function

# Initialize pyttsx3 for voice output
engine = pyttsx3.init()
exit_flag = False

def listen_for_exit():
    global exit_flag
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while not exit_flag:
        try:
            with mic as source:
                print("Listening for 'exit' command...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                command = recognizer.recognize_google(audio).lower()
                if "exit" in command:
                    print("Exit command detected by voice.")
                    exit_flag = True
                    break
        except Exception:
            continue

# Start exit listener
threading.Thread(target=listen_for_exit, daemon=True).start()

# Start webcam
cap = cv2.VideoCapture(0)
prev_color = None
last_spoken_time = 0
speak_interval = 2

while True:
    if exit_flag:
        print("Exiting due to voice command...")
        break

    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    cx, cy = width // 2, height // 2
    size = 25
    center_region = frame[cy - size:cy + size, cx - size:cx + size]

    avg_color = np.average(np.average(center_region, axis=0), axis=0)
    b, g, r = [int(c) for c in avg_color]

    color_name = get_color_name(r, g, b)

    cv2.rectangle(frame, (cx - size, cy - size), (cx + size, cy + size), (0, 255, 0), 2)
    cv2.putText(frame, f"{color_name}", (cx - size, cy - size - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    current_time = time.time()
    if color_name != prev_color and (current_time - last_spoken_time) > speak_interval:
        engine.say(f"The color is {color_name}")
        engine.runAndWait()
        prev_color = color_name
        last_spoken_time = current_time

    cv2.imshow("Auto Color Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

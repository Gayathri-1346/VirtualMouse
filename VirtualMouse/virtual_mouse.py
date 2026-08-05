import sys
sys.modules['tensorflow'] = None

import google.protobuf.message_factory as message_factory
if not hasattr(message_factory.MessageFactory, 'GetPrototype'):
    def get_prototype(self, descriptor):
        return self.GetMessageClass(descriptor)
    message_factory.MessageFactory.GetPrototype = get_prototype

import cv2
import numpy as np
import pyautogui
import math
from cvzone.HandTrackingModule import HandDetector
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import time

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.85, maxHands=2)

cam_w, cam_h = 640, 480
cap.set(3, cam_w)
cap.set(4, cam_h)

if not cap.isOpened():
    print("Error: Could not open webcam. Please check if your camera is connected and not in use by another application.")
    exit()

screen_w, screen_h = pyautogui.size()

box_w, box_h = 500, 300
box_x = (cam_w - box_w) // 2
box_y = (cam_h - box_h) // 2


try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))
except Exception as e:
    print("Audio device initialization failed (could be due to no audio endpoints):", e)
    volume_control = None


left_clicked = False
right_clicked = False


prev_x, prev_y = 0, 0
smoothing = 4  


last_volume = -1
last_brightness = -1
last_volume_time = 0
last_brightness_time = 0

def get_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

while True:
    success, img = cap.read()
    if not success:
        print("Warning: Failed to grab frame. Retrying...")
        time.sleep(0.1)  # Sleep briefly to prevent 100% CPU usage if camera fails
        continue

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    cv2.rectangle(img, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 255, 0), 2)
    cv2.putText(img, "Gesture Box", (box_x, box_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            fingers = detector.fingersUp(hand)
            hand_type = hand["type"]

            if hand_type == "Left":
                # Left Hand: Controls Brightness
                # Gesture: Pinky finger is UP
                if fingers[4] == 1:
                    brightness_dist = get_distance(lmList[4], lmList[8])
                    brightness_level = int(np.interp(brightness_dist, [30, 180], [0, 100]))
                    
                    current_time = time.time()
                    if abs(brightness_level - last_brightness) >= 4 and (current_time - last_brightness_time) > 0.15:
                        try:
                            sbc.set_brightness(brightness_level)
                            last_brightness = brightness_level
                            last_brightness_time = current_time
                        except Exception as e:
                            print("Brightness control error:", e)
                    
                    display_val = last_brightness if last_brightness != -1 else brightness_level
                    cv2.putText(img, f"Brightness: {display_val}%", (50, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 2)
            
            elif hand_type == "Right":
                # Right Hand: Controls Mouse Operations and Volume
                # Volume Control Gesture: Pinky is UP, Middle is DOWN 
                if fingers[4] == 1 and fingers[2] == 0:
                    volume_dist = get_distance(lmList[4], lmList[8])
                    volume_level = np.interp(volume_dist, [30, 180], [0.0, 1.0])
                    
                    current_time = time.time()
                    if abs(volume_level - last_volume) >= 0.03 and (current_time - last_volume_time) > 0.05:
                        try:
                            if volume_control is not None:
                                volume_control.SetMasterVolumeLevelScalar(volume_level, None)
                            last_volume = volume_level
                            last_volume_time = current_time
                        except Exception as e:
                            print("Volume control error:", e)
                    
                    display_val = last_volume if last_volume != -1 else volume_level
                    cv2.putText(img, f"Volume: {int(display_val * 100)}%", (50, 260),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2)
                
                else:
                    # Mouse Operations (Move, Click, Scroll)
                    ind_x, ind_y = lmList[8][:2]
                    mid_x, mid_y = lmList[12][:2]
                    
                  
                    ind_mid_dist = get_distance(lmList[8], lmList[12])

                    # 1. Raise index, middle, thumb fingers to pause the cursor
                    if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                        cv2.putText(img, "Cursor Paused", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        prev_x, prev_y = 0, 0

                    # 2. Use index, middle, thumb, little fingers together to scroll down 
                    elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
                        pyautogui.scroll(-40)
                        cv2.putText(img, "Scroll Down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                        prev_x, prev_y = 0, 0

                    # 3. Raise index and middle fingers to move the cursor or scroll up
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                        # Spread apart -> Move cursor (thumb should be down to distinguish from pause)
                        if fingers[0] == 0 and ind_mid_dist >= 35:
                            if box_x <= ind_x <= box_x + box_w and box_y <= ind_y <= box_y + box_h:
                                
                                screen_x = np.interp(ind_x, [box_x, box_x + box_w], [0, screen_w])
                                screen_y = np.interp(ind_y, [box_y, box_y + box_h], [0, screen_h])
                                
                                
                                if prev_x == 0 and prev_y == 0:
                                    curr_x, curr_y = screen_x, screen_y
                                else:
                                    curr_x = prev_x + (screen_x - prev_x) / smoothing
                                    curr_y = prev_y + (screen_y - prev_y) / smoothing
                                
                                pyautogui.moveTo(int(curr_x), int(curr_y))
                                prev_x, prev_y = curr_x, curr_y
                                cv2.putText(img, "Moving Cursor", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        
                        # Close together -> Scroll UP
                        elif fingers[0] == 0 and ind_mid_dist < 35:
                            pyautogui.scroll(40)
                            cv2.putText(img, "Scroll Up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            prev_x, prev_y = 0, 0

                    # 4. Left Click: Bend the index finger (middle is up)
                    if fingers[1] == 0 and fingers[2] == 1 and lmList[8][1] > lmList[6][1]:
                        if not left_clicked:
                            pyautogui.click()
                            left_clicked = True
                        cv2.putText(img, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        left_clicked = False

                    # 5. Right Click: Bend the middle finger (index is up)
                    if fingers[1] == 1 and fingers[2] == 0 and lmList[12][1] > lmList[10][1]:
                        if not right_clicked:
                            pyautogui.rightClick()
                            right_clicked = True
                        cv2.putText(img, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    else:
                        right_clicked = False

                    # Reset cursor movement history if fingers are not in cursor moving state
                    if not (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and ind_mid_dist >= 35):
                        prev_x, prev_y = 0, 0

    cv2.imshow("Virtual Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

                                **** VIRTUAL MOUSE USING HAND GESTURES ****


ABSTRACT:
The Virtual Mouse is a computer vision-based system built using Python, OpenCV, Mediapipe, and CVZone.
It enables users to control the mouse cursor using hand gestures detected via a webcam.
The system replaces traditional input devices with a touchless, intuitive, and hygienic control mechanism.
Users can move the cursor, perform left and right clicks, scroll, and adjust brightness and volume using simple hand movements.
This project aims to improve accessibility, hygiene, and interactivity in computing through artificial intelligence and real-time hand tracking.

--------------------------------------------------------------------------------------------

FEATURES:
✅ Real-Time Hand Tracking – Detects hand gestures using webcam and computer vision.

✅ Touchless Cursor Control – Move the cursor using index, middle, and thumb finger positions.

✅ Mouse Operations – Perform left and right clicks using specific finger gestures.
✅ Scrolling – Scroll up and down using multiple finger combinations.
✅ Volume and Brightness Control – Adjust system audio and display brightness using two-hand gestures.
✅ User-Friendly Interface – Live visual feedback through on-screen gesture box.
✅ Accessible and Hygienic – Ideal for touch-free environments and physically impaired users.

--------------------------------------------------------------------------------------------

PROJECT STRUCTURE:
Virtual-Mouse/
|
|---- virtual_mouse.py   ->  main logic   
|
|___ requirements.txt         -> Python dependencies
|
|___ README.txt               -> Project documentation
|
|___ demo_video.mp4           -> Demonstration file 

--------------------------------------------------------------------------------------------

QUICK START:

PREREQUISITES:
- Python 3.8 or above
- Webcam
- Git (optional, for cloning the project)

STEP 1: Clone or Download the Project
Option 1: Using Git
    git clone <repository-url>
Option 2: Download the ZIP file and extract it

STEP 2: Install Dependencies
    pip install -r requirements.txt

Required Libraries:
opencv-python, mediapipe, cvzone, pyautogui, numpy, pycaw, screen-brightness-control, comtypes

STEP 3: Run the Application
    python virtual_mouse.py

Press 'q' to exit the application.

--------------------------------------------------------------------------------------------

HOW TO USE:
1. Keep your hand in front of the webcam.
2. Raise  index and middle fingers to move the cursor.
3. Raise index, middle, thumb fingers to pause the cursor
3. Bend the index finger for a left click.
4. Bend the middle finger for a right click.
5. Use index and middle fingers together to scroll up 
6. Use index, middle, thumb, little fingers together to scroll down.
6. Use left hand to control brightness and right hand to control volume.
7. Press 'q' to quit the application.

--------------------------------------------------------------------------------------------

TECHNICAL DETAILS:

LIBRARIES AND MODULES:
- OpenCV: For video capture and image processing.
- CVZone and Mediapipe: For real-time hand landmark detection and gesture recognition.
- PyAutoGUI: For automating mouse movement and clicks.
- PyCaw: For audio volume control via Windows API.
- Screen Brightness Control: For adjusting system brightness.
- NumPy, Math, Comtypes: For computations and system-level functions.

OPERATING SYSTEM: Windows
PROGRAMMING LANGUAGE: Python 3.8+

--------------------------------------------------------------------------------------------

TROUBLESHOOTING:

ISSUE: Cursor lag or delay
CAUSE: Low system performance or poor lighting.
SOLUTION: Improve lighting or close background applications.

ISSUE: Click not detected
CAUSE: Gesture misalignment.
SOLUTION: Keep hand steady and within the gesture box.

ISSUE: Volume/Brightness not changing
CAUSE: Wrong hand used or camera not detecting both hands.
SOLUTION: Use left hand for brightness, right hand for volume.

ISSUE: Program not starting
CAUSE: Missing library.
SOLUTION: Reinstall dependencies using pip install -r requirements.txt.

--------------------------------------------------------------------------------------------

FUTURE ENHANCEMENTS:
- Gesture customization and user-defined mapping.
- Voice command integration.
- Multi-platform support (Windows, Linux, macOS).
- Deep learning-based gesture recognition.
- Gesture logging and analytics.

--------------------------------------------------------------------------------------------

TECHNOLOGIES USED:
- Language: Python 3.8+
- Computer Vision: OpenCV, CVZone, Mediapipe
- Automation: PyAutoGUI, PyCaw, Screen Brightness Control
- Platform: Windows

--------------------------------------------------------------------------------------------

SUPPORT:
For queries or issues:
Email: gayathri.somanath06@gmail.com




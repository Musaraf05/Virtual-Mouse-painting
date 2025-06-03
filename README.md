# Virtual-Mouse-painting
# 🤖 Hand Gesture Recognition Projects

A set of interactive computer vision-based Python projects using hand gesture recognition powered by **MediaPipe** and **OpenCV**. These applications allow for real-time mouse control, painting, and hand tracking using a webcam.

---

## 📁 Projects Included

### 1. HandTrackingModule.py
A utility module to detect hands, track landmarks, count fingers, and measure distances using **MediaPipe**.

#### Features:
- Hand detection and tracking
- Finger counting logic
- Distance calculation between landmarks

---

### 2. AiVirtualMouse.py
Control your computer mouse using hand gestures.

#### Features:
- Move cursor using the index finger
- Click using index and middle fingers together
- Smooth and responsive tracking

#### Usage:
```bash
python AiVirtualMouse.py
```

---

### 3. AiVirtualPainting.py
A virtual canvas where you can draw in the air using your finger.

#### Features:
- Selection mode using two fingers
- Drawing mode using index finger
- Color palette switching
- Eraser functionality
- Auto-save canvas every 30 seconds when only the thumb is up

#### Usage:
Ensure you have a folder named `Header` with button images:
```bash
python AiVirtualPainting.py
```

---

## 🧰 Requirements

Install the necessary Python libraries with:

```bash
pip install -r requirements.txt
```

---

## 📦 requirements.txt
```
opencv-python
mediapipe
numpy
pyautogui
```

---

## 💡 Notes
- Tested on Python 3.8+
- Ensure you have access to a webcam
- The `Header/` folder must contain at least four header images for painting

---

## 🏁 Run
Make sure all scripts and the `Header/` folder are in the same directory. Start any script using:

```bash
python AiVirtualMouse.py
# or
python AiVirtualPainting.py
```

Press `q` to exit any window.

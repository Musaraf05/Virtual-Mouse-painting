import cv2
import numpy as np
import os
import HandTrackingModule as htm 
import time 

#################################
brushThickness = 15
eraserThickness = 90
#################################
folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    if image is not None:
        overlayList.append(image)
    else:
        print(f"Warning: Unable to load image {imPath}")
        
# Check if overlayList is empty
if not overlayList:
    raise ValueError("No images found in the specified header folder.")

header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(minDetectionConfidence=0.85)
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

last_save_time = time.time()  # Track the last save time
save_interval = 30  # Save every 30 seconds

while True:
    # 1. Import image
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        continue  # Skip if frame capture failed
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks 
    img = detector.findHands(img)
    if img is None:  # Additional check to ensure img is not None
        print("Error: No image returned from findHands.")
        continue
    lmList, _ = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tip of index and middle finger 
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. If Selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            # Checking for click 
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing mode - Index finger is up
        if fingers[1] and not fingers[2]:  # Changed condition to check for drawing mode
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1 

    #  # 6. Save the canvas if only the thumb is up
    #     if fingers[0] and not fingers[1] and not fingers[2]:  # Only the thumb is up
    #         filename = f"Drawn_Canvas_{time.strftime('%Y%m%d_%H%M%S')}.png"
    #         cv2.imwrite(filename, imgCanvas)  # Save the canvas
    #         print(f"Canvas saved as {filename}")

     # 6. Save the canvas every 30 seconds if only the thumb is up
        if fingers[0] and not fingers[1] and not fingers[2]:  # Only the thumb is up
            current_time = time.time()
            if current_time - last_save_time >= save_interval:  # Check if 30 seconds have passed
                filename = f"Drawn_Canvas_{time.strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(filename, imgCanvas)  # Save the canvas
                print(f"Canvas saved as {filename}")
                last_save_time = current_time  # Update the last save time

    # Combine the canvas with the live image
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image 
    img[0:125, 0:1280] = header

    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
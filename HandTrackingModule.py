import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.minTrackCon,
            model_complexity=0  # Fast and efficient
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True, flipType=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape

        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                mylmList = []
                xList, yList = [], []

                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label

                allHands.append(myHand)

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 10, bbox[1] - 10),
                                  (bbox[0] + bbox[2] + 10, bbox[1] + bbox[3] + 10),
                                  (255, 0, 255), 2)
                    move_label = f"{self.getMoveName(self.getHandMove(myHand))} {myHand['type']}"
                    cv2.putText(img, move_label, (bbox[0], bbox[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        if draw:
            return allHands, img
        else:
            return allHands

    def fingersUp(self, myHand):
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        fingers = []

        # Thumb
        if myHandType == "Right":
            fingers.append(1 if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0] else 0)
        else:
            fingers.append(1 if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0] else 0)

        # Other fingers
        for id in range(1, 5):
            fingers.append(1 if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1] else 0)
        return fingers

    def getHandMove(self, myHand):
        fingers = self.fingersUp(myHand)
        # Rock: All fingers down
        if fingers == [0, 0, 0, 0, 0]:
            return 1
        # Paper: All fingers up
        elif fingers == [1, 1, 1, 1, 1]:
            return 2
        # Scissors: Index and middle up (allow thumb up or down)
        elif fingers in ([0,1,1,0,0], [1,1,1,0,0]):
            return 3
        else:
            return 0  # Unknown

    def getMoveName(self, move):
        return {1: "Rock", 2: "Paper", 3: "Scissors"}.get(move, "")

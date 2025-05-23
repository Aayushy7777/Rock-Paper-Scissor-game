import cv2
import random
import time
import numpy as np
from HandTrackingModule import HandDetector

class RockPaperScissorsGame:
    def __init__(self):
        self.WINDOW_WIDTH = 1317
        self.WINDOW_HEIGHT = 768
        self.CAMERA_SQUARE_SIZE = 400

        self.colors = {
            'bg': (255, 250, 240),
            'border': (255, 221, 102),
            'ai_box': (160, 100, 255),
            'player_box': (160, 100, 255),
            'ai_score': (255, 99, 71),
            'player_score': (120, 255, 120),
            'purple': (160, 32, 240),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'green': (0, 255, 0),
            'yellow': (0, 255, 255),
            'cyan': (255, 255, 0),
            'pink': (255, 0, 255)
        }

        self.scores = [0, 0]  # [AI, Player]
        self.timer = 0
        self.stateResult = False
        self.startGame = False
        self.initialTime = 0
        self.aiMove = None
        self.playerMove = None
        self.gesture_buffer = []

        self.moves = {1: "Rock", 2: "Paper", 3: "Scissors"}
        self.detector = HandDetector(maxHands=1)
        self.cap = cv2.VideoCapture(0)

    def get_square_camera_image(self, img, output_size):
        h, w = img.shape[:2]
        min_dim = min(h, w)
        start_x = (w - min_dim) // 2
        start_y = (h - min_dim) // 2
        cropped = img[start_y:start_y+min_dim, start_x:start_x+min_dim]
        square_img = cv2.resize(cropped, (output_size, output_size))
        return square_img

    def draw_background(self, img):
        img[:,:] = self.colors['bg']
        cv2.rectangle(img, (0,0), (self.WINDOW_WIDTH-1, self.WINDOW_HEIGHT-1), self.colors['border'], 12)
        for i in range(0, self.WINDOW_WIDTH, 60):
            cv2.line(img, (i,0), (i+self.WINDOW_HEIGHT, self.WINDOW_HEIGHT), (240,240,240), 8)
        return img

    def draw_header(self, img):
        cv2.putText(img, "ROCK - PAPER - SCISSOR", (320, 70), cv2.FONT_HERSHEY_DUPLEX, 2.2, (80, 120, 255), 5)
        cv2.putText(img, "ROCK - PAPER - SCISSOR", (320, 70), cv2.FONT_HERSHEY_DUPLEX, 2.2, (50, 90, 180), 2)
        cv2.putText(img, "🪨", (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (120,120,120), 4)
        cv2.putText(img, "✂️", (1150, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (120,120,120), 4)
        cv2.putText(img, "✂️", (1150, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2)

    def draw_section(self, img, x, y, w, h, label, score, move, is_ai=False):
        box_color = self.colors['ai_box'] if is_ai else self.colors['player_box']
        score_color = self.colors['ai_score'] if is_ai else self.colors['player_score']
        cv2.rectangle(img, (x, y), (x+w, y+h), box_color, 8)
        cv2.rectangle(img, (x, y), (x+w, y+60), box_color, -1)
        cv2.putText(img, label, (x+20, y+45), cv2.FONT_HERSHEY_DUPLEX, 1.5, self.colors['white'], 3)
        cv2.rectangle(img, (x+w-70, y), (x+w, y+60), score_color, -1)
        cv2.putText(img, str(score), (x+w-55, y+45), cv2.FONT_HERSHEY_DUPLEX, 1.6, self.colors['white'], 4)
        if is_ai:
            cv2.circle(img, (x+w//2, y+200), 110, (200, 150, 255), -1)
            if move:
                cv2.putText(img, move, (x+80, y+120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.colors['pink'], 2)

    def draw_center(self, img):
        cx = self.WINDOW_WIDTH // 2
        cy = self.WINDOW_HEIGHT // 2
        cv2.line(img, (cx, 140), (cx, self.WINDOW_HEIGHT-80), (180,180,180), 4)
        cv2.rectangle(img, (cx-80, cy-50), (cx+80, cy+50), (255,180,90), -1)
        cv2.rectangle(img, (cx-80, cy-50), (cx+80, cy+50), (255,150,80), 6)

    def draw_camera_feed(self, img, camera_img, x, y):
        img[y+70:y+70+camera_img.shape[0], x+20:x+20+camera_img.shape[1]] = camera_img

    def draw_status(self, img, status):
        cv2.putText(img, status, (60, self.WINDOW_HEIGHT-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    def draw_controls(self, img):
        cv2.putText(img, "Press 's' to start, 'r' to reset, 'q' to quit", (350, self.WINDOW_HEIGHT-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    def determine_winner(self, player, ai):
        if player == ai:
            return "tie"
        elif (player == 1 and ai == 3) or (player == 2 and ai == 1) or (player == 3 and ai == 2):
            return "player"
        else:
            return "ai"

    def most_frequent_gesture(self, gestures):
        valid = [g for g in gestures if g in [1,2,3]]
        if not valid:
            return None
        return max(set(valid), key=valid.count)

    def process_game_logic(self, hands):
        if self.startGame:
            if not self.stateResult:
                self.timer = time.time() - self.initialTime
                countdown = max(0, int(4 - self.timer))
                if countdown > 0:
                    if hands:
                        hand = hands[0]
                        gesture = self.detector.getHandMove(hand)
                        self.gesture_buffer.append(gesture)
                    else:
                        self.gesture_buffer.append(0)
                if self.timer > 3:
                    self.stateResult = True
                    self.timer = 0
                    self.playerMove = self.most_frequent_gesture(self.gesture_buffer)
                    self.gesture_buffer = []
                    self.aiMove = random.randint(1, 3)
                    if self.playerMove and self.playerMove in [1,2,3]:
                        result = self.determine_winner(self.playerMove, self.aiMove)
                        if result == "player":
                            self.scores[1] += 1
                        elif result == "ai":
                            self.scores[0] += 1
                return countdown
        return 0

    def run(self):
        while True:
            success, camera_img = self.cap.read()
            if not success:
                continue
            camera_img = cv2.flip(camera_img, 1)
            square_camera_img = self.get_square_camera_image(camera_img, self.CAMERA_SQUARE_SIZE)
            hands, square_camera_img = self.detector.findHands(square_camera_img, draw=True)

            countdown = self.process_game_logic(hands)

            main_img = np.zeros((self.WINDOW_HEIGHT, self.WINDOW_WIDTH, 3), np.uint8)
            main_img = self.draw_background(main_img)
            self.draw_header(main_img)
            self.draw_center(main_img)

            ai_x, ai_y, ai_w, ai_h = 80, 120, 400, 500
            player_x, player_y, player_w, player_h = self.WINDOW_WIDTH-480, 120, 400, 500

            ai_move_name = self.moves.get(self.aiMove, "") if self.stateResult else ""
            self.draw_section(main_img, ai_x, ai_y, ai_w, ai_h, "AI", self.scores[0], ai_move_name, is_ai=True)

            player_move_name = self.moves.get(self.playerMove, "") if self.stateResult else ""
            self.draw_section(main_img, player_x, player_y, player_w, player_h, "PLAYER", self.scores[1], player_move_name, is_ai=False)
            self.draw_camera_feed(main_img, square_camera_img, player_x, player_y)

            if not self.startGame:
                status = "Press 's' to start playing!"
            elif countdown > 0:
                status = "Get ready! Show your hand gesture clearly."
                cv2.putText(main_img, f"Show your move in: {countdown}", (500, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)
            elif self.stateResult:
                if self.playerMove and self.playerMove in [1,2,3]:
                    result = self.determine_winner(self.playerMove, self.aiMove)
                    if result == "player":
                        status = "Player wins this round!"
                    elif result == "ai":
                        status = "AI wins this round!"
                    else:
                        status = "It's a tie!"
                else:
                    status = "No valid gesture detected! Please try again."
            else:
                status = ""
            self.draw_status(main_img, status)
            self.draw_controls(main_img)

            cv2.imshow("Rock Paper Scissors", main_img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                if not self.startGame or self.stateResult:
                    self.startGame = True
                    self.initialTime = time.time()
                    self.stateResult = False
                    self.aiMove = None
                    self.playerMove = None
                    self.gesture_buffer = []
            elif key == ord('r'):
                self.scores = [0, 0]
                self.startGame = False
                self.stateResult = False
                self.aiMove = None
                self.playerMove = None
                self.gesture_buffer = []
            elif key == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    RockPaperScissorsGame().run()

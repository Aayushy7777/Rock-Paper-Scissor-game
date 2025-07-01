Rock-Paper-Scissors Hand Gesture Game
A modern, interactive Rock-Paper-Scissors game using your webcam and hand gestures, powered by OpenCV and MediaPipe.
Challenge the AI, see your score live, and enjoy a smooth and visually appealing interface!

![Screenshot 2025-04-10 141614](https://github.com/user-attachments/assets/867b3c89-db55-4125-b04a-6e3f87e4d0bf)

![Screenshot 2025-04-10 141542](https://github.com/user-attachments/assets/f0579aca-d05e-455b-9660-22f748ca8b2e)

![Uploading Screenshot 2025-04-10 141458.png…]()


Features
🖐️ Hand gesture recognition for Rock, Paper, and Scissors using MediaPipe

🎥 Live webcam feed with hand landmarks and gesture labels

🤖 AI opponent with random moves

📊 Score tracking for both player and AI

🖼️ Modern, colorful UI with clear sections for player and AI

🟩 Robust gesture detection (aggregates over several frames for accuracy)

🟦 Easy controls:

s to start a round

r to reset the game

q to quit

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/rock-paper-scissors-gesture.git
cd rock-paper-scissors-gesture
Install dependencies:

bash
pip install opencv-python mediapipe numpy
Usage
Run the game:

bash
python main.py
Show your hand gesture (rock, paper, or scissors) in the camera box during the countdown.

See the result and score!

File Structure
text
rock-paper-scissors-gesture/
│
├── main.py                  # Main game logic and UI
├── handTrackingModule.py    # Hand detection and gesture recognition
├── README.md
└── screenshot.png           # (Optional) Screenshot of the game UI
How It Works
Uses your webcam to detect your hand and recognize gestures (rock, paper, scissors).

Aggregates gesture detection over multiple frames for robust results.

AI randomly selects its move.

Scores are updated and displayed after each round.

Tips for Best Performance
Make sure your hand is fully visible and well-lit in the camera box.

Hold your gesture steady during the countdown.

For best results, use a plain background behind your hand.

Credits
MediaPipe for hand tracking

OpenCV for image processing

UI inspired by modern game layouts

License
MIT License.
Feel free to use, modify, and share!

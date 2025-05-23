🪨✋✂️ Rock-Paper-Scissors Hand Gesture Game
A modern, interactive Rock-Paper-Scissors game using your webcam and hand gestures, powered by OpenCV and MediaPipe.
Challenge the AI, track your score live, and enjoy a smooth, colorful UI!

![Uploading Screenshot 2025-04-10 141614.png…]()


🚀 Features
🖐️ Hand Gesture Recognition for Rock, Paper, and Scissors using MediaPipe

🎥 Live Webcam Feed with hand landmarks and gesture labels

🤖 AI Opponent that selects moves randomly

📊 Score Tracker for Player vs AI

🎨 Modern UI with clearly defined sections

✅ Robust Detection by aggregating results across frames

🎮 Simple Controls:

s → Start a new round

r → Reset the game

q → Quit the game

🧩 Installation
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/rock-paper-scissors-gesture.git
cd rock-paper-scissors-gesture
2️⃣ Install Dependencies
bash
Copy
Edit
pip install opencv-python mediapipe numpy
🕹️ How to Play
bash
Copy
Edit
python main.py
Show your Rock, Paper, or Scissors gesture in the webcam box.

Hold steady during the countdown.

The AI selects its move.

See the result and live score on screen!

🗂️ File Structure
bash
Copy
Edit
rock-paper-scissors-gesture/
├── main.py                # Main game logic and UI rendering
├── handTrackingModule.py  # Hand detection and gesture recognition
├── README.md              # Project overview
└── screenshot.png         # Optional screenshot for README
🔍 How It Works
Uses MediaPipe for real-time hand tracking.

Recognizes gestures based on the relative positions of landmarks.

Aggregates detection over several frames to avoid false recognition.

Displays the AI vs Player UI with moves and scores.

📷 Tips for Best Performance
Use a well-lit area with no hand occlusion.

Maintain a steady gesture during the countdown.

Prefer a plain background to improve gesture detection accuracy.

🙏 Credits
MediaPipe – Real-time hand tracking

OpenCV – Image and video processing

UI inspired by modern game HUDs

📄 License
This project is licensed under the MIT License.
Feel free to use, share, and build upon it!


MIT License.
Feel free to use, modify, and share!

Enjoy playing Rock-Paper-Scissors with your computer!

If you like this project, please ⭐ star it on GitHub!

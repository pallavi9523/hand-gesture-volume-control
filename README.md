## 🎯 AI Gesture-Based Music Controller

### 📌 Project Description

This project is an AI-based Gesture Music Controller that uses computer vision to enable touchless control of music playback. The system utilizes a webcam to detect and track hand gestures in real time, allowing users to interact with their media player without physical contact.

By leveraging advanced hand tracking techniques, the application can recognize specific gestures to perform actions such as adjusting volume, playing or pausing music, and navigating between songs. This makes the system intuitive, efficient, and suitable for modern human-computer interaction.

---

### 🚀 Key Features

* ✋ Real-time hand tracking using computer vision
* 🔊 Volume control based on finger distance
* ⏯ Play and pause music using gestures
* ⏭ Next and previous song navigation
* 🎵 Support for multiple audio files (playlist)
* 📷 Live webcam integration
* 🎯 Smooth and responsive user interface

---

### 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame

---

### ▶️ How It Works

The system captures live video from the webcam and processes it using MediaPipe to detect hand landmarks. Based on the position and movement of fingers, specific gestures are identified and mapped to different media control actions. For example:

* The distance between thumb and index finger controls volume
* A closed fist pauses the music
* An open hand resumes playback
* Three fingers trigger the next song
* Four fingers trigger the previous song

---

### 📂 Setup Instructions

1. Clone the repository
2. Install required libraries:

   ```
   pip install opencv-python mediapipe numpy pygame
   ```
3. Add your own music files in the project folder:

   ```
   song1.mp3, song2.mp3, song3.mp3
   ```
4. Run the program:

   ```
   python control_volume.py
   ```

---

### ⚠️ Note

Music files are not included in this repository due to copyright restrictions. Users are required to add their own MP3 files.

---

### 💡 Future Enhancements

* Screen brightness control using gestures
* Integration with voice commands
* Gesture-based system navigation
* Mobile or web-based implementation

---

### 🏆 Author

**Pallavi Shree**

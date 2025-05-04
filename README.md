#MOODIFY
# 🎧 Mood-Based Music Recommender 🎵

Welcome to your personalized music companion!  
This web app detects your **mood** from a selfie or lets you choose it manually — then recommends songs that perfectly match your vibe. 💫

---

## 🖼️ How It Works

🎭 **Choose Your Mood:**
- Upload a selfie (we'll analyze your facial expression using ML), **OR**
- Select your mood manually: 😊 Happy | 😢 Sad | 😡 Angry | 😌 Calm

🧠 **ML in Action:**
- Uses **DeepFace** or **FER** to detect emotion from your uploaded photo.
- Optionally, basic sentiment analysis on typed input.

🎶 **Music Recommendation:**
- Based on the detected or selected mood, you'll get a curated playlist.
- YouTube embeds or static playlists mapped to each mood.

---

## 🚀 Live Demo

🔗 **Live Site:** [Add your hosted link here]  
🖥️ **Local Access:** `http://localhost:5000`

---

## 🛠️ Tech Stack

| 🧩 Layer       | ⚙️ Technologies                        |
|---------------|----------------------------------------|
| 🎨 Frontend    | HTML, CSS (Bootstrap), JavaScript      |
| 🔧 Backend     | Python Flask                           |
| 🤖 ML Libraries| DeepFace, FER, OpenCV, NumPy           |
| 🚀 Deployment  | (Optional) Render / Heroku / Localhost |

---

## 📁 Project Structure

```plaintext
mood-music-recommender/
├── static/         📁 → CSS, JS, images
├── templates/      📁 → HTML templates (Home, Results, About, Contact)
├── model/          📁 → ML logic and utilities
├── app.py          🧠 → Main Flask application
├── requirements.txt📄 → Python dependencies
└── README.md       📘 → Project overview

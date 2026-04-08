# 🔥 Universal Video Downloader

A powerful and modern **Flask-based video downloader** that allows you to download videos from **YouTube, Instagram, Facebook, and many other platforms** with a clean UI and advanced features.

---

## ✨ Features

### 🎯 Core Features

* 📥 Download videos using direct URL
* 🔎 YouTube Search inside app
* 🌐 Supports multiple websites (via yt-dlp)
* 🖼️ Video preview (thumbnail, title, duration)

### 🎚️ Quality & Format

* 🎥 Video quality options:

  * Best Quality
  * 720p / 480p / 360p
* 🎵 Audio-only mode:

  * MP3 / M4A
  * 128 / 192 / 320 kbps

### ⚡ Smart Features

* 📊 Shows **video + audio size before download**
* 🔄 Auto-selects best format
* 🎯 Merges video + audio automatically
* 📁 Clean file saving system

### 🎨 UI Features

* 🧩 Tab-based UI:

  * 📥 YT URL
  * 🔎 YT Search
  * 🌐 All Sites
* 📊 Progress bar
* 📱 Fully responsive design

---

## 🏗️ Project Structure

```
universal-downloader/
│
├── app.py
├── templates/
│   └── index.html
├── Licence
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/universal-downloader.git
cd universal-downloader
```

---

### 2️⃣ Install Dependencies

```bash
pip install flask yt-dlp requests
```

---

### 3️⃣ Install FFmpeg (IMPORTANT ⚠️)

👉 Required for audio extraction

#### Windows:

* Download: https://ffmpeg.org/download.html
* Add to system PATH

#### Linux:

```bash
sudo apt install ffmpeg
```

#### Mac:

```bash
brew install ffmpeg
```

---

## ▶️ Run the App

```bash
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

## 🧠 How to Use

### 🔹 1. YT URL Download

1. Paste video URL
2. Click **Fetch Video Info**
3. Select:

   * Video quality OR
   * Audio-only mode
4. Click **Download**

---

### 🔹 2. YouTube Search

1. Enter keyword
2. Click **Search**
3. Choose video
4. Click **Download**

---

### 🔹 3. All Sites Mode

1. Paste any video page link
2. Preview video
3. Download

---

## 🎵 Audio Mode

✔ Enable **Audio Only**

Then choose:

* Format → `mp3` / `m4a`
* Bitrate → `128 / 192 / 320 kbps`

---

## 📦 Output

All downloaded files are saved in:

```
/downloads
```

---

## 🔐 API Usage Notice

This application uses the **YouTube Data API v3** for search functionality.

⚠️ You MUST use your own API key.

### Important:

* Do NOT rely on any pre-included API key
* API keys may stop working or exceed quota
* Each user is responsible for their own API usage

### 🔑 Get your API key:

1. Go to Google Cloud Console
2. Create a project
3. Enable **YouTube Data API v3**
4. Generate API key

Replace in `app.py`:

```python
API_KEY = "YOUR_API_KEY"
```

🚫 The developer is not responsible for:

* API quota issues
* Key misuse
* Service interruptions

---

## 🛠️ Tech Stack

* ⚙️ Backend: Flask
* 🎨 Frontend: HTML, CSS, JavaScript
* 📦 Downloader: yt-dlp
* 🔗 API: YouTube Data API

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.

🚫 Do not download copyrighted content without permission
🚫 Respect platform terms and policies

---

## 🔥 Future Improvements

* 📊 Real-time download progress (speed + ETA)
* 📂 Download history
* 📱 Android APK version
* 🖥️ Desktop (.exe installer)
* 🎨 UI improvements
* 📥 Playlist downloader

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a Pull Request

---

## ⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
📢 Share it

---

## 👑 Author

Made with ❤️ by **Abhishek Garg**

---

## 🚀 Pro Tips

* Use **Best Quality** for highest resolution
* Use **MP3 320 kbps** for best audio
* Keep FFmpeg properly installed

---


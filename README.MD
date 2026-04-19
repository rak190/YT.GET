# YT.GET — Personal YouTube Downloader

A local web app that runs on your computer to download YouTube videos.
Files are saved to your `Downloads/YT-Downloads` folder.

---

## Setup (do this once)

### Step 1 — Install Python
Download from https://python.org and install it.
Make sure to check "Add Python to PATH" during install.

### Step 2 — Install required tools

Open **Command Prompt** (Windows) or **Terminal** (Mac) and run:

```
pip install flask yt-dlp
```

Then install **ffmpeg** (needed to merge video+audio):

- **Windows**: Download from https://ffmpeg.org/download.html
  - Extract the zip, copy `ffmpeg.exe` to the same folder as `server.py`
  - OR add ffmpeg to your PATH

- **Mac**: Run `brew install ffmpeg` (install Homebrew first from brew.sh)

---

## How to Run

1. Put `server.py` and `index.html` in the same folder
2. Open Command Prompt / Terminal in that folder
3. Run:
   ```
   python server.py
   ```
4. Open your browser and go to: **http://localhost:5000**
5. Paste a YouTube URL and download!

---

## Usage

1. Paste a YouTube video URL into the box
2. Click **FETCH** to load video info
3. Choose your format (video quality or MP3)
4. Click **DOWNLOAD**
5. Find your file in `Downloads/YT-Downloads`

---

## Notes
- This tool is for **personal use only**
- Downloads are saved to `~/Downloads/YT-Downloads`
- Keep `server.py` running while you use the browser app
- For personal/school presentations only

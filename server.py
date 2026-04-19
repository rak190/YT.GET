from flask import Flask, request, jsonify, send_from_directory
import subprocess, os, json, re, threading

app = Flask(__name__, static_folder=".")
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "YT-Downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/info", methods=["POST"])
def info():
    url = request.json.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    stdout, stderr = run(["yt-dlp", "--dump-json", "--no-playlist", url])
    if not stdout:
        return jsonify({"error": "Could not fetch video info. Check the URL."}), 400
    try:
        data = json.loads(stdout)
        formats = []
        seen = set()
        for f in data.get("formats", []):
            ext = f.get("ext", "")
            height = f.get("height")
            acodec = f.get("acodec", "none")
            vcodec = f.get("vcodec", "none")
            fid = f.get("format_id", "")
            if height and vcodec != "none" and ext in ("mp4", "webm"):
                label = f"{height}p ({ext})"
                if label not in seen:
                    seen.add(label)
                    formats.append({"id": fid, "label": label, "type": "video", "height": height})
        formats.sort(key=lambda x: -x["height"])
        formats.append({"id": "mp3", "label": "MP3 (audio only)", "type": "audio"})
        return jsonify({
            "title": data.get("title", "Unknown"),
            "thumbnail": data.get("thumbnail", ""),
            "duration": data.get("duration_string", ""),
            "channel": data.get("channel", ""),
            "formats": formats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url", "").strip()
    fmt = request.json.get("format", "").strip()
    if not url or not fmt:
        return jsonify({"error": "Missing URL or format"}), 400

    if fmt == "mp3":
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3",
               "-o", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"), url]
    else:
        cmd = ["yt-dlp", "-f", f"{fmt}+bestaudio/best", "--merge-output-format", "mp4",
               "-o", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"), url]

    stdout, stderr = run(cmd)
    if "has already been downloaded" in stdout or "Destination" in stdout or "[ffmpeg]" in stdout or "100%" in stdout:
        return jsonify({"success": True, "path": DOWNLOAD_DIR})
    # Try to detect success another way
    if stderr and "ERROR" in stderr:
        return jsonify({"error": stderr.split("ERROR:")[-1].strip()}), 500
    return jsonify({"success": True, "path": DOWNLOAD_DIR})

if __name__ == "__main__":
    print("=" * 50)
    print("  YouTube Downloader running!")
    print("  Open: http://localhost:5000")
    print(f"  Files saved to: {DOWNLOAD_DIR}")
    print("=" * 50)
    app.run(debug=False, port=5000)

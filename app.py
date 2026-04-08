import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import requests
import yt_dlp

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_FOLDER = BASE_DIR / "downloads"
DOWNLOAD_FOLDER.mkdir(exist_ok=True)

# Put your YouTube API key here for YT Search tab
API_KEY = "USE YOUR API KEY"

app = Flask(__name__, template_folder="templates")


def format_duration(seconds):
    if not seconds:
        return "Unknown"

    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"



def format_bytes(num):
    if num is None:
        return "Unknown"

    num = float(num)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"



def estimate_audio_size(duration_seconds, bitrate_kbps):
    if not duration_seconds:
        return None
    return (duration_seconds * bitrate_kbps * 1000) / 8



def safe_filesize(fmt):
    return fmt.get("filesize") or fmt.get("filesize_approx")



def search_youtube(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": API_KEY,
        "maxResults": 8,
        "type": "video",
    }

    res = requests.get(url, params=params, timeout=20)
    data = res.json()

    if "error" in data:
        msg = data["error"].get("message", "YouTube API error")
        raise Exception(msg)

    videos = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        video_id = item.get("id", {}).get("videoId", "")

        videos.append(
            {
                "title": snippet.get("title", "No title"),
                "videoId": video_id,
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                "channel": snippet.get("channelTitle", "Unknown channel"),
            }
        )

    return videos



def build_download_options(info):
    formats = info.get("formats", [])
    duration = info.get("duration") or 0

    desired_heights = {
        "Best Quality": None,
        "720p": 720,
        "480p": 480,
        "360p": 360,
    }

    best_audio_size = None
    for fmt in formats:
        if fmt.get("vcodec") == "none" and fmt.get("acodec") != "none":
            size = safe_filesize(fmt)
            if size and (best_audio_size is None or size > best_audio_size):
                best_audio_size = size

    progressive_formats = []
    video_only_formats = []

    for fmt in formats:
        height = fmt.get("height")
        if not height:
            continue

        has_video = fmt.get("vcodec") != "none"
        has_audio = fmt.get("acodec") != "none"

        if has_video and has_audio:
            progressive_formats.append(fmt)
        elif has_video:
            video_only_formats.append(fmt)

    quality_options = []
    for label, max_height in desired_heights.items():
        candidate_sizes = []

        for fmt in progressive_formats:
            h = fmt.get("height")
            if max_height is None or (h and h <= max_height):
                size = safe_filesize(fmt)
                if size:
                    candidate_sizes.append(size)

        for fmt in video_only_formats:
            h = fmt.get("height")
            if max_height is None or (h and h <= max_height):
                vsize = safe_filesize(fmt)
                if vsize:
                    total_size = vsize + (best_audio_size or 0)
                    candidate_sizes.append(total_size)

        if candidate_sizes:
            best_size = max(candidate_sizes)
            display = f"{label} ({format_bytes(best_size)})"
        else:
            display = f"{label} (Size Unknown)"

        quality_options.append(display)

    audio_bitrate_options = []
    for bitrate in [128, 192, 320]:
        est_size = estimate_audio_size(duration, bitrate)
        if est_size:
            display = f"{bitrate} kbps ({format_bytes(est_size)})"
        else:
            display = f"{bitrate} kbps (Size Unknown)"
        audio_bitrate_options.append(display)

    return quality_options, audio_bitrate_options



def get_video_info(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        quality_options, audio_bitrate_options = build_download_options(info)

        return {
            "title": info.get("title", "Unknown Title"),
            "thumbnail": info.get("thumbnail", ""),
            "uploader": info.get("uploader", "Unknown"),
            "duration": format_duration(info.get("duration")),
            "duration_seconds": info.get("duration"),
            "webpage_url": info.get("webpage_url", url),
            "quality_options": quality_options,
            "audio_bitrate_options": audio_bitrate_options,
        }



def normalize_quality_value(raw_quality):
    raw_quality = (raw_quality or "").strip().lower()
    mapping = {
        "best": "Best Quality",
        "best quality": "Best Quality",
        "720": "720p",
        "720p": "720p",
        "480": "480p",
        "480p": "480p",
        "360": "360p",
        "360p": "360p",
    }
    return mapping.get(raw_quality, "Best Quality")



def build_format_string(quality, audio_only):
    if audio_only:
        return "bestaudio/best"

    if quality == "720p":
        return "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
    if quality == "480p":
        return "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
    if quality == "360p":
        return "bestvideo[height<=360]+bestaudio/best[height<=360]/best"
    return "bestvideo+bestaudio/best"



def safe_output_template():
    return str(DOWNLOAD_FOLDER / "%(title)s.%(ext)s")



def download_video(url, quality="Best Quality", audio_only=False, audio_format="mp3", bitrate="192"):
    fmt = build_format_string(quality, audio_only)

    ydl_opts = {
        "outtmpl": safe_output_template(),
        "format": fmt,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "nocheckcertificate": True,
        "quiet": True,
    }

    if audio_only:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": str(bitrate),
            }
        ]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        if audio_only:
            base, _ = os.path.splitext(filename)
            filename = f"{base}.{audio_format}"

        return filename


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    url = request.form.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        info = get_video_info(url)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    if not query:
        return jsonify([{"error": "Search query is required"}]), 400

    try:
        videos = search_youtube(query)
        return jsonify(videos)
    except Exception as e:
        return jsonify([{"error": str(e)}])


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()
    quality = normalize_quality_value(request.form.get("quality", "best"))
    audio_only = request.form.get("audio_only", "false").strip().lower() in {"true", "1", "yes", "on"}
    audio_format = request.form.get("audio_format", "mp3").strip().lower() or "mp3"
    bitrate = request.form.get("bitrate", "192").strip() or "192"

    if audio_format not in {"mp3", "m4a"}:
        audio_format = "mp3"

    if bitrate not in {"128", "192", "320"}:
        bitrate = "192"

    if not url:
        return "URL is required", 400

    try:
        saved_file = download_video(
            url=url,
            quality=quality,
            audio_only=audio_only,
            audio_format=audio_format,
            bitrate=bitrate,
        )
        return f"Downloaded successfully: {os.path.basename(saved_file)}"
    except Exception as e:
        return f"Download failed: {e}", 500


@app.route("/quality_options", methods=["POST"])
def quality_options():
    url = request.form.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        info = get_video_info(url)
        return jsonify({
            "quality_options": info.get("quality_options", []),
            "audio_bitrate_options": info.get("audio_bitrate_options", []),
        })
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

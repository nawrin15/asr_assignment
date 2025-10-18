import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.video_utils import get_whisper_srt

# Load .env values
def load_env_vars():
    load_dotenv(dotenv_path="dev.env")  # or "test.env" based on context

load_env_vars()

app = Flask(__name__)

# Dummy in-memory store to simulate project states
project_status = {}

@app.route("/build_srt_file/<project_id>", methods=["POST"])
def build_srt_file(project_id):
    try:
        audio_bytes = request.data
        whisper_result = get_whisper_srt(f"{project_id}.wav", audio_bytes)

        # Simulate setting project state
        project_status[project_id] = "MEDIA_SRT_CREATED"

        return jsonify({
            "status": "success",
            "message": "SRT created successfully",
            "project_id": project_id,
            "state": project_status[project_id],
            "transcription": whisper_result["text"]  
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

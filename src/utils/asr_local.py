from faster_whisper import WhisperModel
import tempfile
import os
from typing import Optional

def transcribe_local(audio_bytes: bytes, language: Optional[str] = None) -> dict:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        audio_path = tmp.name

    model = WhisperModel("base", compute_type="int8")
    segments, _ = model.transcribe(audio_path, language=language, beam_size=5, word_timestamps=True)

    results = {
        "text": "",
        "segments": []
    }

    for i, segment in enumerate(segments):
        segment_data = {
            "id": i,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text,
            "words": [{"start": w.start, "end": w.end, "word": w.word} for w in segment.words]
        }
        results["segments"].append(segment_data)
        results["text"] += segment.text + " "

    # Optional: delete tmp file
    os.remove(audio_path)

    return results

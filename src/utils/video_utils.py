import os
from .asr_local import transcribe_local

def get_whisper_srt(file_name, audio_bytes):
    provider = os.getenv("WHISPER_PROVIDER", "auto")

    if provider == "openai":
        return openai_whisper(audio_bytes)
    
    elif provider == "faster-whisper":
        return transcribe_local(audio_bytes)
    
    elif provider == "auto":
        try:
            return openai_whisper(audio_bytes)
        except Exception as e:
            print(f"[Fallback] OpenAI failed: {e}")
            return transcribe_local(audio_bytes)

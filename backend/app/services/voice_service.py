
import os
import tempfile
from openai import OpenAI
from app.core.config import settings

class VoiceService:
    def __init__(self):
        # Prefer OpenAI Key, but could fallback if needed
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
             # In a real app, maybe log warning or disable voice
             pass
        else:
            self.client = OpenAI(api_key=self.api_key)

    def transcribe(self, audio_bytes: bytes) -> str:
        if not hasattr(self, 'client'):
            raise ValueError("OpenAI API Key not configured for voice transcription")

        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name

            try:
                with open(temp_audio_path, "rb") as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file,
                        response_format="text"
                    )
                return transcription
            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

voice_service = VoiceService()

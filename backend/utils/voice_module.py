
import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceProcessor:
    """Handles audio transcription using OpenAI Whisper API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
        
        self.client = OpenAI(api_key=self.api_key)

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """
        Transcribes audio bytes to text using OpenAI Whisper API.
        
        Args:
            audio_bytes: Raw bytes from the audio recording
            
        Returns:
            str: Transcribed text
        """
        try:
            # Create a temporary file for the audio
            # Whisper API requires a file-like object with a valid format (e.g., .wav, .mp3, .webm)
            # streamlit-mic-recorder outputs WAV by default
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name

            try:
                # Open the file and send to Whisper API
                with open(temp_audio_path, "rb") as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file,
                        response_format="text"
                    )
                
                return transcription
                
            finally:
                # Cleanup: remove the temporary file
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
                    
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

# Simple helper for direct use
def transcribe(audio_bytes):
    processor = VoiceProcessor()
    return processor.transcribe_audio(audio_bytes)

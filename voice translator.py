import whisper
from openai import OpenAI
import playsound
import sounddevice as sd
import soundfile as sf
import tempfile
import os
from deep_translator import GoogleTranslator
import time
from openai import RateLimitError


client = OpenAI(api_key='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')

filename = "/Users/wj/Documents/sample/recording.wav"


model = whisper.load_model("base")


translator = GoogleTranslator(source='auto', target='zh-CN')

def record_audio(duration=5, samplerate=44100):
    print("Recording...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float64')
    sd.wait()
    print("Recording stopped")
    return myrecording

def save_recording(recording, filename="recording.wav", samplerate=44100):
    sf.write(filename, recording, samplerate)

def openai_tts(text, lang='zh-CN'):
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        # Use NamedTemporaryFile to create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            response.stream_to_file(tmp.name)
            return tmp.name
    except RateLimitError as e:
        print("Rate limit exceeded. Please try again later.")
      
        
  
        return None 
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        response.stream_to_file(tmp.name)
        return tmp.name

while True:
    print("Speak Now")
    recording = record_audio()
    save_recording(recording, filename)

    result = model.transcribe(filename)
    text = result["text"]
    print(f"You said: {text}")

    if text.lower() == "i'm done":
        break

    translated_text = translator.translate(text)
    print(f"Translated to Chinese: {translated_text}")

   
    tts_file = openai_tts(translated_text, lang='zh-CN')
    if tts_file:  
        playsound.playsound(tts_file)
        os.remove(tts_file)  
    else:
        print("Could not generate TTS audio. Skipping playback.")

print("Smell you later")
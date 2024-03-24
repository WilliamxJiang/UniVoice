import googletrans
import speech_recognition as sr
import gtts
import playsound

# Initialize recognizer
recognizer = sr.Recognizer()

# Keep running the program until the user says 'I'm done'
while True:
    with sr.Microphone() as source:
        print("Speak now or say 'I'm done' to exit:")
        
        # Adjust the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        audio = recognizer.listen(source)
        
        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio, language='en')
            print(f"You said: {text}")
            
            # Check if the user said 'I'm done'
            if text.lower() == "i'm done":
                print("Smell you later")
                break
            
            # Translation to French
            translator = googletrans.Translator()
            translation = translator.translate(text, dest='fr')
            print(f"Translated to French: {translation.text}")
            
            # Text-to-speech conversion
            converted_audio = gtts.gTTS(translation.text, lang='fr')
            # Save the audio to a file
            converted_audio.save('translation.mp3')
            # Play the converted file
            playsound.playsound('translation.mp3')
            
        except sr.UnknownValueError:
            # Error handling for unknown words or accents
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            # Error handling for recognizer not connected
            print(f"Could not request results from Google Speech Recognition service; {e}")

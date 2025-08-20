import pyttsx3
import speech_recognition as sr


# Init speech recognition configuration
recognizer = sr.Recognizer()

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("voice", engine.getProperty("voices")[0].id)
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as mic:
            print("Listening...")
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio, language="es-ES")
            print("I heard this: {}".format(text))
            return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print("Could not request results: {}".format(e))


if __name__ == '__main__':
    # Testing speak method
    speak("Hello world!")
    # print(engine.getProperty("rate"))
    # print(engine.getProperty("voice"))
    # print(engine.getProperty("volume"))
    # print([voice.id for voice in engine.getProperty("voices")])

    # Testing recognizer
    listen()
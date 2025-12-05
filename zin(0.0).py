import datetime
import os
import random
import webbrowser
import speech_recognition as sr
import pyttsx3
import pygame
import re
import subprocess
import sys

engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    print(f"Zin: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=4, phrase_time_limit=6)
            return r.recognize_google(audio).lower()
    except:
        return input("You (type): ").lower()

def get_time():
    speak(f"It's {datetime.datetime.now().strftime('%I:%M %P')}.")

def play_music():
    music_dir = "music"
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        speak("No music folder. I created one—add MP3 or WAV files there.")
        return
    songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
    if not songs:
        speak("No music files found in the 'music' folder.")
        return
    song = os.path.join(music_dir, random.choice(songs))
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    speak(f"Now playing: {os.path.basename(song)}")

def open_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Opening YouTube for: {query}")

def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak("Searching on Google.")

def ask_local_ai(prompt):
    try:
        result = subprocess.run([
            sys.executable, "-m", "llm", "chat",
            "-m", "phi3",
            "--prompt", f"You are a helpful coding assistant. Answer concisely. {prompt}"
        ], capture_output=True, text=True, timeout=60)
        answer = result.stdout.strip()
        if not answer:
            answer = "Hmm, I couldn't generate a response. Try rephrasing."
        return answer
    except:
        return "I need to set up my brain first. Run: 'pip install llm && llm install llm-phi3'"

def handle(cmd):
    if "time" in cmd:
        get_time()
    elif "play music" in cmd or "play song" in cmd:
        play_music()
    elif "stop music" in cmd:
        pygame.mixer.music.stop()
        speak("Music stopped.")
    elif "open youtube" in cmd:
        query = cmd.replace("open youtube", "").strip()
        if query:
            open_youtube(query)
        else:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube homepage.")
    elif any(kw in cmd for kw in ["code", "coding", "python", "error", "how to write", "debug"]):
        speak("Thinking...")
        answer = ask_local_ai(cmd)
        speak(answer)
    elif any(kw in cmd for kw in ["what is", "how to", "why", "tell me", "search", "who is"]):
        search_google(cmd)
    elif "bye" in cmd or "exit" in cmd:
        speak("See you later!")
        return False
    else:
        speak("Say 'code how to read a file' or 'open youtube cats' — I'm all ears!")
    return True

def main():
    speak("Hey! I'm Zin. Ask me to play music, open YouTube, or help with code — all private and free!")
    while True:
        if not handle(listen()):
            break

if __name__ == "__main__":
    main()
#Author: G.Rithvik Nag
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import websites
import requests
from gtts import gTTS
import pygame
from openai import OpenAI
import os
import threading
from datetime import datetime
import openai

# Setting up audio receiver and output
recognizer = sr.Recognizer()
engine = pyttsx3.init()
# Adding newsapi allows the bot to know the latest news
newsapi = "Enter Your NewsAPI key bro!!"

# Constants for commands
COMMAND_OPEN = "open"
COMMAND_TIME = "what is time now"
COMMAND_PLAY = "play"
COMMAND_NEWS = "say news"
COMMAND_END = "exit"

# Setting the voice of assistant
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload() 
    os.remove("temp.mp3")      

# If the command is out of the pre-defined instructions, let AI process the command
def aiprocess(command):
    client = OpenAI(api_key=os.getenv("Paste your OpenAI key...."))  # Use environment variable for API key
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named alexa who works as siri and googlecloud"},
            {"role": "user", "content": command}
        ]
    )
    
    return completion.choices[0].message.content

# Command processing functions
def process_open_command(site):
    weblink = websites.browselinks.get(site)
    if weblink:
        speak(f"Opening {site}")
        webbrowser.open(weblink)

def process_time_command():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The time right now is {current_times}")

def process_play_command(song):
    link = musicLibrary.music.get(song)
    if link:
        speak(f"Playing {song}")
        webbrowser.open(link)
    else:
        speak(f"Sorry, I couldn't find the song {song} in the Library")

def process_news_command():
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get("articles", [])
        for article in articles:
            speak(article['title'])  

def processCommand(command):  
    command_lower = command.lower()
    if command_lower.startswith(COMMAND_OPEN):
        parts = command_lower.split(" ", 1)
        if len(parts) > 1:
            site = parts[1]
            process_open_command(site)
        else:
            speak("Please specify a site to open.")
    elif COMMAND_TIME in command_lower:
        process_time_command()
    elif command_lower.startswith(COMMAND_PLAY): 
        parts = command_lower.split(" ", 1)
        if len(parts) > 1:
            song = parts[1]
            process_play_command(song)
        else:
            speak("Please specify a song to play.")
    elif COMMAND_NEWS in command_lower:
        process_news_command()
    elif COMMAND_END in command_lower:
        speak("peace")
        exit()
    else:
        output = aiprocess(command)
        speak(output)

if __name__ == "__main__":
    speak("Launching Alexa")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)  # type: ignore[attr-defined]
                if word and word.lower() == "alexa":
                    speak("Yes Boss")
                    with sr.Microphone() as source:
                        print("Activated, listening for command...")
                        audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                        command = recognizer.recognize_google(audio)  # type: ignore[attr-defined]
                        if command:
                            print(f"Recognized command: {command}")
                            processCommand(command)
                        else:
                            print("No command recognized.")

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")    
#Enjoy....
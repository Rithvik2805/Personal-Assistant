import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
from openai import OpenAI
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
#Search fo "news api" in browser and create an account in it then it generates an api key for you
newsapi = "enter your news api key"

def speak(text):
    engine.say(text) 
    engine.runAndWait()

def speak(text):
   tts=gTTS(text)
   tts.save('temp.mp3')

   # Initialize Pygame
   pygame.init()

   # Initialize the mixer module
   pygame.mixer.init()

   # Load the MP3 file
   pygame.mixer.music.load('temp.mp3')

   # Play the loaded MP3 file
   pygame.mixer.music.play()

   # Wait for the music to finish playing
   while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
   pygame.mixer.music.unload() 
   os.remove("temp.mp3")      

def aiprocess(text):

    client = OpenAI(
        api_key="Enter Your API Key"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a virtual assistant named friday skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": command}
    ]
    )
    
    return completion.choices[0].message.content   

def processCommand(c):
   if "open google" in c.lower():
      speak("opening google")
      webbrowser.open("https://www.google.co.in/")
   elif "open facebook" in c.lower():   
      speak("opening facebook")
      webbrowser.open("https://facebook.com") 
   elif "open watsapp" in c.lower():
      speak("opening watsapp")
      webbrowser.open("https://web.whatsapp.com")   
   elif "open youtube" in c.lower():
      speak("opening youtube")
      webbrowser.open("https://youtube.com")     
   elif c.lower().startswith("play"): 
      song = c.lower().split(" ")[1] 
      link = musicLibrary.music[song]
      if True :
         #speaks only if the song is available in the musicLibrary
         speak("playing")
      webbrowser.open(link)
       
   elif "news" in c.lower():
      r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
      if r.status_code == 200:
    # Parse the JSON response
       data = r.json()
    # Extract the articles
       articles = data.get("articles", [])
    
    # Read the headlines
      for article in articles:
        speak(article['title'])
   else:
      # let openai handle the request
          output = aiprocess(c)
          speak(output)
      


if __name__ == "__main__":
    speak("Launching Friday")
    while True:
     #Listen for the wake work Jarvis
     #obtain audio from the microphone
     r = sr.Recognizer()

     print("recognizing...")
     try:
        with sr.Microphone() as source:
          print("Listening...")
          audio = r.listen(source,timeout=2,phrase_time_limit=1)
        word = r.recognize_google(audio)
        if(word.lower() =="friday"):
           speak("Yes Boss")
           #Listen for command
           with sr.Microphone() as source:
            print("Activated...")
            audio = r.listen(source)
            command = r.recognize_google(audio)

            processCommand(command)


     except Exception as e:
        print("Error; {0}".format(e))      
       




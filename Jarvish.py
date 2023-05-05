import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
from ecapture import ecapture as ec
import requests
import smtplib
import random

# Setting up a speech engine

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# function to greet the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
        print("Good Afternoon!")   

    else:
        speak("Good Evening!")  
        print("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")       


# function to recieve input from the microphone
def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    
    return query


# to send an email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


# The main driving function
if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            music_dir = 'D:\\Jarvish\\Playlist'
            songs = os.listdir(music_dir)   
            os.startfile(os.path.join(music_dir, songs[random.randint(0, len(songs))]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = 'C:\\Users\\javed\\AppData\\Local\\Programs\\Microsoft VS Code\\Cde.exe'
            os.startfile(codePath)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "harryyourEmail@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")    
        
        elif 'news' in query:
            new = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, Happy reading')
            time.sleep(6)

        elif "camera" in query or 'take a photo' in query:
            l = len(os.listdir("myClicks"))
            ec.capture(0, "robo camera", f'myClicks\\img{l}.jpg')

        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            time.sleep(5)

        elif "weather" in query:
            response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=31.2560&longitude=75.7051&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m#')

            p = response.json()
            cur_weather = p['current_weather']
            temp =  cur_weather['temperature']
            windspeed = cur_weather['windspeed']
            winddirection = cur_weather['winddirection']
            weathercode = cur_weather['weathercode']
            is_day = cur_weather['is_day']
            cur_time = cur_weather["time"]
            cur_index = p['hourly']['time'].index(cur_time)

            speak(f"Temperature in Celcius unit is {str(temp)} \n  humidity in percentage is {str(p['hourly']['relativehumidity_2m'][cur_index])}\n and the windspeed is {str(cur_weather['windspeed'])}" )
            

            
        elif 'ruko' in query or 'ok bye' in query or 'good bye' in query or 'stop' in query or 'bye' in query:
            exit()

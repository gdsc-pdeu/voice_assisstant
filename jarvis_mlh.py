import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognition
import datetime
import wikipedia #pip install wikipedia
import smtplib
import webbrowser as wb
import os
import requests
import pyautogui #pip install pyautogui
import psutil #pip install psutil
import pyjokes #pip install pyjokes #Using pyjokes is another way to say jokes. Here we have just used an api
import vlc 
import pafy 
from googlesearch import search 
from twilio.rest import Client

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
newVoiceRate=190
def speak(audio_text):
    engine.say(audio_text)
    engine.runAndWait()


def set_whichvoice(audio_text):
    for i in range(3):
        #voice=engine.getProperty('voices')
        engine.setProperty('voice',voices[i].id)
        speak(audio_text)

def set_VoiceRate(n):
    #default is 200
    newVoiceRate=n
    engine.setProperty('rate',newVoiceRate)

def time():
    Time=datetime.datetime.now().strftime("%H:%M:%S")
    speak(Time)

def date():
    Date=datetime.datetime.now().strftime("%Y-%m-%d") #We can also do this as year=int(datetime.datetime.now().year), and same with others and print them individually
    speak("Current date is")
    speak(Date)

def wishme():
    hour=datetime.datetime.now().hour
       
    speak("Any thing else?")
    
    
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=0.5
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio)
        print(query)
    except  Exception as e:
        print(e)
        speak("What?")

        return None
    return query

def sendmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("test@gmail.com","123test")
    server.sendmail("test@gmail.com",to,content)
    server.close()

if __name__ == "__main__":

    wishme()
    while True:
        take_command=takeCommand()
        if take_command==None:
            continue
        query=take_command.lower().split()
        print(query)
        print(type(query))
        if "time" in query:
            time()

        elif "date" in query:
            date()
        elif "wiki" in query:
            wiki_search_text=""
            wiki_start=0
            for i in query:
                wiki_start+=1
                if i=="wiki":
                    for j in range(wiki_start,len(query)):
                        wiki_search_text+=query[j]
                    break;
            
            speak("Searching ...")
            result=wikipedia.summary(wiki_search_text,sentences=2)
            speak(result)
            print(query[wiki_start:])
        

        elif "mail" in query:
            try:
                speak("What are the contents of the mail?")
                content=take_command()

                to="xyz@gmail.com"
                sendmail(to,content)
                speak("Khat mene daal diya")
            except Exception as e:
                speak("Unable to send the mail")
                print(e)

        elif "chrome" in query:
            speak("What link do you want me to open?")
            chromepath="C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            while(True):
                take_command=takeCommand()
                if take_command==None:
                    continue
                break
            search=take_command.lower()
            if search[-3:]!='com':
                search+=".com"
            wb.get(chromepath).open_new_tab(search)
            continue
        elif "logout" in query:
            pass
            #os.system("shutdown - l")
        elif "shutdown" in query:
            pass
            #os.system("shutdown /s /t 1")

        elif "restart" in query:
            pass
            #os.system("shutdown /r /t 1")
        
        elif "songs" in query:
            pass
            # songs_dir="F:\musics\music"

            # songs=os.listdir(songs_dir)
            # os.startfile(os.path.join(songs_dir,songs[0]))

        elif "remember" in query or "write" in query:
            speak("What do you want me to remember?")
            while(True):
                take_command=takeCommand()
                if take_command==None:
                    continue
                break
            text_to_remember=take_command.lower()
            with open("remember.txt","a+") as f:
                f.write(text_to_remember)

        elif "remembered" in query or "read" in query or ("open" in query and "diary" in query):
            with open("remember.txt","r") as f:
                speak(f.read())
        elif "empty" in query or ("diary" in query and "clear" in query):
            print("Clearing")
            with open("remember.txt","w") as f:
                print("Clear")
                speak("Emptied")
            continue
        
        elif "screenshot" in query or ("capture" in query and "screen" in query):
            img=pyautogui.screenshot()
            img.save("ss.png")
            speak("Done")
        
        elif ("machine" in query or "cpu" in query) and ("report" in query or "status" in query):
            usage=str(psutil.cpu_percent())
            speak("CPU is at" + usage)

            battery=psutil.sensors_battery()
            speak("Battery is "+battery.percent)

            
        elif "joke" in query or "jokes" in query:
            url="https://v2.jokeapi.dev/joke/Programming?format=txt"
            a=requests.get(url)
            print(a.text)
            print(type(a.text))
            speak(a.text)
            pass

        elif "tata" in query:
            speak("Goodnight")
            quit()
            
        elif "weather" in query:
            response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=170186c6c1db43f1854d9690835e0778")
            print(response.status_code)
            city=response.json()['city']
            respons=requests.get("http://api.openweathermap.org/data/2.5/weather?appid=351861fb0a871db7957069e9ae033277&q="+"Vadodara")
            weather_details=respons.json()
            speak("Temperature in " +city + " is " + str(weather_details["main"]["temp"])+" Kelvin, with "+str(weather_details["main"]["pressure"])+" hPascals")

        elif "news" in query:
            country = "in"
            query_news = "idea"
            response = requests.get("https://newsapi.org/v2/top-headlines?country="+ country +"&q="+ query_news +"&apiKey=4a733a4e0a2846acbe7ec32d8d1e2761")
            speak(response.title)
            pass

        elif "youtube" in query:
            j=list()
    
            for i in search(query, tld="co.in", num=10, stop=10, pause=2): 
                j.append(i)
            a=j[0]
                #Playing video
            url = a
            video = pafy.new(url)  
            best = video.streams[0]    
            media = vlc.MediaPlayer(best.url) 
            media.play()
        
        elif "sms" in query or "message" in query:
            try:
                client = Client("ACe2ef31a4d09f9846afcd486586495973", "8d2e36f767db9c4948d5ad81a03e933d")
                speak("What are the contents of the sms?")
                content=take_command()
                
                speak("State the name of the recipient")
                name=take_command()
                
                speak("State the number of the recipient")
                mobile=take_command()
                number="+91"+str(mobile)

                client.messages.create(to=number, 
                                        from_="+13092711496", 
                                        body=(content))
                speak("Khat mene daal diya")
            except Exception as e:
                speak("Unable to send the sms")
                print(e)



        else:
            speak("I didn't get you. Say that again")
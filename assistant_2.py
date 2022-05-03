import urllib.request
import pyttsx3
import sys
import speech_recognition as sr
import pandas as pd
import wikipedia
import webbrowser
import os
import time
import colorama
from colorama import Fore
from plyer import notification

colorama.init(autoreset=True)

#Speaking System
def speak(text):
    x=pyttsx3.init()
    voices=x.getProperty('voices')
    x.setProperty('rate',130)
    x.setProperty('voice', voices[2].id)
    x.runAndWait()

    x.say(text)
    x.runAndWait()

#Checking Internet connection
def connect(host='http://google.com'):
    print (Fore.BLUE+'Checking Internet connection. Please Wait...')
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
if connect():
    print(Fore.GREEN+'Connected')
else:
    print(Fore.RED+'No Internet! Please try again later.')
    speak('No Internet! Please try again later.')
    sys.exit()

#enter data in database
def newData(Question, Answer):
    df = pd.DataFrame({'Question': [Question],
                   'Answer': [Answer]})
    df.to_csv('Data.csv',mode='a', index=False, header=False)

#answer not found
def noAnswer(topic):
    print(Fore.BLUE+'searching on wikipedia...')
    try:
        result = (wikipedia.summary(topic, 2))
        cleanresult = result.replace("\\","")
        webbrowser.open("https://www.google.com/search?q="+topic)
        print(cleanresult)
        newData(topic,cleanresult)
        speak(cleanresult)
    except Exception:
        print('Unable to find answer for '+ topic+' !')
        speak('Unable to find answer for'+ topic)

#excel file processing
def getAnswer(Question):
    df = pd.read_csv('Data.csv')
    answer = pd.DataFrame(df,columns=['Answer'])[df.Question.str.contains(Question,case=True)]
    anslist = answer.values.tolist()
    aListLen = len(anslist)
    if aListLen == 0:
        noAnswer(Question)
    else:
        print(anslist)
        speak(anslist)
        
def notify(t,m):
    notification.notify(
    title = t,
    message = m,
    app_icon = None,
    timeout = 5,
)
#Listening and responce system
def command():
    print (Fore.BLUE+'Setting all things ready...')
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print ("lisning...")
        r.pause_threshold=0.6
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
        print("recognising...")
    try:
        speech=r.recognize_google(audio,language='en-us')
        lowerspeech = speech.lower()
        print(Fore.GREEN+f"you said:{lowerspeech}")
        # functions
        if "open youtube" in lowerspeech:
            webbrowser.open("https://youtube.com")
        elif "youtube" in lowerspeech:
            search = lowerspeech.replace('youtube','')
            webbrowser.open("https://www.youtube.com/results?search_query="+search)
        elif "open google" in lowerspeech:
            webbrowser.open("https://google.com")
        elif "open browser" in lowerspeech:
            webbrowser.open()
        elif "open whatsapp" in lowerspeech:
            webbrowser.open("https://web.whatsapp.com")
        elif "open aics" in lowerspeech:
            webbrowser.open("https://aistudent.community")
        elif "open cmd" in lowerspeech:
            os.system("start cmd")
        elif "close browser" in lowerspeech or "close web browser" in lowerspeech :
            os.system("taskkill /im msedge.exe /f")
            notify('Browser closed','Browser has been closed succesfully')
        elif lowerspeech == ("tell me the time"):
                print(time.asctime(time.localtime(time.time())))
                speak(time.asctime(time.localtime(time.time())))
        else:
            getAnswer(lowerspeech)
    except Exception:
        print(Fore.RED+"sorry! unable to recognise, say that again...")
while True:
    command()

import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import  Gesture_Controller
import  Function
import  app
import threading 

today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

file_exp_status = False
files =[]
path = ''
is_awake = True  

def reply(audio):
    if audio:
        app.ChatBot.addAppMsg(audio)
        print(audio)
        engine.say(audio)
        engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Exlaw, how may I help you?")

with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

def record_audio():
    print("Talk")
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data=""
        audio = r.listen(source, phrase_time_limit=5)
        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
        return voice_data.lower()

def open_web(url, voice_data, keyword):
    query = voice_data.split(keyword)[1]
    try:
        webbrowser.get().open(url.format(query))
        reply('This is what I found Sir.')
    except:
        reply('Please check your Internet')

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('exlaw','')
    if voice_data:
        app.eel.addUserMsg(voice_data)

    url_commands = {
        'search': 'https://google.com/search?q={}',
        'play spotify': 'https://open.spotify.com/{}',
        'w3school': 'https://www.w3schools.com/{}',
        'learn python': 'https://www.learnpython.org/{}',
        'whatsapp': 'https://web.whatsapp.com/{}',
        'instagram': 'https://www.instagram.com/{}',
        'twitter': 'https://twitter.com/i/flow/login{}',
        'gmail': 'https://accounts.google.com/v3/{}',
        'weather': 'https://weather.com/en-IN{}',
        'kit': 'https://kitcbe.com/{}',
        'swiggy': 'https://www.swiggy.com/{}',
        'amazon': 'https://www.amazon.in/{}',
        'netflix': 'https://www.netflix.com/in/{}',
    }

    if not is_awake and 'wake up' in voice_data:
        is_awake = True
    elif 'hello' in voice_data:
        wish()
    elif 'what is your name' in voice_data:
        reply('My name is Exlaw!')
    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))
    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])
    elif any(command in voice_data for command in url_commands.keys()):
        for command, url in url_commands.items():
            if command in voice_data:
                open_web(url, voice_data, command)
                break
    # Handle other commands as before...
    # ...


            
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')  
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            event =threading.Event()
            t =threading.Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')
            event.set()

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')

    elif 'hand sign' in voice_data:
        import Exlaw_cursor.src.Main as Main
        if Main.Function.vd_mode:
            reply('Hand sign is already active')
        else:
            voice_data = Main.Function()
            event = threading.Event()
            t =threading.Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')
            event.set()

    elif ('stop hand sign' in voice_data) or ('top hand sign' in voice_data):
        if Main.Function.vd_mode:
           Main.Function.vd_mode = 0
           reply('Hand sign stopped')
        else:
            reply('Hand sign is already inactive')
   
  
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   


event =threading.Event()
t1 = threading.Thread(target = app.ChatBot.start )
t1.start()


while not app.ChatBot.started:
    time.sleep(0.01)

wish()
voice_data = None
while True:
    if app.ChatBot.userinputQueue.empty() ==False:
        voice_data = app.ChatBot.popUserInput()
    else: 
     voice_data = record_audio()
     print("Comes Again")
    if 'exlaw' in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            print("EXCEPTION raised while closing.") 
            event.set()
            break     

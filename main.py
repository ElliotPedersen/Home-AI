import os
from datetime import datetime

import pyttsx3 as pyttsx3
import requests
import speech_recognition as sr
import subprocess

weather_api_key = 'WEATHER_API_KEY'
news_api_key = 'NEWS_API_KEY'

volume = 0
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"


def assistant_speaks(inputObject):
    global volume

    volume = 0.25
    voice = pyttsx3.init(driverName='sapi5')

    print("Arthur: ", inputObject)

    voice.setProperty('rate', 150)
    voice.setProperty('volume', volume)
    voice.setProperty('voice', voice_id)

    voice.say(inputObject)

    voice.runAndWait()


def get_audio():
    rObject = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        audio = rObject.listen(source=source, phrase_time_limit=2.5)

    try:

        textObject = rObject.recognize_google(audio, language='en-US')
        print("You: ", textObject)
        return textObject

    except:
        return 'a'


def close_application(inputObject):
    if 'chrome' in inputObject:
        assistant_speaks("Closing Google Chrome")
        os.system("TASKKILL /F /IM chrome.exe")
        return

    if 'discord' in inputObject:
        assistant_speaks("Closing Discord")
        os.system("TASKKILL /F /IM discord.exe")
        return

    elif 'steam' in inputObject:
        assistant_speaks("Closing Steam")
        os.system("TASKKILL /F /IM steam.exe")
        return

    elif 'minecraft' in inputObject:
        assistant_speaks("Closing Minecraft")
        os.system("TASKKILL /F /IM minecraftlauncher.exe")
        return


    elif 'spotify' in inputObject:
        assistant_speaks("Closing Spotify")
        os.system("TASKKILL /F /IM spotify.exe")
        return

    elif 'cs' or "counter strike" in inputObject:
        assistant_speaks("Closing Counter Strike: Global Offensive")
        os.system("TASKKILL /F /IM csgo.exe")
        return

    else:
        assistant_speaks("Application not available")
        return


def open_application(inputObject):
    if 'chrome' in inputObject:
        assistant_speaks("Opening Google Chrome")
        os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
        return

    elif 'discord' in inputObject:
        assistant_speaks("Opening Discord")
        subprocess.call(r"C:\Users\ellio\AppData\Local\Discord\Update.exe --processStart Discord.exe")
        return

    elif 'steam' in inputObject:
        assistant_speaks("Opening Steam")
        os.startfile("D:\Steam\steam.exe")
        return

    elif 'minecraft' in inputObject:
        assistant_speaks("Opening Minecraft")
        os.startfile("D:\Minecraft\MinecraftLauncher.exe")
        return

    elif 'spotify' in inputObject:
        assistant_speaks("Opening Spotify")
        os.startfile("C:/Users/ellio/AppData/Roaming/Spotify/Spotify.exe")
        return

    elif 'cs' or "counter strike" in inputObject:
        assistant_speaks("Opening Counter Strike: Global Offensive")
        subprocess.call(r"D:\Steam\steam.exe -applaunch 730")
        return

    else:
        assistant_speaks("Application not available")
        return


def computer_operation(inputObject):
    if "log off" in inputObject or "log out" in inputObject:
        assistant_speaks("Are you sure?")

        ans = get_audio()

        if 'yes' in str(ans) or 'yeah' in str(ans):
            assistant_speaks("Ok bye.")
            os.startfile("logoff.bat")
            return

    elif "restart" in inputObject or "reboot" in inputObject or "restart computer" in inputObject or "reboot computer" in inputObject:
        assistant_speaks("Are you sure?")

        ans = get_audio()

        if 'yes' in str(ans) or 'yeah' in str(ans):
            assistant_speaks("Ok bye.")
            os.startfile("restart.bat")
            return

    elif "shut down computer" in inputObject or "shut down" in inputObject or "turn off" in inputObject or "turn off computer" in inputObject:
        assistant_speaks("Are you sure?")

        ans = get_audio()

        if 'yes' in str(ans) or 'yeah' in str(ans):
            assistant_speaks("Ok bye.")
            os.startfile("shutdown.bat")
            return


def get_datetime(inputObject):
    if 'date' in inputObject:
        today = datetime.today()
        date = today.strftime("%B %d, %y")
        assistant_speaks(date)

    elif 'time' in inputObject:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        assistant_speaks(current_time)


def get_weather(inputObject):
    base_weather_url = "http://api.openweathermap.org/data/2.5/weather?"

    index = inputObject.split().index('in')
    query = inputObject.split()[index + 1:]

    city = query[0]

    complete_weather_url = base_weather_url + "appid=" + weather_api_key + "&q=" + city

    response = requests.get(complete_weather_url)

    x = response.json()

    if x["cod"] != "404":

        y = x["main"]
        current_temperature = round(y["temp"] - 273.15)
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        assistant_speaks("The temperature is about " + str(current_temperature) + " degrees celsius" +
                         ", The humidity level is at " + str(current_humidity) + " percent" +
                         ", I would describe the weather as " + str(weather_description) + '.')

    else:
        assistant_speaks("City Not Found")


def get_news():
    query_params = {
        "source": "bbc-news",
        "sortBy": "top",
        "apiKey": news_api_key
    }

    main_url = " https://newsapi.org/v1/articles"

    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()

    article = open_bbc_page["articles"]

    results = []

    for ar in article:
        results.append(ar["title"])

    assistant_speaks(results)


def process_text(inputObject):
    try:
        if 'close' in inputObject:
            close_application(inputObject.lower())
            return

        elif 'open' in inputObject:
            open_application(inputObject.lower())
            return

        elif ("log off" in inputObject or "log out" in inputObject or "restart" in inputObject or "reboot" in
              inputObject or "restart computer" in inputObject or "reboot computer" in inputObject or
              "shut down computer" in inputObject or "shut down" in inputObject or "turn off" in inputObject or
              "turn off computer" in inputObject):

            computer_operation(inputObject.lower())
            return

        elif 'date' in inputObject or 'time' in inputObject:
            get_datetime(inputObject.lower())
            return

        elif 'weather' in inputObject:
            get_weather(inputObject.lower())
            return

        elif 'news' in inputObject:
            get_news()
            return

        elif 'thanks' in inputObject:
            assistant_speaks("No problem")
            return

        else:
            return

    except:
        assistant_speaks("I don't understand.")


while 1:
    text = get_audio()

    if text == 'a':
        continue

    if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text) or "end" in str(text) or "stop" in str(
            text) or "quit" in str(text):
        break

    process_text(text)

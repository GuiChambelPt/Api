
from flask import Flask
import random
import requests
import wikipedia
import os
from googletrans import Translator
from dotenv import load_dotenv
from config import *
app = Flask(__name__)
load_dotenv()
WEATHERAPIKEY = os.getenv("WEATHERAPIKEY")
def kelvintocelcius(temp):
    temp = temp - 273.15
    temp = round(temp, 1)
    return temp
    

@app.route('/',  methods=['GET'])
def barras():
    barra = random.choice(Barra)
    print(barra)
    return {"Barra": barra}

@app.route('/translator/&src=<string:srclanguage>&d=<string:destinationlanguage>&p=<string:pharse>', methods=['GET'])
def translator(srclanguage,destinationlanguage,pharse):
    translator = Translator()
    translate_channel = translator.translate(pharse, src=srclanguage, dest=destinationlanguage)
    translate_text = translate_channel.text
    return {"Translate_text": translate_text}

    
@app.route('/curiosidades/',  methods=['GET'])
def curiosidades():
    curiosidade = random.choice(Curiosidade)
    print(curiosidade)
    return {"Curiosidades": curiosidade, "Tipo": "N/A"}

@app.route('/weather/&c=<string:city>', methods=['GET'])
def weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    Key = WEATHERAPIKEY
    lang = 'pt'
    complete_url = base_url + "appid=" + Key + "&q=" + city + "&lang=" + lang
    print(complete_url)
    x = requests.get(url=complete_url)
    weather = x.json()
    print(weather)
    error = weather["cod"]
    if error == '404':
        return {'message': 'city not found', 'error': '404'}
    else:
        weathermain = weather["weather"]
        for i in weathermain:
            mainweather = i
        description = mainweather["description"]
        name = weather["name"]
        main = weather["main"]
        temp = main["temp"]
        temp_max = main["temp_max"]
        temp_min = main["temp_min"]
        temp_max = kelvintocelcius(temp_max)
        temp_min = kelvintocelcius(temp_min)
        temp = kelvintocelcius(temp)
        return {"name": name, "Temp":temp, "Temp_max": temp_max, "Temp_min": temp_min, "WeatherDescription": description}
@app.route('/wikipedia/&lang=<string:lang>&s=<string:tosearch>')
def Wikipedia(tosearch, lang):
    wikipedia.set_lang(lang)
    result = wikipedia.summary(tosearch, sentences=2)
    return {"Summary": result, "Lang": lang}

def iniciar():
    print("Iniciado Api")
    app.run(port="1111")

if  __name__ == "__main__":
    iniciar()
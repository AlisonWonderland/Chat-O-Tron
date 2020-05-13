import webbrowser
import socket
import requests
from spellchecker import SpellChecker
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Got to make sure websites are spell corrected
# def initSpellchecker():



def openWebsite(website):
    webbrowser.open('https://' + website + '.com/', new=0)

def getWeather():
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}

    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()

    weather_request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={geo_data["latitude"]}&lon={geo_data["longitude"]}&units=imperial&appid=6620fb18917ffa433db64ebf83cde131').json()
    city = weather_request["name"]
    maxTemp = weather_request["main"]["temp_max"]
    weatherDescription = weather_request["weather"][0]["description"]
    response = "In " + city + " the high is " + str(maxTemp) + " degrees. With " + weatherDescription + "."
    return response
    

def spellcheck(str):
    spell = SpellChecker()
    strWordList = str.split()

    for i in range(len(strWordList)):
        word = strWordList[i]
        if spell.unknown([word]):
            strWordList[i] = spell.correction(word)
    
    str = " ".join(strWordList)
    return str

def sentimentAnalysis(str):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(str)

    if(ss["compound"] > 0.5):
        return "Also, why are you so positive about that?\n"
    elif(ss["compound"] < -0.5):
        return "Also, why are you so negative about that?\n"
    else:
        return ""
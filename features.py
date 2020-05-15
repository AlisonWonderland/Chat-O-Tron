import webbrowser
import socket
import requests
import random
import config
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

    weather_request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={geo_data["latitude"]}&lon={geo_data["longitude"]}&units=imperial&appid={config.weather_api_key}').json()
    city = weather_request["name"]
    max_temp = weather_request["main"]["temp_max"]
    weather_description = weather_request["weather"][0]["description"]
    response = "In " + city + " the high is " + str(max_temp) + " degrees. With " + weather_description + "."
    return response

def getNews():
    news_request = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={config.news_api_key}').json()
    num_articles = len(news_request["articles"])
    
    article_num = random.randint(0, num_articles - 1)
    article = news_request["articles"][article_num]
    
    print("Talking about the news huh. Here have some news.")
    print("Title:", article["title"])
    print("CONTENT:")
    print(article["content"])


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
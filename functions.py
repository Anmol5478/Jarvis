import os
import webbrowser
import datetime
import requests
import google.generativeai as genai
import pywhatkit
import speech_recognition as sr
from database import save_chat

# ✅ Configure Gemini API
API_KEY_GEMINI = "AIzaSyCTrqVoIwRcQ0vf1j7d_ioQYawRWxDf_xc"
genai.configure(api_key=API_KEY_GEMINI)

chatStr = ""  # Stores conversation history


def chat(query):
    """Handles AI chat responses using Gemini API"""
    global chatStr
    model = genai.GenerativeModel("gemini-2.0-flash")
    chatStr += f"User: {query}\nJarvis: "

    response = model.generate_content(chatStr)

    if response and hasattr(response, "candidates"):
        generated_text = response.candidates[0].content.parts[0].text.strip()
        print("Jarvis:", generated_text)

        # ✅ Save chat to database
        save_chat(query, generated_text)

        return generated_text
    else:
        return "I couldn't understand that. Could you please repeat?"


# ✅ Weather API
API_KEY_WEATHER = "1a6ed565e7f34774b7253406250104"
BASE_URL_WEATHER = "http://api.weatherapi.com/v1/current.json"


def get_weather(city):
    """Fetches current weather data for a given city"""
    url = f"{BASE_URL_WEATHER}?key={API_KEY_WEATHER}&q={city}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # ✅ Raise error if request fails
        data = response.json()

        if "current" not in data:
            return "I couldn't fetch the weather data. Please try again."

        condition = data['current']['condition']['text']
        temp = data['current']['temp_c']
        feels_like = data['current']['feelslike_c']
        humidity = data['current']['humidity']

        weather_report = (f"The weather in {city} is {condition}. "
                          f"The temperature is {temp}°C, feels like {feels_like}°C, "
                          f"with a humidity of {humidity}%.")
        return weather_report

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"


# ✅ News API
NEWS_API_KEY = "pub_7738401d559e784cafeeee25b39239548329f"
NEWS_BASE_URL = "https://newsdata.io/api/1/news"


def get_news(topic=None, country="us"):
    """Fetches latest news headlines. If no topic is given, fetches general current affairs."""
    url = f"{NEWS_BASE_URL}?apikey={NEWS_API_KEY}&country={country}"
    if topic:
        url += f"&q={topic}"  # Add topic if provided

    try:
        response = requests.get(url)
        response.raise_for_status()  # ✅ Raise error if request fails
        data = response.json()

        articles = data.get("results", [])
        if not articles:
            return "No relevant news found."

        news_report = "Here are the latest news updates: \n"
        for article in articles[:3]:  # ✅ Limit to top 3 news
            title = article.get('title', 'No title available')
            news_report += f"📰 {title}\n"

        return news_report

    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"


def say(text):
    """Speaks the given text, truncating long messages"""
    max_length = 500  # ✅ Truncate if text is too long
    if len(text) > max_length:
        text = text[:max_length] + "..."

    os.system(f'say "{text}"')


def takeCommand():
    """Continuously listens for 'Jarvis' wake word and processes commands"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("Listening for 'Jarvis'...")

        while True:
            try:
                audio = r.listen(source, phrase_time_limit=5)  # ✅ Limit max listen time
                query = r.recognize_google(audio, language="en-in").lower()
                print(f"User: {query}")

                if "jarvis" in query:
                    query = query.replace("jarvis", "").strip()
                    say(f"Yes, sir. {query}")
                    return query  # ✅ Return cleaned command

            except sr.UnknownValueError:
                continue  # Ignore and keep listening
            except sr.RequestError:
                print("Jarvis: Network error. Please check your internet connection.")
                say("Network error. Please check your internet connection.")
                return None  # Skip execution if network issue

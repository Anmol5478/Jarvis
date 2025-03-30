import speech_recognition as sr
import os
import webbrowser
import datetime
import google.generativeai as genai
import re
from All import sites, apps
import pywhatkit





chatStr = ""
# Configure Gemini API
API_KEY = "AIzaSyCTrqVoIwRcQ0vf1j7d_ioQYawRWxDf_xc"  # Replace with your actual API key
genai.configure(api_key=API_KEY)


def chat(query):
    global chatStr

    model = genai.GenerativeModel("gemini-2.0-flash")

    # Ensure model name is correct
    chatStr += f"Anmol: {query} \n"
    response = model.generate_content(chatStr)

    if response and hasattr(response, "text"):
        generated_text = response.text.strip()  # Clean response
        print("Jarvis:", generated_text)
        say(generated_text)  # Speak the AI response
        return generated_text
    else:
        print("Error: No text generated")
        return "I couldn't understand that. Could you please repeat?"

    # Create directory if not exists
    if not os.path.exists("gemini"):
        os.mkdir("gemini")

    # Generate a valid filename from the prompt
    safe_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', query)  # Remove special characters
    safe_prompt = "_".join(safe_prompt.split())[:50]  # Limit length and replace spaces

    filename = f"gemini/{safe_prompt}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(generated_text)
    except Exception as e:
        print(f"Error saving file: {e}")


def ai(prompt):
    """Generates AI response using Google Gemini and saves it to a file"""

    model = genai.GenerativeModel("gemini-1.5-pro")  # Ensure model name is correct
    response = model.generate_content(prompt)

    if response and hasattr(response, "text"):
        generated_text = response.text.strip()  # Clean response
        print(generated_text)
    else:
        print("Error: No text generated")
        return "I couldn't understand that. Could you please repeat?"

    # Create directory if not exists
    if not os.path.exists("gemini"):
        os.mkdir("gemini")

    # Generate a valid filename from the prompt
    safe_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)  # Remove special characters
    safe_prompt = "_".join(safe_prompt.split())[:50]  # Limit length and replace spaces

    filename = f"gemini/{safe_prompt}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(generated_text)
    except Exception as e:
        print(f"Error saving file: {e}")

    return generated_text  # Return only the AI response


def say(text):
    """Speaks the given text, truncating long messages"""
    max_length = 500  # Adjust as needed
    if len(text) > max_length:
        text = text[:max_length] + "..."
    os.system(f'say "{text}"')


def takeCommand():
    """Captures voice command from the microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"Anmol: {query}")
            return query.lower()
        except Exception:
            return "Some error occurred, sorry from Jarvis."


if __name__ == "__main__":
    print("Jarvis AI Initialized")
    say("Hello, I am Jarvis A.I.")

    while True:
        query = takeCommand()

        # Open Webpages
        # sites = {
        #     "youtube": "https://youtube.com",
        #     "linkedin": "https://linkedin.com",
        #     "google": "https://google.com",
        #     "instagram": "https://instagram.com"
        # }

        for site in sites:
            if f"open {site[0].lower()}" in query:
                say(f"Opening {site[0]}, sir")
                webbrowser.open(site[1])

        # Play music
        if "play music" in query:
            music_path = "/Users/lord/Downloads/HAK.mp3"
            os.system(f'open "{music_path}"')

        # Tell the time
        if "the time" in query:
            strf_time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {strf_time}")

        # Open applications


        for app in apps:
            if f"open {app[0].lower()}" in query:
                os.system(f"open {app[1]}")

        if "play" in query and "on youtube" in query:
            song_name = query.replace("play", "").replace("on youtube", "").strip()
            say(f"Playing {song_name} on YouTube, sir")
            pywhatkit.playonyt(song_name)


        # AI-based response
        if "tell" in query or "write" in query:
            response = ai(query)
            if response:
                say(response)  # Speak only the AI-generated response
        elif "exit" in query or "quit" in query:
            say("Goodbye, sir")
            exit()
        elif "reset chat" in query:
            chatStr = ""
        else:
            chat(query)

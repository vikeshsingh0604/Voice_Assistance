import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  # Ensure this module contains a valid 'music' dictionary
import requests


# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# News API key (ensure you keep this safe and secure)

newsapi = "Yours NewsApi key"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process user commands
def processCommand(c):
    c = c.lower()  # Normalize command to lowercase
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
    elif "open whatsapp" in c:
        webbrowser.open("https://web.whatsapp.com/")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        try:
            Link = musicLibrary.music[song]
            webbrowser.open(Link)
        except KeyError:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:5]:  # Limit to 5 articles
                    speak(article['title'])
            else:
                speak("No news articles found.")
        else:
            speak("Sorry, I couldn't retrieve the news.")
    else:
        speak("Sorry, I didn't understand the command.")

# Main loop to handle listening and processing commands
if __name__ == "__main__":
    speak("Initializing Google Assistant...")
    
    while True:
        print("Recognizing...")
        try:
            # Listen for the wake word "Google"
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)

            # If wake word is "Google", listen for the actual command
            if word.lower() == "google":
                speak("Yes, how can I assist?")
                
                with sr.Microphone() as source:
                    print("Google is active. Listening for command...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")
                    processCommand(command)
        
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            
        except Exception as e:
            print("error; {0}".format(e)) 
           

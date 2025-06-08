import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia  
import pywhatkit    
import os
import subprocess
import webbrowser
import openai 
import requests

# ========== Setup your API Keys here ==========
openai.api_key = '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'
WEATHER_API_KEY = 'd997fe512926c1542a3b85d6b1f03c8f'

# ========== Initialize TTS engine ==========
engine = pyttsx3.init()

# ========== Memory dictionary ==========
memory = {}

# ========== Speak function ==========
def speak(text):
    print("Zara:", text)
    engine.say(text)
    engine.runAndWait()

# Get all available voices
voices = engine.getProperty('voices')

# Print available voices to find the female one
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name}, {voice.gender}, {voice.id}")

# Select a female voice (usually index 1 on Windows)
engine.setProperty('voice', voices[1].id)

# ========== Wish user ==========
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Akif!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Akif!")
    else:
        speak("Good Evening Akif!")
    speak("I am Zara, your personal assistant. How can I help you?")

# ========== Take voice command ==========
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except:
        speak("Sorry, I didn't catch that. Please say it again.")
        return "None"

# ========== ChatGPT query ==========
def ask_chatgpt(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

# ========== Weather info ==========
def get_weather(city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data.get("cod") != "404":
        main = data["main"]
        temp = main["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}."
    else:
        return "City not found."

# ========== Main assistant loop ==========
def run_zara():
    wish_me()
    while True:
        query = take_command()

        if query == "none":
            continue

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("Sorry, I could not find any results.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            pywhatkit.playonyt("YouTube")

        elif 'play music' in query:
            music_dir = "C:\\Users\\Akif\\Music"  # Change YourUsername
            try:
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
            except:
                speak("Sorry, I couldn't find music on your device.")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open chrome' in query:
            speak("Opening Google Chrome")
            subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")  # Change if needed

        elif 'open vs code' in query or 'open visual studio code' in query:
            speak("Opening Visual Studio Code")
            subprocess.Popen("C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")  # Change username

        elif 'open whatsapp' in query:
            speak("Opening WhatsApp Web")
            webbrowser.open("https://web.whatsapp.com/")

        elif 'weather' in query:
            speak("Which city weather do you want to know?")
            city = take_command()
            weather_report = get_weather(city)
            speak(weather_report)

        elif 'remember my name' in query:
            speak("What should I remember your name as?")
            name = take_command()
            memory['name'] = name
            speak(f"I will remember that your name is {name}")

        elif 'what is my name' in query:
            if 'name' in memory:
                speak(f"Your name is {memory['name']}")
            else:
                speak("I don't know your name yet.")

        elif 'remember task' in query:
            speak("What task should I remember?")
            task = take_command()
            if 'tasks' not in memory:
                memory['tasks'] = []
            memory['tasks'].append(task)
            speak("Task saved.")

        elif 'what are my tasks' in query:
            if 'tasks' in memory and memory['tasks']:
                tasks = ', '.join(memory['tasks'])
                speak(f"You have these tasks: {tasks}")
            else:
                speak("You have no tasks saved.")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye Akif! Have a great day.")
            break

        else:
            # Fallback to ChatGPT for unknown queries
            response = ask_chatgpt(query)
            speak(response)

if __name__ == "__main__":
    run_zara()

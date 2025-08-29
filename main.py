import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import wikipedia

engine=pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# greet user based on time of the day
def greet_user():
    hour=int(datetime.datetime.now().hour)
    if 0<=hour<12:
        speak("good morning mam!")
    elif 12<=hour<18:
        speak("good afternoon mam!")
    else:
        speak("good evening mam!")
    speak("I am Jarvis.How can I help you?")

#listen from microphone and convert speech to text
def listen():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source) #this reduces noise
        audio=recognizer.listen(source)

    try:
        command=recognizer.recognize_google(audio) #voice -> text
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("sorry,I could not understand")
        return ""
    except sr.RequestError:
        print("network error")
        return ""
    
def execute_command(command):
    if "time" in command:
        current_time=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"the current time is {current_time}")

    elif "google" in command:
        webbrowser.open("https://www.google.com")
        speak("opening google")

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")

    elif "wikipedia" in command:
        try:
            topic=command.replace("wikipedia","").strip()
            if topic:
                summary=wikipedia.summary(topic,sentence=2)
                speak(f"according to wikipedia, {summary}")
            else:
                speak("please tell me what to search on wikipedia")
        except Exception:
            speak("sorry, I couldn't find any result on wikipedia")

    elif "search" in command and "google" in command:
        query=command.replace("search","").replace("google","").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Here are the Google search results for {query}")
        else:
            speak("please tell us what to search on google")

    elif "play music" in command and "youtube" in command:
        webbrowser.open("https://www.youtube.com/results?search_query=music")
        speak("Playing music on YouTube")

    elif "play music" in command and "spotify" in command:
        webbrowser.open("https://open.spotify.com/")
        speak("Opening Spotify for you")

    elif "play music" in command:
        webbrowser.open("https://www.youtube.com/results?search_query=music")
        speak("Playing music online")

    # map feature
    elif "map" in command or "location" in command:
        place=command.replace("show me","").replace("on map","").replace("location of","").strip()
        if place:
            webbrowser.open(f"https://www.google.com/maps/place/{place}")
            speak(f"Here is the location of {place}")
        else:
            speak("Please tell me the location you want to see")

        # notes features
    elif "take a note" in command:
        speak("what should i write, mam?")
        note=listen()
        if note:
            with open("notes.txt","a") as f:
                f.write(note+"\n")
            speak("note saved successfully")
        elif "read my notes" in command:
            try:
                with open("notes.txt","r") as f:
                    notes=f.read()
                if notes:
                    speak("here are your notes")
                    speak(notes)
                else:
                    speak("your notes are empty")
            except FileNotFoundError:
                speak("no notes found")
        



    elif "exit" in command or "quit" in command:
        speak("Goodbye mam. Have a nice day!")
        exit()
    else:
        speak(f"You said {command}")

    
# main program
if __name__=="__main__":
    speak("Initializing Jarvis....")
    greet_user()

    #text listening
    while True:
        command=listen()
        if command:
            execute_command(command)
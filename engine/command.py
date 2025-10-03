import pyttsx3
import requests
import speech_recognition as sr
import eel
import time


def speak(text):
    text = str(text)
    engine = pyttsx3.init('nsss')
    engine.setProperty('rate', 180)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()




@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        eel.DisplayMessage("Listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print('Recognizing....')
        eel.DisplayMessage("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(3)
    except Exception:
        return ""
    return query.lower()


@eel.expose
def allCommands(message=1):
    try:
        if message == 1:
            query = takecommand()
            eel.senderText(query)
        else:
            query = message.lower().strip()
            eel.senderText(query)

        print(f"Query received: {query}")

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYouTube
            PlayYouTube(query)

        elif "send message" in query or "whatsapp" in query:
            from engine.features import findContact, sendMessageViaWeb
            speak("What message should I send?")
            msg_to_send = takecommand()

            if msg_to_send:
                contact_no, name = findContact(query)
                if contact_no:
                    sendMessageViaWeb(contact_no, msg_to_send)
                else:
                    speak("I couldn't find that contact.")
            else:
                speak("No message received.")

        elif "time" in query:
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")
            
        

        elif "date" in query:
            import datetime
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

            
        elif "temperature" in query or "weather" in query:
            
            try:
                api_key = "ee1738fb87e51f350aafc7d2730ee2f1"   # your key here

                # Check if user asked for current location
                if "now" in query or "current" in query:
                    # Get your current city using IP
                    location_url = "http://ip-api.com/json/"
                    loc_res = requests.get(location_url).json()
                    city = loc_res.get("city", None)
                else:
                    # Extract city from the query
                    words = query.split()
                    city = None
                    for i, word in enumerate(words):
                        if word.lower() == "in" and i + 1 < len(words):
                            city = " ".join(words[i+1:])
                            break

                if not city:
                    speak("Please specify a city, for example, temperature in Bangalore.")
                else:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    response = requests.get(url)
                    data = response.json()

                    if data["cod"] == 200:
                        temp = data["main"]["temp"]
                        description = data["weather"][0]["description"]
                        speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
                    else:
                        speak(f"Sorry, I couldn’t find the weather for {city}.")
            except Exception as e:
                speak("An error occurred while fetching the weather.")
                print("Weather error:", e)
                
        else:
            from engine.features import getGPTResponse
            
            eel.DisplayMessage("Thinking wait for the Response.......")
            time.sleep(1.5)
            reply = getGPTResponse(query)
            
            speak(reply)

    except Exception as e:
        print("Error in allCommands():", e)

    # Optional UI reset
    if hasattr(eel, "ShowHood"):
        eel.ShowHood()

from datetime import datetime
import re
from shlex import quote
import struct
import subprocess
import pyaudio
import pyautogui
import pygame
import eel
import os
import sqlite3
import webbrowser
import time

from playsound import playsound
import requests

ACCESS_KEY = "YOUR_PORCUPINE_ACCESS_KEY"
from engine.command import *
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/sound.wav"
    playsound(music_dir)

@eel.expose
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip()
    app_name = query

    if not app_name:
        speak("Please say an app or website to open")
        return

    try:
        cursor.execute('SELECT path FROM sys_commands WHERE name = ?', (app_name,))
        results = cursor.fetchall()

        if results:
            path = results[0][0]
            speak(f"Opening {app_name}")
            os.system(f"open '{path}'")
            return

        cursor.execute('SELECT url FROM web_commands WHERE name = ?', (app_name,))
        results = cursor.fetchall()

        if results:
            url = results[0][0]
            speak(f"Opening {app_name}")
            webbrowser.open(url)
            return

        speak(f"Trying to open {app_name}")
        os.system(f"open -a '{app_name}'")

    except Exception as e:
        print("❌ Error:", e)
        speak("Something went wrong while trying to open it.")

# Play YouTube
def PlayYouTube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

# Hotword Detection

def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    keyword_list = ["jarvis", "alexa"]

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keywords=keyword_list
        )

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("🎤 Listening for hotword...")

        while True:
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                detected_word = keyword_list[keyword_index]
                print(f"✅ Hotword Detected: {detected_word}")
                pyautogui.hotkey("command", "j")
                time.sleep(2)

    except Exception as e:
        print("❌ Error in hotword detection:", e)

    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()

@eel.expose
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        # Try exact match first
        cursor.execute("SELECT mobile_no FROM contacts_1 WHERE LOWER(name) = ?", (query,))
        result = cursor.fetchone()

        # Fallback to startswith match if exact fails
        if not result:
            cursor.execute("SELECT mobile_no FROM contacts_1 WHERE LOWER(name) LIKE ?", (query + '%',))
            result = cursor.fetchone()

        # Final fallback to anywhere match
        if not result:
            cursor.execute("SELECT mobile_no FROM contacts_1 WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
            result = cursor.fetchone()

        if result:
            mobile_number_str = str(result[0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            speak("Contact not found.")
            return None, None
    except Exception as e:
        speak("Something went wrong while finding the contact.")
        print("❌ Error in findContact:", e)
        return None, None

@eel.expose

# Corrected function signature
# This should go inside your features.py file

def sendMessageViaWeb(phone_number, message):
    import webbrowser
    import time
    import pyautogui

    # Use plain message without URL encoding
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}&app_absent=0"

    webbrowser.open(url)
    time.sleep(10)  # Wait for the chat to load
    pyautogui.press("enter")


import google.generativeai as genai

# Configure the API key
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# Create the model instance
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def getGPTResponse(prompt):
    try:
        # Generate content with your updated config
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 120
            }
        )
        return response.text
    except Exception as e:
        print("❌ Gemini API Error:", e)
        return "Sorry, I couldn't generate a response."
    
def getTime():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    text = f"The current time is {current_time}"
    speak(text)
    return text




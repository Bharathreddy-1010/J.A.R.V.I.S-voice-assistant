import eel
import os
import time



from engine.features import *



@eel.expose
def get_response_from_jarvis(message):
    print("User said:", message)
    return f"JARVIS heard: '{message}'"


def start():
    eel.init("www")
    eel.start('index.html', mode='chrome', host='localhost', port=8000, block=False)
    playAssistantSound()

    while True:
        eel.sleep(1)  # Keep the app alive

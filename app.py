from flask import Flask, request, jsonify
from gtts import gTTS
import pygame
import threading
import os
import time

app = Flask(__name__)

# Initialize pygame mixer
pygame.mixer.init()

# Background music file (upload your mp3 to same directory)
BACKGROUND_MUSIC = "background.mp3"
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.set_volume(0.2)  # adjust volume for background
pygame.mixer.music.play(-1)  # loop forever

# Function to play voice alert
def play_voice(text):
    try:
        filename = "alert.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(filename)

        alert_sound = pygame.mixer.Sound(filename)
        alert_sound.set_volume(1.0)  # full volume for alert
        alert_sound.play()

        time.sleep(alert_sound.get_length())
        os.remove(filename)
    except Exception as e:
        print("Error:", e)

@app.route('/')
def home():
    return "Voice Alert System is running!"

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    message = data.get("text", "New alert received")
    threading.Thread(target=play_voice, args=(message,)).start()
    return jsonify({"status": "ok", "message": message})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

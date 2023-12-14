import tkinter as tk
from tkinter import ttk
from threading import Thread
import sounddevice as sd
import requests
import json
import base64
import time
import random

url = 'http://34.41.169.38/'
chunk_size = 1  # in seconds

def bytes_to_base64(bytes_data):
    return base64.b64encode(bytes_data).decode('utf-8')

def record_audio(callback):
    stream = sd.InputStream(channels=1, callback=callback)
    
    with stream:
        total_frames = int(chunk_size * 44100)
        sd.sleep(int(chunk_size * 1000))

def upload_audio(data, filename):
    payload = {'mp3': bytes_to_base64(data), 'filename': filename}
    upload_url = url + 'upload'
    response = requests.post(upload_url, json=payload)
    print(response.status_code)

class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")

        self.record_button = ttk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.user_input_label = ttk.Label(self.root, text="Enter your custom recording name:")
        self.user_input_label.pack()

        self.user_input = ttk.Entry(self.root)
        self.user_input.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.user_input.config(state=tk.DISABLED)

        # Get user input or generate random string
        user_input = self.user_input.get()
        if not user_input:
            user_input = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=5))

        self.filename = f'{user_input}_{int(time.time())}'
        self.audio_data = bytearray()

        def callback(indata, frames, time, status):
            if status:
                print('Error:', status)
            self.audio_data.extend(indata)

        self.audio_thread = Thread(target=record_audio, args=(callback,))
        self.audio_thread.start()

        self.status_label.config(text="Recording...")

    def stop_recording(self):
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.user_input.config(state=tk.NORMAL)

        self.audio_thread.join()
        upload_audio(self.audio_data, self.filename)
        self.status_label.config(text=f'Recording uploaded as {self.filename}')

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()

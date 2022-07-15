from flask import Flask
from queue import Queue, Empty
from threading import Thread
from time import sleep

app = Flask(__name__)
commands = Queue()

def game_loop():
    while True:
        try:
            command = commands.get_nowait()
            print(command)
        except Empty:
            pass
        sleep(5)  # TODO poll other things

Thread(target=game_loop, daemon=True).start()

# Literally the Flask quickstart but pushing to the queue
@app.route("/")
def hello_world():
    commands.put_nowait({ 'action': 'something' })
    print("hi")
    return "<p>Hello, World!</p>"
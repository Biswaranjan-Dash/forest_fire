# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from forest_fire_simulation import ForestFireSimulation
import logging
import time
from threading import Thread

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

simulation = ForestFireSimulation()

@app.route('/')
def home():
    app.logger.debug("Home route accessed")
    return render_template('index.html')

def simulate_fire():
    app.logger.debug("Starting fire simulation after 1-second delay")
    time.sleep(1)  # Wait for 1 seconds before starting the fire
    while True:
        forest_state = simulation.step()
        app.logger.debug("Simulation step completed. Emitting update.")
        socketio.emit('update', {'forest': forest_state})
        socketio.sleep(1)  # Control the speed of updates

@socketio.on('start_simulation')
def start_simulation():
    app.logger.debug("Start simulation event received")
    # Emit the initial state of the forest (fully green)
    initial_forest = simulation.forest.tolist()
    socketio.emit('update', {'forest': initial_forest})
    # Start the fire simulation in a separate thread
    thread = Thread(target=simulate_fire)
    thread.start()

if __name__ == '__main__':
    app.logger.debug("Starting Flask app")
    socketio.run(app, debug=True)

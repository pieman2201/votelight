import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import democracy

app = Flask(__name__)
socketio = SocketIO(app)

def handle_result(result):
    print('%s wins with %d votes' % (result.winner, result.win_votes))
    socketio.emit('result',
            {'winner': result.winner}, namespace = '/ws')

    with open('/sys/class/leds/led0/brightness', 'w') as f:
        f.write(result.winner)

def handle_countdown(remaining, string):
    socketio.emit('countdown', {
        'remaining': remaining,
        'countdown': string
        }, namespace = '/ws', broadcast = True)


@app.route('/')
def index():
    return render_template('index.html', winner = government.get_elected_candidate())

@socketio.on('connect', namespace = '/ws')
def connect():
    global thread

    if not thread.is_alive():
        thread = socketio.start_background_task(government.run)

@socketio.on('tally_vote', namespace = '/ws')
def tally_vote(candidate):
    vote = democracy.Vote(request.remote_addr, candidate)
    print('%s casts a vote for %s' % (vote.voter, vote.candidate))
    government.cast_vote(vote)


if __name__ == '__main__':
    government = democracy.Democracy(
            interval = 60,
            candidates = ['0', '1'],
            countdown_callback = handle_countdown,
            result_callback = handle_result
            )

    thread = socketio.start_background_task(government.run)

    socketio.run(app, host = '0.0.0.0')

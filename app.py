import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import rgbvote

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

import eventlet
eventlet.monkey_patch()


def handle_result(result):
    print('outcome: %s with %d votes' % (result.color.as_tuple_str(), result.total_votes))
    socketio.emit('result', {
        'rgb': result.color.as_tuple(),
        'color': result.color.as_hex_str(),
        'tally': result.tally.tallies
        }, namespace = '/ws', broadcast = True)

def handle_countdown(remaining, string):
    socketio.emit('countdown', {
        'remaining': remaining,
        'countdown': string
        }, namespace = '/ws', broadcast = True)

def handle_resume():
    socketio.emit('resume', {
        'color': government.current.color.as_hex_str()
        }, namespace = '/ws', broadcast = True)


@app.route('/')
def index():
    return render_template('index.html',
            government = government,
            voter = request.remote_addr
            )

@socketio.on('connect', namespace = '/ws')
def connect():
    global gov_thread

    if not gov_thread.is_alive():
        gov_thread = socketio.start_background_task(government.run)


@socketio.on('tally_vote', namespace = '/ws')
def tally_vote(candidate):
    vote = rgbvote.RGBVote(request.remote_addr, candidate)
    print('%s casts a vote for %s' % (vote.voter, vote.candidate))
    government.get_election().cast_vote(vote)


if __name__ == '__main__':
    government = rgbvote.RGBDemocracy(
            vote_time = 55,
            rest_time = 5,
            countdown_callback = handle_countdown,
            result_callback = handle_result,
            resume_callback = handle_resume
            )

    gov_thread = socketio.start_background_task(government.run)

    socketio.run(app, host = '0.0.0.0', port = 80)

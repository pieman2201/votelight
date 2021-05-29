import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread, Event

class Democracy():
    def __init__(self, interval = 60):
        self.interval = interval
        self.votes = {
                '1': 0,
                '0': 0
                }
        self.voters = []
        self.last_winner = '0'
        self.voting_is_over = False

    def getRemaining(self):
        current = int(time.time())
        end = current - (current % self.interval) + self.interval
        return end - current

    def getCountDown(self, remaining):
        return '%02d:%02d' % (int(remaining / 60), remaining % 60)

    def runCountDown(self):
        remaining = self.getRemaining()
        while remaining > 1:
            start = time.time()
            remaining = self.getRemaining()
            socketio.emit('countdown', {
                'remaining': remaining,
                'countdown': self.getCountDown(remaining)
                }, namespace = '/ws', broadcast = True)
            time.sleep(max(int(start) + 1 - time.time(), 0))
        self.voting_is_over = True
        socketio.emit('countdown', {
            'remaining': 0,
            'countdown': "Tallying..."
            }, namespace = '/ws')

    def tallyVote(self, candidate):
        if candidate not in self.votes.keys():
            return 'failed'
        self.votes[candidate] += 1

    def getWinner(self):
        winner = max(self.votes.keys(), key = self.votes.get)
        loser = min(self.votes.keys(), key = self.votes.get)
        return self.last_winner if self.votes[winner] == votes[loser] else winner

    def respectVote(self):
        self.last_winner = self.getWinner()

        socketio.emit('winner',
                {'name': 'o' + ('ff', 'n')[int(self.last_winner)]}, namespace = '/ws')

        with open('/sys/class/leds/led0/brightness', 'w') as f:
            f.write(self.last_winner)

    def flushBallotBox(self):
        self.votes = {
                '1': 0,
                '0': 0
                }
        self.voters = []

    def run(self):
        while True:
            self.runCountDown()
            self.respectVote()
            self.flushBallotBox()


@app.route('/')
def index():
    return render_template('index.html', winner = democracy.last_winner)

@socketio.on('connect', namespace = '/ws')
def connect():
    global thread

    if not thread.is_alive():
        thread = socketio.start_background_task(democracy.run)

@socketio.on('vote', namespace = '/ws')
def vote(data):
    democracy.tallyVote(


if __name__ == '__main__':
    app = Flask(__name__)
    socketio = SocketIO(app)
    thread = Thread()
    democracy = Democracy()
    democracy.respectVote()

    socketio.run(app, host = '0.0.0.0')

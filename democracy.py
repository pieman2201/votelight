import time

class Vote():
    def __init__(self, voter, candidate):
        self.voter = voter
        self.candidate = candidate


class ElectionResult():
    def __init__(self, votes, default):
        self.votes = votes
        self.default = default

        winner = max(self.votes.keys(), key = self.votes.get)
        winner = self.default if len(set(self.votes.values())) == 1 else winner
        loser = min(self.votes.keys(), key = lambda k: self.votes.get(k) if k != winner else float('inf'))

        self.winner = winner
        self.win_votes = self.votes[winner]
        self.loser = loser
        self.loss_votes = self.votes[loser]


class Election():
    def __init__(self, end_time, default = None, candidates = ['0', '1'], countdown_callback = (lambda r, s: None)):
        self.end_time = end_time
        self.candidates = candidates
        self.votes = { c: 0 for c in self.candidates }
        self.voters = []
        self.default = default
        if self.default ==  None:
            self.default = self.candidates[0]
        self.countdown_callback = countdown_callback

    def get_remaining(self):
        r = self.end_time - time.time()
        return int(r - (1 if r < 0 else 0))

    def get_countdown(self):
        remaining = self.get_remaining()
        return '%02d:%02d' % (int(remaining / 60), remaining % 60)

    def cast_vote(self, vote):
        if vote.voter not in self.voters and vote.candidate in self.candidates and not time.time() >= self.end_time:
            self.voters.append(vote.voter)
            self.votes[vote.candidate] += 1

    def get_result(self):
        return ElectionResult(self.votes, self.default)

    def run(self):
        while self.get_remaining() >= 0:
            start = time.time()
            self.countdown_callback(self.get_remaining(), self.get_countdown())

            time.sleep(max(int(start) + 1 - time.time(), 0))


class Democracy():
    def __init__(self, interval = 60, candidates = ['0', '1'], countdown_callback = (lambda r, s: None), result_callback = (lambda er: None)):
        self.interval = interval

        self.candidates = candidates

        self.countdown_callback = countdown_callback
        self.result_callback = result_callback

        self.elections = [
                Election(
                    int(time.time()),
                    candidates = self.candidates,
                    countdown_callback = self.countdown_callback
                    )
                ]

    def cast_vote(self, vote):
        self.elections[-1].cast_vote(vote)

    def get_elected_candidate(self):
        return self.elections[-1].default

    def run(self):
        while True:
            cycle = self.elections[-1]
            print('election ends in %d seconds' % cycle.get_remaining())
            cycle.run()
            self.result_callback(cycle.get_result())

            self.elections.append(
                    Election(
                        int(time.time() + self.interval),
                        default = cycle.get_result().winner,
                        candidates = self.candidates,
                        countdown_callback = self.countdown_callback
                        )
                    )




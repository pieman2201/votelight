import time

class Vote():
    def __init__(self, voter, candidate):
        self.voter = voter
        self.candidate = candidate


class ElectionResult():
    def __init__(self, votes, default):

        tally = {default: 0}
        for voter in votes.keys():
            tally[votes[voter]] = tally.get(votes[voter], 0) + 1

        winner = max(tally.keys(), key = tally.get)
        winner = default if len(set(tally.values())) == 1 else winner
        loser = min(tally.keys(), key = lambda k: tally.get(k) if k != winner else float('inf'))

        self.winner = winner
        self.win_votes = tally[winner]
        self.loser = loser
        self.loss_votes = tally[loser]


class Election():
    def __init__(self, end_time, default = None, candidates = ['0', '1'], countdown_callback = (lambda r, s: None)):
        self.end_time = end_time
        self.candidates = candidates
        self.votes = {}
        self.default = default
        if self.default ==  None:
            self.default = self.candidates[0]
        self.countdown_callback = countdown_callback

    def get_remaining(self):
        r = self.end_time - time.time()
        return int(r - (1 if r < 0 else 0))

    def get_countdown(self):
        remaining = self.get_remaining() + 1
        if remaining >= 60:
            return '%02d:%02d' % (int(remaining / 60), remaining % 60)
        else:
            return '%ds' % int(remaining)

    def can_vote(self, voter):
        return (self.votes.get(voter, None) is None and not time.time() >= self.end_time)

    def cast_vote(self, vote):
        if self.can_vote(vote.voter) and vote.candidate in self.candidates:
            self.votes[vote.voter] = vote.candidate

    def retrieve_vote(self, voter):
        return self.votes.get(voter, None)

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

    def get_election(self):
        return self.elections[-1]

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




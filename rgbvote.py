import time

class RGBVote:
    def __init__(self, voter, candidate):
        self.voter = voter
        self.candidate = candidate

class RGBColor:
    def __init__(self, color_map):
        self.R = color_map.get('R', 0)
        self.G = color_map.get('G', 0)
        self.B = color_map.get('B', 0)

    def as_tuple(self):
        return (self.R, self.G, self.B)

    def as_tuple_str(self):
        return str(self.as_tuple())

    def as_hex_str(self):
        return '#' + ''.join([('%02x' % v) for v in self.as_tuple()])

class RGBElectionResult:
    def __init__(self, tally, result_norm = 255):
        self.result_norm = result_norm
        self.tally = tally
        self.total_votes = sum(self.tally.tallies.values())
        factor = result_norm / max(self.total_votes, 1)
        self.color = RGBColor({ c : round(self.tally.tallies[c] * factor) for c in self.tally.tallies.keys() })


class RGBTally:
    def __init__(self, tallies = None):
        self.tallies = {
                'R': 0,
                'G': 0,
                'B': 0
                } if tallies == None else tallies

    def increment(self, vote):
        if vote.candidate in self.tallies.keys():
            self.tallies[vote.candidate] += 1
            return True
        return False


class RGBElection:
    def __init__(self, end_time, countdown_callback):
        self.end_time = end_time
        self.votes = {}

        self.tally = RGBTally()

        self.countdown_callback = countdown_callback

    def get_remaining(self):
        r = self.end_time - time.time()
        return int(r + 1)

    def get_clock_str(self):
        remaining = self.get_remaining()
        if remaining >= 60:
            return '%02d:%02d' % (int(remaining / 60), remaining % 60)
        else:
            return '%ds' % int(remaining)

    def can_vote(self, voter):
        return (self.votes.get(voter, None) is None and not self.get_remaining() <= 0)

    def cast_vote(self, vote):
        if self.can_vote(vote.voter) and self.tally.increment(vote):
            self.votes[vote.voter] = vote.candidate

    def retrieve_vote(self, voter):
        return self.votes.get(voter, None)

    def get_result(self):
        return RGBElectionResult(self.tally)

    def run(self):
        while self.get_remaining() > 0:
            start = time.time()
            self.countdown_callback(self.get_remaining(), self.get_clock_str())

            time.sleep(max(int(start) + 1 - time.time(), 0))


class RGBDemocracy:
    def __init__(self, vote_time, rest_time, countdown_callback, result_callback, resume_callback):
        self.vote_time = vote_time
        self.rest_time = rest_time
        self.countdown_callback = countdown_callback
        self.result_callback = result_callback
        self.resume_callback = resume_callback

        self.resting = False

        self.current = RGBElectionResult(RGBTally({c:0 for c in 'RGB'}))
        self.elections = [
                RGBElection(
                    int(time.time()),
                    countdown_callback
                    )
                ]

    def get_election(self):
        return self.elections[-1]

    def run(self):
        while True:
            cycle = self.get_election()
            print('election ends in %d seconds' % cycle.get_remaining())
            cycle.run()
            self.result_callback(cycle.get_result())
            self.current = cycle.get_result()

            self.resting = True
            time.sleep(self.rest_time)
            self.resting = False

            self.resume_callback()

            self.elections.append(
                    RGBElection(
                        int(time.time() + self.vote_time),
                        countdown_callback = self.countdown_callback
                        )
                    )

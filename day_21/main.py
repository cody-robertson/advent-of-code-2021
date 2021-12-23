from typing import NamedTuple


class QuantumState(NamedTuple):
    player_1_position: int
    player_2_position: int
    player_1_score: int
    player_2_score: int
    player_1_turn: bool
    # roll_count: int


def load_input(file_name: str):
    with open(file_name, "r") as input_file:
        return [int(line.strip().split(": ")[1]) for line in input_file]


def generate_player_scores():
    start = 0
    while True:
        spaces = 0
        for i in range(3):
            spaces += (start % 100) + 1
            start += 1
        yield spaces


# class DeterministicDie:
#     def __init__(self):
#         self._counter = 0
#
#     @property
#     def __counter(self):
#         value = self._counter
#         self._counter += 1
#         return value
#
#     def roll(self):
#         return self.__counter


class DiracDieSimulation:
    def __init__(self, player_1_start, player_2_start):
        self.player_one_position = player_1_start - 1
        self.player_two_position = player_2_start - 1
        self.player_one_score = 0
        self.player_two_score = 0
        self.score_generator = generate_player_scores()
        self.is_player_one_turn = True
        self.rolls = 0

    def play(self):
        rolls = next(self.score_generator)
        self.rolls += 3
        if self.is_player_one_turn:
            self.player_one_position = (rolls + self.player_one_position) % 10
            self.player_one_score += self.player_one_position + 1
        else:
            self.player_two_position = (rolls + self.player_two_position) % 10
            self.player_two_score += self.player_two_position + 1
        self.is_player_one_turn = not self.is_player_one_turn

    def play_until_1000(self):
        while self.player_one_score < 1000 and self.player_two_score < 1000:
            self.play()

    @property
    def losing_score(self):
        if self.player_two_score < self.player_one_score:
            return self.player_two_score * self.rolls
        return self.player_one_score * self.rolls


def quantum_simulate_until_21(state: QuantumState, cache: dict = None):
    if cache is None:
        cache = {}
    if state in cache:
        return cache[state]
    elif state.player_1_score >= 21:
        cache[state] = 1, 0
        return 1, 0
    elif state.player_2_score >= 21:
        cache[state] = 0, 1
        return 0, 1

    total_wins, total_losses = 0, 0
    for roll, timeline_branches in [
        (3, 1),
        (4, 3),
        (5, 6),
        (6, 7),
        (7, 6),
        (8, 3),
        (9, 1),
    ]:
        player_one_position = (
            state.player_1_position
            if not state.player_1_turn
            else (state.player_1_position + roll - 1) % 10 + 1
        )
        player_one_score = (
            state.player_1_score
            if not state.player_1_turn
            else state.player_1_score + player_one_position
        )
        player_two_position = (
            state.player_2_position
            if state.player_1_turn
            else (state.player_2_position + roll - 1) % 10 + 1
        )
        player_two_score = (
            state.player_2_score
            if state.player_1_turn
            else state.player_2_score + player_two_position
        )
        player_one_turn = not state.player_1_turn
        next_state = QuantumState(
            player_one_position,
            player_two_position,
            player_one_score,
            player_two_score,
            player_one_turn,
        )
        wins, losses = quantum_simulate_until_21(next_state, cache)
        total_wins += wins * timeline_branches
        total_losses += losses * timeline_branches
    cache[state] = total_wins, total_losses
    return total_wins, total_losses


if __name__ == "__main__":
    input_first, input_second = load_input("input.txt")
    sim = DiracDieSimulation(input_first, input_second)
    sim.play_until_1000()
    print(sim.losing_score)

    initial_state = QuantumState(input_first, input_second, 0, 0, True)
    print(initial_state)
    print(quantum_simulate_until_21(initial_state))

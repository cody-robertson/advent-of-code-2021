from copy import deepcopy
from itertools import permutations


indices = list(permutations((-1, 0, 1), 2))
print(indices)


def load_input(file_name):
    board = []
    with open(file_name, "r") as input_file:
        for line in input_file:
            board.append([int(n) for n in line.strip()])
    return board


class OctopusSimulation:
    def __init__(self, file_name: str):
        self.initial_state = load_input(file_name)
        self.state = deepcopy(self.initial_state)
        self.total_flashes = 0

    def reset_state(self):
        self.state = deepcopy(self.initial_state)
        self.total_flashes = 0

    def increment_board(self):
        for i, row in enumerate(self.state):
            for j, _ in enumerate(row):
                self.state[i][j] += 1

    def flash(self, i_flash, j_flash):
        self.state[i_flash][j_flash] = 0
        self.total_flashes += 1
        for i in (i_flash - 1, i_flash, i_flash + 1):
            for j in (j_flash - 1, j_flash, j_flash + 1):
                if (
                    0 <= i < len(self.state)
                    and 0 <= j < len(self.state[i])
                    and self.state[i][j] != 0
                ):
                    self.state[i][j] += 1

    def get_octopuses_ready_to_flash(self):
        ready_to_flash = set()
        for i, row in enumerate(self.state):
            for j, item in enumerate(row):
                if item > 9:
                    ready_to_flash.add((i, j))
        return ready_to_flash

    def flash_until_stable(self):
        ready_to_flash = self.get_octopuses_ready_to_flash()
        while len(ready_to_flash) > 0:
            for i, j in ready_to_flash:
                self.flash(i, j)
            ready_to_flash = self.get_octopuses_ready_to_flash()

    def step(self):
        self.increment_board()
        self.flash_until_stable()

    def step_n(self, n: int):
        self.reset_state()
        for _ in range(n):
            self.step()

    def have_all_flashed(self):
        for row in self.state:
            for item in row:
                if item != 0:
                    return False
        return True

    def step_until_simultaneous(self):
        self.reset_state()
        have_all_flashed = self.have_all_flashed()
        steps = 0
        while not have_all_flashed:
            self.step()
            steps += 1
            have_all_flashed = self.have_all_flashed()
        return steps

    def __repr__(self):
        rv = ""
        for row in self.state:
            rv += " ".join(map(str, row)) + "\n"
        return rv

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    sim = OctopusSimulation("input.txt")
    print(sim)
    sim.step_n(100)
    print(sim.total_flashes)
    print(sim.step_until_simultaneous())

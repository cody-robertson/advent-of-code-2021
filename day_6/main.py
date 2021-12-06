from collections import deque


def load_input(file_name):
    # store counts for values 0-8
    initial_state = [0 for _ in range(9)]
    with open(file_name, "r") as input_file:
        values = list(map(int, input_file.readline().strip().split(",")))
        for value in values:
            initial_state[value] += 1
    return initial_state


class LanternfishSim:
    def __init__(self, file_name):
        self.initial_state = load_input(file_name)
        self.state = deque(self.initial_state)

    def reset_state(self):
        self.state = deque(self.initial_state)

    @property
    def current_population(self):
        return sum(self.state)

    def simulate(self):
        self.state[7] += self.state[0]
        self.state.rotate(-1)
        return self.current_population

    def simulate_days(self, num_days):
        self.reset_state()
        for _ in range(num_days):
            self.simulate()
        return self.current_population


if __name__ == "__main__":
    sim = LanternfishSim("input.txt")
    print(sim.simulate_days(80))
    print(sim.simulate_days(256))

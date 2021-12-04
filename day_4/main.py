from typing import NamedTuple


Board = list[list[int]]


class BingoInput(NamedTuple):
    moves: list[int]
    boards: list[Board]


class BingoSimulation:
    def __init__(self, file_name):
        self.moves, self.boards = self.load_input(file_name)
        self.move_index = 0
        self.complete_boards = []

    @staticmethod
    def _parse_board_line(input_line, board_size=5) -> list[int]:
        indices = [num for num in range(100) if num % 3 == 0]
        return [
            int(input_line[start:end])
            for start, end in zip(indices[:board_size], indices[1 : board_size + 1])
        ]

    def load_input(self, file_name) -> BingoInput:
        with open(file_name) as input_file:
            input_lines = input_file.readlines()
        moves = [int(move) for move in input_lines[0].split(",")]
        boards = []
        board_index = 0
        for line in input_lines[2:]:
            # removing a leading space skews indices needed for parse_board_line
            line = line.rstrip()
            if line == "":
                board_index += 1
                continue
            if board_index == len(boards):
                boards.append([])
            boards[board_index].append(self._parse_board_line(line))
        return BingoInput(moves, boards)

    def _check_rows(self, board_index):
        board = self.boards[board_index]
        spaces_remaining = [len([spot for spot in row if spot >= 0]) for row in board]
        return len([spaces for spaces in spaces_remaining if spaces == 0])

    def _check_columns(self, board_index):
        board = self.boards[board_index]
        columns = list(zip(*board))
        spaces_remaining = [
            len([spot for spot in column if spot >= 0]) for column in columns
        ]
        return len([spaces for spaces in spaces_remaining if spaces == 0])

    def is_board_complete(self, board_index):
        if board_index in self.complete_boards:
            return True
        is_complete = (
            self._check_rows(board_index) > 0 or self._check_columns(board_index) > 0
        )
        if is_complete:
            self.complete_boards.append(board_index)
        return is_complete

    def check_boards(self):
        return [
            board_index
            for board_index in range(len(self.boards))
            if self.is_board_complete(board_index)
        ]

    def apply_move_to_board(self, board_index):
        board = self.boards[board_index]
        move = self.moves[self.move_index]
        for row_index in range(len(board)):
            for col_index in range(len(board[0])):
                if board[row_index][col_index] == move:
                    board[row_index][col_index] = -(self.move_index + 1)

    def apply_move(self):
        for i in range(len(self.boards)):
            if i not in self.complete_boards:
                self.apply_move_to_board(i)
        self.move_index += 1

    def calculate_board_score(self, board_index):
        board = self.boards[board_index]
        previous_num_called = self.moves[self.move_index - 1]
        board_sum = sum([sum([space for space in row if space >= 0]) for row in board])
        return board_sum * previous_num_called

    def simulate_until_bingo(self):
        self.check_boards()
        while len(self.complete_boards) == 0 and self.move_index < len(self.moves):
            self.apply_move()
            self.check_boards()
        return (
            self.move_index,
            self.complete_boards,
            [self.calculate_board_score(board) for board in self.complete_boards],
        )

    def simulate_all(self):
        self.check_boards()
        while len(self.complete_boards) < len(self.boards) and self.move_index < len(
            self.moves
        ):
            self.apply_move()
            self.check_boards()
        return (
            self.move_index,
            self.complete_boards[-1],
            self.calculate_board_score(self.complete_boards[-1]),
        )


if __name__ == "__main__":
    sim = BingoSimulation("input.txt")
    moves_until_bingo, complete_boards, board_scores = sim.simulate_until_bingo()
    print(moves_until_bingo, complete_boards, board_scores)
    sim = BingoSimulation("input.txt")
    moves_until_bingo, complete_boards, board_scores = sim.simulate_all()
    print(moves_until_bingo, complete_boards, board_scores)

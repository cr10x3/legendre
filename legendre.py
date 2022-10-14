from dataclasses import dataclass
from random import randint
import colorama


@dataclass
class Board:
    rows: int
    columns: int
    cursor: tuple[int, int]
    gem_pointers: list[tuple[int, int]]
    visited_points: dict[tuple[int, int], bool]
    last_move: str

    def cursor_is_valid(self, cursor: tuple[int, int]):
        x, y = cursor
        valid_x = 0 <= x < self.columns
        valid_y = 0 <= y < self.rows
        return valid_x and valid_y

    def all_valid_moves(self):
        x, y = self.cursor
        moves = dict()

        # Check for up
        if self.cursor_is_valid((x, y-1)) and (x, y-1) not in self.visited_points:
            moves['up'] = (x, y-1)

        # Check for left
        if self.cursor_is_valid((x-1, y)) and (x-1, y) not in self.visited_points:
            moves['left'] = (x-1, y)

        # Check for down
        if self.cursor_is_valid((x, y+1)) and (x, y+1) not in self.visited_points:
            moves['down'] = (x, y+1)

        # Check for right
        if self.cursor_is_valid((x+1, y)) and (x+1, y) not in self.visited_points:
            moves['right'] = (x+1, y)

        return moves

    def visit_cursor(self, new_cursor) -> tuple[int, int]:
        # Returns cursor if gem found
        if self.cursor in self.gem_pointers:
            self.gem_pointers.remove(self.cursor)
            return self.cursor
        self.visited_points[self.cursor] = True

    def move(self, direction) -> tuple[int, int]:
        # Returns cursor if gem found
        valid_moves = self.all_valid_moves()
        if direction not in valid_moves:
            raise Exception(' Invalid move on board ! ')
        self.cursor = valid_moves[direction]
        self.last_move = direction
        self.display_board()
        return self.visit_cursor(self.cursor)

    def gems_remaining(self) -> int:
        return len(self.gem_pointers)

    def display_board(self) -> None:
        m = self.rows
        n = self.columns
        print("="*20)
        print()
        for i in range(m):
            row = ''
            for j in range(n):
                if (i, j) in self.gem_pointers:
                    row += f'{colorama.Fore.GREEN}G'
                    continue
                visited_indicator = f'{colorama.Fore.BLUE}X'
                pending_indicator = f'{colorama.Fore.WHITE}0'
                row += visited_indicator if (i,
                                             j) in self.visited_points else pending_indicator
            print(row)
        print(f"{colorama.Fore.WHITE}="*20)
        print()


@dataclass
class Strategy:
    depth: int
    breadth: int
    board_state: Board

    def search(self):
        current_breadth = 0
        moves = self.board_state.all_valid_moves()
        for direction in moves.keys():
            if current_breadth == self.breadth:
                return
            self.dfs(direction, 0)
            current_breadth += 1
           
    def dfs(self, direction, current_depth):
        if current_depth > self.depth:
            return
        moves = self.board_state.all_valid_moves()
        if not direction in moves:
            return
        gem = self.board_state.move(direction)
        if gem != None:
            print(f'Found gem at {gem}')
        self.dfs(direction, current_depth+1)


def random_point(rows, columns):
    rand_y = randint(0, rows-1)
    rand_x = randint(0, columns-1)
    return (rand_x, rand_y)


def run_simulation(rows, columns, gems, max_depth, max_breadth):
    random_init = random_point(rows, columns)
    gem_list = [random_point(rows, columns) for _ in range(gems)]
    b = Board(rows, columns, random_init, gem_list, dict(), '')
    strategy = Strategy(max_depth, max_breadth, b)
    search_operations = 0
    while b.gems_remaining() > 0:
        if search_operations > 1000:
            print('exhausted')
            return
        strategy.search()
        search_operations += 1
        strategy.depth += randint(-strategy.depth+1, strategy.depth+4)



if __name__ == '__main__':
    run_simulation(50, 50, 7, 5, 5)

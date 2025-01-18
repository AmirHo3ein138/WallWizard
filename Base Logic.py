import os

# Constants
BOARD_SIZE = 17
# Time limit for each player's turn in seconds
TURN_TIME_LIMIT = 30

# Utility functions
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board():
    board = []
    for row in range(BOARD_SIZE):
        line = []
        for col in range(BOARD_SIZE):
            if row % 2 == 0 and col % 2 == 0:
                line.append(".")  # Playable spaces
            elif row % 2 == 1 and col % 2 == 1:
                line.append("+")  # Intersection points for walls
            else:
                line.append("#")  # Wall spaces
        board.append(line)
    return board

def display_board(board):
    clear_console()
    for row in board:
        print(" ".join(row))
    print("\n")

class Player:
    def __init__(self, name, start_position, symbol):
        self.name = name
        self.position = start_position
        self.symbol = symbol
        self.walls_left = 10

class QuoridorGame:
    def __init__(self):
        self.board = create_board()
        self.players = []
        self.current_turn = 0
        self.walls = set()

    def add_player(self, name, start_position, symbol):
        player = Player(name, start_position, symbol)
        self.players.append(player)
        x, y = start_position
        self.board[x][y] = symbol

    def move_player(self, player_name, direction):
        player = next(p for p in self.players if p.name == player_name)
        x, y = player.position

        if direction == 'w':
            new_position = (x - 2, y)
        elif direction == 's':
            new_position = (x + 2, y)
        elif direction == 'a':
            new_position = (x, y - 2)
        elif direction == 'd':
            new_position = (x, y + 2)
        else:
            print("Invalid direction! Use 'w', 'a', 's', or 'd'.")
            return False

        if self.is_valid_move(player, new_position):
            nx, ny = new_position
            self.board[x][y] = "."
            self.board[nx][ny] = player.symbol
            player.position = new_position
            return True

        print("Invalid move! Try again.")
        return False

    def is_valid_move(self, player, new_position):
        x, y = player.position
        nx, ny = new_position

        # Check boundaries
        if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
            return False

        # Ensure the cell is empty
        if self.board[nx][ny] != ".":
            return False

        # Check for valid two-step moves
        if abs(nx - x) + abs(ny - y) == 2:
            return True

        # Check for jumping over an opponent
        for opponent in self.players:
            if opponent != player and opponent.position == ((x + nx) // 2, (y + ny) // 2):
                mid_x, mid_y = opponent.position
                if self.board[nx][ny] == ".":
                    return True

                # Check diagonal moves if jumping forward is blocked
                for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                    diag_x, diag_y = x + dx, y + dy
                    if 0 <= diag_x < BOARD_SIZE and 0 <= diag_y < BOARD_SIZE:
                        if self.board[diag_x][diag_y] == ".":
                            return True

        return False

    def place_wall(self, player_name, wall_position, orientation):
        player = next(p for p in self.players if p.name == player_name)
        grid_x, grid_y = wall_position

        x = grid_x * 2
        y = grid_y * 2

        if player.walls_left <= 0:
            print("No walls left to place!")
            return False

        if self.is_valid_wall((x, y), orientation):
            if orientation == 'h':
                if y + 3 < BOARD_SIZE:
                    self.board[x][y - 1] = "═"
                    self.board[x][y] = "═"
                    self.board[x][y + 1] = "═"
                else:
                    print("Invalid wall placement! Out of bounds.")
                    return False
            elif orientation == 'v':
                if x + 3 < BOARD_SIZE:
                    self.board[x - 1][y] = "║"
                    self.board[x][y] = "║"
                    self.board[x + 1][y] = "║"
                else:
                    print("Invalid wall placement! Out of bounds.")
                    return False

            self.walls.add((x, y, orientation))
            player.walls_left -= 1
            return True

        print("Invalid wall placement! Try again.")
        return False

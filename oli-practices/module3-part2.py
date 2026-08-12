'''Workshop Module 3 Part 2 - Rock Paper Scissors'''

import subprocess
import sys
import tty
import termios
from random import randint

CHOICES = {1: "Rock", 2: "Paper", 3: "Scissors"}


def masked_input(prompt):
    """Reads input but shows '*' instead of characters - used so player 2 can't see player 1's pick."""
    print(prompt, end='', flush=True)
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        chars = []
        while True:
            ch = sys.stdin.read(1)
            if ch in ('\r', '\n'):
                print()
                break
            elif ch in ('\x7f', '\x08'):
                if chars:
                    chars.pop()
                    print('\b \b', end='', flush=True)
            elif ch == '\x03':
                raise KeyboardInterrupt
            else:
                chars.append(ch)
                print('*', end='', flush=True)
        return ''.join(chars)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def clear_screen():
    subprocess.run('cls' if sys.platform == 'win32' else 'clear', shell=False)


class Player:

    def __init__(self, name, is_computer=False):
        self.name = name
        self.score = 0
        self.is_computer = is_computer

    def add_win(self):
        self.score += 1


class RockPaperScissors:

    def __init__(self, player1, player2, rounds):
        self.player1 = player1
        self.player2 = player2
        self.rounds = rounds

    def get_choice(self, player, masked=False):
        if player.is_computer:
            return randint(1, 3)
        while True:
            print("Enter 1 for Rock, 2 for Paper or 3 for Scissors")
            if masked:
                raw = masked_input(f"{player.name}'s choice: ").strip()
            else:
                raw = input(f"{player.name}'s choice: ").strip()
            if raw in ("1", "2", "3"):
                return int(raw)
            print("Please enter 1, 2, or 3")

    def get_winner(self, c1, c2):
        if c1 == c2:
            return None
        beats = {1: 3, 2: 1, 3: 2}
        if beats[c1] == c2:
            return self.player1
        return self.player2

    def play_round(self, round_num):
        pvp = not self.player2.is_computer
        print(f"\nRound {round_num} of {self.rounds}")

        c1 = self.get_choice(self.player1, masked=pvp)

        if pvp:
            input(f"[{self.player1.name} locked in] Pass to {self.player2.name}, then press Enter...")
            clear_screen()
            print(f"\nRound {round_num} of {self.rounds}")

        c2 = self.get_choice(self.player2, masked=pvp)

        if pvp:
            clear_screen()
            print(f"\nRound {round_num} of {self.rounds}")

        print(f"{self.player1.name}: {CHOICES[c1]}")
        print(f"{self.player2.name}: {CHOICES[c2]}")

        winner = self.get_winner(c1, c2)
        if winner is None:
            print("Result: It's a draw!")
        else:
            winner.add_win()
            print(f"Result: {winner.name} wins this round!")

    def play_game(self):
        print(f"\nRock Paper Scissors ({self.rounds} Rounds)")
        print(f"{self.player1.name} vs {self.player2.name}")

        for i in range(1, self.rounds + 1):
            self.play_round(i)

        self.show_result()

    def show_result(self):
        draws = self.rounds - self.player1.score - self.player2.score
        print("\nFinal Score")
        print(f"{self.player1.name}: {self.player1.score}")
        print(f"{self.player2.name}: {self.player2.score}\n")

        if self.player1.score > self.player2.score:
            print(f"Champion: {self.player1.name}!")
        elif self.player2.score > self.player1.score:
            print(f"Champion: {self.player2.name}!")
        else:
            print("It's a tie!")
        if draws:
            print(f"({draws} draw{'s' if draws > 1 else ''})")


def get_rounds(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a number > 0")
        except ValueError:
            print("Please enter integer.")


if __name__ == "__main__":
    print("\nWelcome to Rock Paper Scissors")
    print("Press 1 vs Computer or 2 vs Player")
    while True:
        mode = input("Your choice: ").strip()
        if mode in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    if mode == "1":
        name1 = input("Your name: ").strip() or "Player"
        rounds = get_rounds("How many rounds? ")
        player1 = Player(name1)
        player2 = Player("Computer", is_computer=True)
    else:
        name1 = input("Player 1 name: ").strip() or "Player 1"
        name2 = input("Player 2 name: ").strip() or "Player 2"
        rounds = get_rounds("How many rounds? ")
        player1 = Player(name1)
        player2 = Player(name2)

    game = RockPaperScissors(player1, player2, rounds)
    game.play_game()

import random
import datetime
import os
import json
import cli_box
from colorama import Fore, Back, init
from rich.console import Console
from rich.theme import Theme
from rich.table import Table

custom_theme = Theme({'success': 'green', 'error': 'bold red',
                      'others': 'blue underline', 'tie': 'magenta', 'lose': 'purple', 'win': 'orange3'})

console = Console(theme=custom_theme)

init()


class RPS:
    def __init__(self, player_1: str, player_2: str, rounds: int):
        self.player_1 = player_1
        self.player_2 = player_2
        self.round = rounds
        self.wins = {player_1: 0, player_2: 0}
        self.rolls = {} # type: ignore
        self.load_rolls()
        self.show_leaderboard()

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def log(msg):
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'rps.log')

        with open(filename, 'a', encoding='utf-8') as fout:
            fout.write(f"[{datetime.datetime.now().date().isoformat()}] ")
            fout.write(msg)
            fout.write('\n')

    def load_rolls(self):
        directory = os.path.dirname(__file__)
        file_name = os.path.join(directory, 'rolls.json')

        with open(file_name, 'r', encoding='utf-8') as fin:
            self.rolls = json.load(fin)

        self.log(f"Loaded rolls: {list(self.rolls.keys())} from {os.path.basename(file_name)}.")

    @staticmethod
    def load_leaders():
        directory = os.path.dirname(__file__)
        file_name = os.path.join(directory, 'leaderboard.json')

        if not os.path.exists(file_name):
            return {}

        with open(file_name, 'r', encoding='utf-8') as fin:
            return json.load(fin)

    def show_leaderboard(self):
        print('')
        table = Table(title="LeaderBoard")
        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Number Of Wins", style="magenta")

        leaders = self.load_leaders()

        sorted_leaders = [*leaders.items()]
        sorted_leaders.sort(key=lambda l: l[1], reverse=True)

        for name, wins in sorted_leaders:
            table.add_row(f"{name}", f"{wins}")

        console.print(table, style="dark_goldenrod")

    def record_wins(self, winner):
        leaders = self.load_leaders()

        if winner in leaders:
            leaders[winner] += 1
        else:
            leaders[winner] = 1

        directory = os.path.dirname(__file__)
        file_name = os.path.join(directory, 'leaderboard.json')

        with open(file_name, 'w', encoding='utf-8') as fout:
            json.dump(leaders, fout)

    def get_roll(self):
        console.print("Available rolls", style='others')
        for index, roll in enumerate(self.rolls.keys(), start=1):
            print(f"{index}. {roll}")

        answer = input(f"{Fore.BLUE}{self.player_1}, {Fore.GREEN}what is your roll? ")
        if not answer.isdigit():
            console.print(f"Sorry {self.player_1}, {answer} is not a digit!", style='error')
            return None

        selected_index = int(answer) - 1
        if selected_index < 0 or selected_index >= len(self.rolls.keys()):
            console.print(f"Sorry {self.player_1}, {answer} is out of bound!", style='error')
            return None

        return [key for key in self.rolls.keys()][selected_index]

    def check_for_winner(self, roll1, roll2):
        winner = None

        outcome = self.rolls.get(roll1, {})
        if roll2 in outcome.get("defeats"):
            winner = self.player_1
        elif roll2 in outcome.get("defeated_by"):
            winner = self.player_2

        return winner

    def find_winner(self):
        names = self.wins.keys()
        for name in names:
            if self.wins.get(name, 0) >= self.round:
                return name
        return None

    def play_game(self):
        self.log(f"New game starting between {self.player_1} and {self.player_2}.")
        while not self.find_winner():
            roll1 = self.get_roll()
            roll2 = random.choice([*self.rolls.keys()])

            if roll1 is None:
                console.print("Try again!", style='others')
                continue

            self.clear_screen()
            self.log(f"Round: {self.player_1} roll {roll1} and {self.player_2} rolls {roll2}")
            print(cli_box.rounded(f"{Fore.LIGHTBLUE_EX}{self.player_1} roll {roll1}\n"
                                  f"{Fore.LIGHTCYAN_EX}{self.player_2} rolls {roll2}"))

            winner = self.check_for_winner(roll1, roll2)

            if winner is None:
                msg = "This round was a Tie!"
                console.print(msg, style='tie')
                self.log(msg)
            else:
                msg = f"{winner} take the round!"
                console.print(msg, style='win')
                self.log(msg)
                if winner == self.player_1:
                    self.wins[winner] += 1
                elif winner == self.player_2:
                    self.wins[winner] += 1

            msg = f"Score>> {self.player_1}: {self.wins[self.player_1]} - " \
                  f"{self.player_2}: {self.wins[self.player_2]}."
            console.print(msg, style='slate_blue1 underline')
            self.log(msg)
            print()

        overall_winner = self.find_winner()
        msg = f"{overall_winner} wins the game!"
        console.print(msg, style='win')
        self.log(msg)
        self.record_wins(overall_winner)

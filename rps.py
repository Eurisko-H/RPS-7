import random
import os
import json


class RPS:
    def __init__(self, player_1: str, player_2: str, rounds: int):
        self.player_1 = player_1
        self.player_2 = player_2
        self.round = rounds
        self.wins = {player_1: 0, player_2: 0}
        self.rolls = {}

        self.load_rolls()
        self.show_leaderboard()
        print("---------------------------")
        print(" Rock Paper Scissors")
        print("---------------------------")

    def load_rolls(self):
        directory = os.path.dirname(__file__)
        file_name = os.path.join(directory, 'rolls.json')

        with open(file_name, 'r', encoding='utf-8') as fin:
            self.rolls = json.load(fin)

    @staticmethod
    def load_leaders():
        directory = os.path.dirname(__file__)
        file_name = os.path.join(directory, 'leaderboard.json')

        if not os.path.exists(file_name):
            return {}

        with open(file_name, 'r', encoding='utf-8') as fin:
            return json.load(fin)

    def show_leaderboard(self):
        leaders = self.load_leaders()

        sorted_leaders = [*leaders.items()]
        sorted_leaders.sort(key=lambda l: l[1], reverse=True)

        for name, wins in sorted_leaders:
            print(f"{name} wins:{wins}")

    def record_wins(self, winner):
        leaders = self.load_leaders()

        if winner in leaders:
            leaders[winner] += 1
        else:
            leaders[winner] = 1

        directory = os.path.dirname(__file__)
        file_name = os.path.join(directory, 'leaderboard.json')

        with open (file_name, 'w', encoding='utf-8') as fin:
            json.dump(leaders, fin)

    def get_roll(self):
        print("Available rolls")
        for index, roll in enumerate(self.rolls.keys(), start=1):
            print(f"{index}. {roll}")

        answer = input(f"{self.player_1}, what is your roll? ")
        if not answer.isdigit():
            print(f"Sorry {self.player_1}, {answer} is not a digit!")
            return None

        selected_index = int(answer) - 1
        if selected_index < 0 or selected_index >= len(self.rolls.keys()):
            print(f"Sorry {self.player_1}, {answer} is out of bound!")
            return None

        return [key for key in self.rolls.keys()][selected_index]

    def check_for_winner(self, roll1, roll2):
        winner = None
        if roll1 == roll2:
            print("The play was tied!")

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
        while not self.find_winner():
            roll1 = self.get_roll()
            roll2 = random.choice([*self.rolls.keys()])

            if roll1 is None:
                print("Try again!")
                continue

            print(f"{self.player_1} roll {roll1}")
            print(f"{self.player_2} rolls {roll2}")

            winner = self.check_for_winner(roll1, roll2)

            if winner is None:
                print("This round was a Tie!")
            else:
                print(f"{winner} take the round!")
                if winner == self.player_1:
                    self.wins[winner] += 1
                elif winner == self.player_2:
                    self.wins[winner] += 1

            print(f"Score is {self.player_1}: {self.wins[self.player_1]}"
                  f" and {self.player_2}: {self.wins[self.player_2]}.")
            print()

        overall_winner = self.find_winner()
        print(f"{overall_winner} wins the game!")
        self.record_wins(overall_winner)


rps = RPS("hasan", "CPU", 3)
rps.play_game()

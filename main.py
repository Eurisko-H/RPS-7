import random


class RPS:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.round = 3
        self.wins_p1 = 0
        self.wins_p2 = 0

        self.rolls = ['rock', 'paper', 'scissors']

        print("---------------------------")
        print(" Rock Paper Scissors")
        print("---------------------------")

    @staticmethod
    def get_roll(player, rolls):
        print("Available rolls")
        for i, roll in enumerate(rolls, start=1):
            print(f"{i}. {roll}")

        answer = input(f"{player}, what is your roll? ")
        if not answer.isdigit():
            print(f"Sorry {player}, {answer} is not a digit!")
            return None
        answer = int(answer)
        if answer < 0 or answer > len(rolls):
            print(f"Sorry {player}, {answer} is out of bound!")
            return None

        return rolls[answer - 1]

    @staticmethod
    def check_for_winner(player_1, player_2, roll1, roll2):
        winner = None
        if roll1 == roll2:
            print("The play was tied!")
        elif roll1 == 'rock':
            if roll2 == 'paper':
                winner = player_2
            elif roll2 == 'scissors':
                winner = player_1
        elif roll1 == 'paper':
            if roll2 == 'scissors':
                winner = player_2
            elif roll2 == 'rock':
                winner = player_1
        elif roll1 == 'scissors':
            if roll2 == 'rock':
                winner = player_2
            elif roll2 == 'paper':
                winner = player_1
        return winner

    def play_game(self):
        while self.wins_p1 < self.round and self.wins_p2 < self.round:
            roll1 = self.get_roll(self.player_1, self.rolls)
            roll2 = random.choice(self.rolls)

            if roll1 is None:
                print("Try again!")
                continue

            print(f"{self.player_1} roll {roll1}")
            print(f"{self.player_2} rolls {roll2}")

            winner = self.check_for_winner(self.player_1, self.player_2, roll1, roll2)

            if winner is None:
                print("This round was a Tie!")
            else:
                print(f"{winner} take the round!")
                if winner == self.player_1:
                    self.wins_p1 += 1
                elif winner == self.player_2:
                    self.wins_p2 += 1

            print(f"Score is {self.player_1}: {self.wins_p1} and {self.player_2}: {self.wins_p2}.")
            print()

        if self.wins_p1 >= self.round:
            overall_winner = self.player_1
        else:
            overall_winner = self.player_2

        print(f"{overall_winner} wins the game!")


rps = RPS('You', 'CPU')
rps.play_game()

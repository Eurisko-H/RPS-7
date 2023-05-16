from rps import RPS
from colorama import Fore, init, Style
import time
import sys
import os


init()


def tprint(words):
    for char in words:
        time.sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()


intro_ascii = f"""{Fore.RED}
   __    ___  __     _____ 
  /__\  / _ \/ _\   {Fore.BLUE}|___  |
 / \// / /_)/\ \ _____ {Fore.GREEN}/ / 
/ _  \/ ___/ _\ \_____{Fore.YELLOW}/ /  
\/ \_/\/     \__/    {Fore.MAGENTA}/_/   
                                            
{Style.RESET_ALL}"""


def intro():
    clear_screen()
    tprint(intro_ascii)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    intro()
    user_name = input("What's your name: ")
    rps = RPS(user_name, "CPU", 3)
    rps.play_game()


if __name__ == "__main__":
    main()

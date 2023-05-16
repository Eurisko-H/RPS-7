import json
import platform
import datetime
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


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rps.log')

    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f"[{datetime.datetime.now().date().isoformat()}] ")
        fout.write(msg)
        fout.write('\n')


def main():
    try:
        if platform.system() == 'Windows':
            init(autoreset=True)

        intro()
        log('App starting up')
        user_name = input("What's your name: ")
        log(f"{user_name} has logged in.")
        rps = RPS(user_name, "CPU", 3)
        rps.play_game()
        log("Game over.")

    except json.decoder.JSONDecodeError as je:
        print()
        print(f"{Fore.LIGHTRED_EX}ERROR: The file rolls.json is invalid JSON.{Fore.LIGHTRED_EX}")
        print(f"{Fore.LIGHTRED_EX}ERROR: {je}{Fore.LIGHTWHITE_EX}")

    except FileNotFoundError as fe:
        print()
        print(f"{Fore.LIGHTWHITE_EX}ERROR: Rolls file not found{Fore.LIGHTWHITE_EX}")
        print(f"{Fore.LIGHTRED_EX}ERROR: {fe}{Fore.LIGHTWHITE_EX}")

    except KeyboardInterrupt:
        print()
        print(f"{Fore.LIGHTCYAN_EX}You gotta run? Ok, cya next time!{Fore.LIGHTWHITE_EX}")

    except Exception as x:
        print(f"{Fore.LIGHTWHITE_EX}Unknown error: {x}{Fore.LIGHTWHITE_EX}")


if __name__ == "__main__":
    main()

import random
import csv 
from datetime import datetime

# Function to write data in CSV file
def write_to_csv(username, attempts, level): 
    with open('numbersgame.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, attempts, level, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]) #strftime()

# Level 1: Standard number guessing game 

def level_1(username):
    print("\n--- Level 1: Guess the number between 1 and 100 ---")
    print("\nType 'menu' at any time to return back to main menu\n")
    target_number = random.randint(1, 100)
    attempts = 0
    while True:
        user_guess = str(input("Enter your guess:"))
        if user_guess.lower() == "menu":
            print("Returning to the main menu...")
            break

        try: #try: except:
            user_guess = int(user_guess)
            attempts += 1
            if target_number > user_guess:
                print("Too low!")
            elif target_number < user_guess:
                print("Too high!")
            else:
                print(f"Congratulations {username}! You have guessed the number in {attempts} attempts.")
                write_to_csv(username, attempts, 1)
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")

# Level 2: Advanced number guessing game

def level_2(username):
    print("\n--- Level 2: Guess the number beetween 1 and 100.... but the number changes every time you guess ;) ---")
    print("\nType 'menu' at any time to return back to main menu\n")
    numbers = list(range(1, 101))
    target_number = random.randint(1, 100)
    attempts = 0
    while True:
        user_guess = str(input("Enter your guess:")) #Invalid input problem might be related to assigning user_guess as string 
        if user_guess.lower() == "menu":
            print("Returning to the main menu...")
            break
        try:
            user_guess = int(user_guess)
            attempts += 1
            if user_guess != target_number:
                print("Not quite!")
            else:
                print(f"Congratulations {username}! You have guessed the number in {attempts} attempts.")
                write_to_csv(username, attempts, 2)
                break
            
            numbers.remove(target_number)
            if len(numbers) == 0:
                print("You have guessed all numbers. Starting a new game...")
                break
            
            target_number = random.randint(1, 100)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")

# Level 3: Code breaker

def level_3(username):
    print("\n--- Level 3: Code Breaker ---")
    print("\nType 'menu' at any time to return back to main menu\n")
    program_number = random.randint(100, 999)
    attempts = 0
    while True:
        user_guess = input("Enter your 3-digit guess: ")
        if user_guess.lower() == "menu":
            print("Returning to the main menu...")
            break
        try:
            user_guess = str(user_guess)
            if len(user_guess) != 3 or not user_guess.isdigit(): #isdigit()
                raise ValueError("Invalid input. Please enter a 3-digit number.") #raise
        except ValueError as e:
            print(e)
            continue
        attempts += 1

        correct_spot = 0
        wrong_spot = 0
        wrong_number = 0

        program_number_numbers = list(str(program_number))
        user_guess_numbers = list(str(user_guess))

        for i in range(3): 
            if user_guess_numbers[i] == program_number_numbers[i]:
                correct_spot += 1 
                program_number_numbers[i] = user_guess_numbers[i] = None #Chat GPT told me to do this and I dont fully understand why
    
        for i in range(3): 
            if program_number_numbers[i] is not None and program_number_numbers[i] in user_guess_numbers:
                wrong_spot += 1
                user_guess_numbers[user_guess_numbers.index(program_number_numbers[i])] = None
            elif user_guess_numbers[i] is not None:
                wrong_number += 1

        if correct_spot == 3:
            print(f"Congratulations {username}! You have guessed the number in {attempts} attempts.")
            write_to_csv(username, attempts, 3)
            break
        else:
            print(f"{correct_spot} correct spot(s), {wrong_spot} wrong spot(s), {wrong_number} wrong number(s) at the wrong spot.")
            
# Main menu (suggested by Chat GPT)

def main_menu():
    print("Welcome to the number guessing game!")
    username = input("Enter your username: ")
    while True:
        print("\nMain Menu:")
        print("1. Level 1: Standard number guessing game")
        print("2. Level 2: Advanced number guessing game")
        print("3. Level 3: Code Breaker")
        print("4. Quit")
        choice = input("Enter your choice:")
        if choice == '1':
            level_1(username)
        elif choice == '2':
            level_2(username)
        elif choice == '3':
            level_3(username)
        elif choice == '4':
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")

def main():
    while True:
        main_menu()
        replay = input("Do you want to play again? (yes/no): ").lower
        if replay != 'yes':
            print("Thank you for playing!")
            break

if __name__ == '__main__':
    main_menu()


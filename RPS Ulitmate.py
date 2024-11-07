import random
import json


# Global Variables
insta_win_mode = False  # Flag to track Insta-Win Mode


# Define items and their winning relationships
items = ["Rock", "Paper", "Scissors", "Lizard", "Spock", "Fire", "Water", "Air", "Lightning", "Earth", "Combustion"]

winning_relationships = {
    "Rock": ["Scissors", "Lizard", "Fire"],
    "Paper": ["Rock", "Spock", "Air"],
    "Scissors": ["Paper", "Lizard", "Air"],
    "Lizard": ["Spock", "Paper", "Water"],
    "Spock": ["Scissors", "Rock", "Lightning"],
    "Fire": ["Paper", "Lizard", "Air"],
    "Water": ["Fire", "Rock", "Lightning"],
    "Air": ["Water", "Lightning", "Fire"],
    "Lightning": ["Rock", "Scissors", "Spock"],
    "Earth": ["Air", "Water"],
    "Combustion": ["Earth", "Lizard", "Water"]
}

# Initialize scores and currency
player_score = 0
ai_score = 0
ties = 0
coins = 10  # Starting coins for the player

# Updated Inventory with no rollable items
inventory = {
    "Luck Bringer": {"quantity": 0, "description": "Increases win chance by 10%"},
    "Lucky Coin": {"quantity": 0, "description": "Increases coin rewards by 20%"},
    "Four Leaf Clover": {"quantity": 0, "description": "Increases chance of winning in a tie"}
}


# Save and load functions for game state
def save_game():
    data = {
        "player_score": player_score,
        "ai_score": ai_score,
        "ties": ties,
        "coins": coins,
        "inventory": inventory
    }
    with open("game_save.json", "w") as file:
        json.dump(data, file)
    print("Game saved successfully!")

def load_game():
    global player_score, ai_score, ties, coins, inventory
    try:
        with open("game_save.json", "r") as file:
            data = json.load(file)
            player_score = data["player_score"]
            ai_score = data["ai_score"]
            ties = data["ties"]
            coins = data["coins"]
            inventory = data["inventory"]
        print("Game loaded successfully!")
    except FileNotFoundError:
        print("No saved game found, starting a new game.")
    
    
        # Function to start a new game
def new_game():
    global player_score, ai_score, ties, coins, inventory
    player_score = 0
    ai_score = 0
    ties = 0
    coins = 10  # Starting coins for the new game
    inventory = {
        "Luck Bringer": {"quantity": 0, "description": "Increases win chance by 10%"},
    }
    print("\nNew game started! All progress has been reset.")

        
        
        # Developer Menu Function
def dev_menu():
    global coins
    print("\n--- Developer Menu ---")
    print("1. Add Coins")
    print("2. Grant Insta-Win (Auto-Win Mode)")
    print("3. Exit Dev Menu")
    
    while True:
        choice = input("Choose an option: ")
        
        if choice == "1":
            try:
                amount = int(input("Enter the amount of coins to add: "))
                coins += amount
                print(f"Added {amount} coins. Total coins: {coins}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "2":
            global insta_win_mode
            insta_win_mode = True
            print("Insta-Win Mode activated! You will now win every round.")
        elif choice == "3":
            print("Exiting Dev Menu.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


# Function to display inventory with descriptions
def view_inventory():
    print("\n--- Your Inventory ---")
    for item, details in inventory.items():
        print(f"{item}: {details['quantity']} - {details['description']}")

# Function for the shop
# Updated shop items without rollable items
def shop():
    global coins, inventory
    print("\n--- Welcome to the Shop ---")
    print("1. Luck Bringer - 15 coins (Increases win chance by 10%)")
    print("2. Lucky Coin - 30 coins (Increases coin rewards by 20%)")
    print("3. Four Leaf Clover - 40 coins (Increases chance of winning in a tie)")
    print("4. Exit Shop")
    
    choice = input("Choose an item to buy or '4' to exit: ")
    
    if choice == "1":
        if coins >= 15:
            coins -= 15
            inventory["Luck Bringer"]["quantity"] += 1
            print("You bought a Luck Bringer!")
        else:
            print("Not enough coins!")
    elif choice == "2":
        if coins >= 30:
            coins -= 30
            inventory["Lucky Coin"] = {"quantity": 1, "description": "Increases coin rewards by 20%"}
            print("You bought a Lucky Coin!")
        else:
            print("Not enough coins!")
    elif choice == "3":
        if coins >= 40:
            coins -= 40
            inventory["Four Leaf Clover"] = {"quantity": 1, "description": "Increases chance of winning in a tie"}
            print("You bought a Four Leaf Clover!")
        else:
            print("Not enough coins!")
    elif choice == "4":
        print("Leaving the shop.")
    else:
        print("Invalid choice.")

    
# Function to simulate a round with potential luck boost
# Modify play_round to check for insta_win_mode
def play_round(player_choice):
    global player_score, ai_score, ties, coins
    
    # Check if Insta-Win Mode is active
    if insta_win_mode:
        print("Insta-Win Mode active! You win this round automatically!")
        player_score += 1
        coins += 5  # Earn 5 coins per win
        return
    
    # AI makes a random choice with a small chance of bias if Luck Bringer is owned
    if inventory["Luck Bringer"]["quantity"] > 0 and random.random() < 0.1:  # 10% win chance boost
        ai_choice = random.choice([item for item in items if item in winning_relationships[player_choice]])
    else:
        ai_choice = random.choice(items)
    
    print(f"\nYou chose: {player_choice}")
    print(f"AI chose: {ai_choice}")
    
    # Determine the outcome
    if player_choice == ai_choice:
        print("It's a tie!")
        ties += 1
    elif ai_choice in winning_relationships[player_choice]:
        print("You win this round!")
        player_score += 1
        coins += 5  # Earn 5 coins per win
    else:
        print("AI wins this round!")
        ai_score += 1


# Function for Auto Roll Machine
# Updated Auto Roll Machine that only gives luck-based items and coins
def auto_roll():
    global coins
    if coins < 100:
        print("Not enough coins to use the Roll Machine!")
        return

    # Deduct the cost
    coins -= 100
    reward = random.choice([
        "Coins", 
        "Luck Bringer", 
        "Lucky Coin", 
        "Four Leaf Clover"
    ])
    
    if reward == "Coins":
        gained_coins = random.randint(110 , 250)
        coins += gained_coins
        print(f"The Roll Machine awarded you {gained_coins} coins!")
    elif reward == "Luck Bringer":
        inventory["Luck Bringer"]["quantity"] += 1
        print("The Roll Machine awarded you a Luck Bringer!")
    elif reward == "Lucky Coin":
        inventory["Lucky Coin"]["quantity"] += 1
        print("The Roll Machine awarded you a Lucky Coin!")
    elif reward == "Four Leaf Clover":
        inventory["Four Leaf Clover"]["quantity"] += 1
        print("The Roll Machine awarded you a Four Leaf Clover!")
    else:
        print("The Roll Machine gave you... nothing. Better luck next time!")

# Main game loop

# Main game loop with secret mod menu option
# In the main game loop, add a new option for the user to start a new game:
def game():
    global player_score, ai_score, ties, coins, insta_win_mode
    load_game()  # Load game state at the start
    insta_win_mode = False  # Initialize Insta-Win mode to off
    print("Welcome to Rock, Paper, Scissors Ultimate!")
    print("Choices:", ", ".join(items))

    while True:
        # Display current scores and currency
        print(f"\nScore: You - {player_score} | AI - {ai_score} | Ties - {ties}")
        print(f"Coins: {coins}")
        
        # Ask if the player wants to enter the shop, play a round, view inventory, or use the auto roll
        action = input("Type 'play' to play a round, 'shop' for the shop, 'inventory' to view items, 'roll' for the auto roll machine, 'save' to save the game, 'new' to start a new game, or 'exit' to quit: ").lower()
        
        if action == "exit":
            break
        elif action == "new":
            new_game()  # Start a new game
        elif action == "secret":
            dev_menu()  # Call dev_menu function to open the developer menu
        elif action == "shop":
            shop()
        elif action == "inventory":
            view_inventory()
        elif action == "play":
            player_choice = input("\nChoose your item: ").capitalize()
            if player_choice not in items:
                print("Invalid choice, please try again.")
                continue
            play_round(player_choice)
        elif action == "roll":
            auto_roll()
        elif action == "save":
            save_game()
        else:
            print("Invalid input, please try again.")

    # Final score display and save on exit
    print("\nGame Over!")
    print(f"Final Score: You - {player_score} | AI - {ai_score} | Ties - {ties}")
    print(f"Coins collected: {coins}")
    save_game()

    # Final score display and save on exit
    print("\nGame Over!")
    print(f"Final Score: You - {player_score} | AI - {ai_score} | Ties - {ties}")
    print(f"Coins collected: {coins}")
    save_game()


# Run the game
game()


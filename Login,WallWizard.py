import uuid
import bcrypt
import re
import json
import os
import getpass
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

console = Console()

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'nt':
        os.system('cls')

# Function to validate email format
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Function to load users from the JSON file
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to load game history
def load_game_history():
    try:
        with open("games.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save users to the JSON file
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Function to save game history
def save_game_history(games):
    with open("games.json", "w") as file:
        json.dump(games, file, indent=4)

def display_login_table():
    table = Table(title="[bold magenta]Login Menu[/bold magenta]", show_header=True, header_style="bold yellow", padding=(0, 2))
    table.add_column("Option", style="bold cyan", justify="center")
    table.add_column("Description", style="bold green", justify="center")
    table.add_row("1", "Register a new user")
    table.add_row("2", "Login")
    table.add_row("3", "Exit")
    console.print(table)

def display_registration_table():
    table = Table(title="[bold yellow]Registration Fields[/bold yellow]", show_header=True, header_style="bold green", padding=(0, 2))
    table.add_column("Field", style="bold cyan", justify="center")
    table.add_column("Description", style="bold magenta", justify="center")
    table.add_row("Username", "Unique username for the user")
    table.add_row("Email", "Valid email address")
    table.add_row("Password", "Password must be at least 8 characters long")
    console.print(table)

def display_main_menu_table():
    table = Table(title="[bold cyan]Main Menu[/bold cyan]", show_header=True, header_style="bold yellow", padding=(0, 2))
    table.add_column("Option", style="bold cyan", justify="center")
    table.add_column("Action", style="bold green", justify="center")
    table.add_row("1", "Start New Game")
    table.add_row("2", "Continue Game")
    table.add_row("3", "View Game History")
    table.add_row("4", "View Leaderboard")
    table.add_row("5", "Exit")
    console.print(table)

def signin_user():
    users = load_users()

    while True:
        display_signin_table()
        username = Prompt.ask("[bold yellow]Enter username (or b to go back)[/bold yellow]", default="", show_default=False)
        if username == 'b':
            clear_screen()
            return 
        if username in users:
            console.print("Error: Username already exists.", style="bold underline red", justify="center")
            continue

        email = Prompt.ask("[bold yellow]Enter email (or b to go back)[/bold yellow]", default="", show_default=False)
        if email == 'b':
            clear_screen()
            return
        if not validate_email(email):
            console.print("Error: Invalid email format.", style="bold underline red", justify="center")
            continue
        if any(user['email'] == email for user in users.values()):
            console.print("Error: Email already exists.", style="bold underline red", justify="center")
            continue

        while True:
            password = getpass.getpass("Enter password (more than 8 characters, or b to go back):")
            if password == 'b':
                clear_screen()
                return
            if len(password) < 8:
                console.print("Error: Password must be at least 8 characters.", style="bold underline red", justify="center")
                continue

            password_confirm = getpass.getpass("Confirm password: ")
            if password != password_confirm:
                console.print("Error: Passwords do not match. Please try again.", style="bold underline red", justify="center")
                continue
            break

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        users[user_id] = {
            "username": username,
            "password": hashed_password.decode('utf-8')
            "email": email
        }

        save_users(users)
        console.print("Registration successful!", style="bold underline green", justify="center")
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        break

# Function to login a user
def login_user():
    console.print(Panel("[bold magenta]=== Login ===", style="bold magenta"))
    users = load_users()

    while True:
        username = Prompt.ask("[bold magenta]Enter username (or b to go back)[/bold magenta]", default="", show_default=False)
        if username == 'b':
            clear_screen()
            return
        user = None
        for user_id, data in users.items():
            if data["username"] == username:
                user = data
                break

        if user is None:
            console.print("Error: Username does not exist.", style="bold underline red", justify="center")
            continue

        password = getpass.getpass("Enter password (or b to go back): ")
        if password == 'b':
            clear_screen()
            return 
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            console.print("Error: Incorrect password.", style="bold underline red", justify="center")
            continue

        console.print("Login successful!", style="bold underline green", justify="center")
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        main_menu(username)
        break

# Function to display the main menu
def main_menu(username):
    while True:
        clear_screen()
        display_main_menu_table()

        choice = Prompt.ask("[bold yellow]Enter choice[/bold yellow]", default="", show_default=False)
        if choice == '1':
            start_new_game(username)
        elif choice == '2':
            continue_game()
        elif choice == '3':
            view_game_history()
        elif choice == '4':
            view_leaderboard()
        elif choice == '5':
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]", justify="center")

# Main Menu
def main():
    while True:
        clear_screen()
        display_login_table()

        choice = Prompt.ask("[bold yellow]Enter choice[/bold yellow]", default="", show_default=False)
        if choice == '1':
            clear_screen()
            register_user()
        elif choice == '2':
            clear_screen()
            login_user()
        elif choice == '3':
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]", justify="center")
            Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
            
if __name__ == "__main__":
    main()

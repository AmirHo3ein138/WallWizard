import uuid
import bcrypt
import re
import json
import os
import msvcrt
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def clear_screen():
    if os.name == 'nt':
        os.system('cls')

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def create_player_file(username, user_data):
    players_folder = "players"
    if not os.path.exists(players_folder):
        os.makedirs(players_folder)

    player_file_path = os.path.join(players_folder, f"{username}.json")
    with open(player_file_path, "w") as file:
        json.dump(user_data, file, indent=4)

def load_user(username):
    player_file_path = os.path.join("players", f"{username}.json")
    if os.path.exists(player_file_path):
        with open(player_file_path, "r") as file:
            return json.load(file)
    return None

def display_login_table():
    table = Table(title="[bold magenta]==| Login Menu |==[/bold magenta]")
    table.add_column("Field", style="bold magenta", justify="center")
    table.add_column("Description", style="bold magenta", justify="center")
    table.add_row("Username", "Unique username for the user")
    table.add_row("Email", "Valid email address")
    table.add_row("Password", "Password must be at least 8 characters long")
    console.print(table)

def display_entry_table():
    table = Table(title="[bold cyan]==| Entry Menu |==[/bold cyan]", show_header=True, header_style="bold cyan", padding=(0, 2))
    table.add_column("Option", style="bold cyan", justify="center")
    table.add_column("Description", style="bold cyan", justify="center")
    table.add_row("1", "SignIn")
    table.add_row("2", "Login")
    table.add_row("3", "Exit")
    console.print(table)

def display_signin_table():
    table = Table(title="[bold blue]==|Terms|==[/bold blue]", show_header=True, header_style="bold blue", padding=(0, 2))
    table.add_column("Field", style="bold blue", justify="center")
    table.add_column("Description", style="bold blue", justify="center")
    table.add_row("Username", "Unique username for the user")
    table.add_row("Email", "Valid email address")
    table.add_row("Password", "Password must be at least 8 characters long")
    console.print(table)

def display_main_menu_table():
    table = Table(title="[bold cyan]Main Menu[/bold cyan]", show_header=True, header_style="bold yellow", padding=(0, 2))
    table.add_column("Option", style="bold cyan", justify="center")
    table.add_column("Action", style="bold green", justify="center")
    table.add_row("1", "Start New Game")
    table.add_row("2", "View Game History")
    table.add_row("3", "View Leaderboard")
    table.add_row("4", "Exit")
    console.print(table)

def get_password(prompt):
    console.print(prompt, end='', style="bold blue")
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b'\r':
            print()
            break
        elif char == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end='', flush=True)
        else:
            password += char.decode('utf-8')
            print("*", end='', flush=True)
    return password

def register_user():
    while True:
        display_signin_table()
        username = Prompt.ask("[bold blue]Enter username (or b to go back)[/bold blue]", default="", show_default=False)
        if username == 'b':
            clear_screen()
            return 
        if load_user(username):
            console.print("Error: Username already exists.", style="bold underline red")
            continue

        email = Prompt.ask("[bold blue]Enter email (or b to go back)[/bold blue]", default="", show_default=False)
        if email == 'b':
            clear_screen()
            return 
        if not validate_email(email):
            console.print("Error: Invalid email format.", style="bold underline red")
            continue

        while True:
            password = get_password("Enter password (more than 8 characters, or b to go back): ")
            if password == 'b':
                clear_screen()
                return
            if len(password) < 8:
                console.print("Error: Password must be at least 8 characters.", style="bold underline red", justify="center")
                continue

            password_confirm = get_password("Confirm password: ")
            if password != password_confirm:
                console.print("Error: Passwords do not match. Please try again.", style="bold underline red", justify="center")
                continue
            break

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": username,
            "password": hashed_password.decode('utf-8'),
            "email": email
        }

        create_player_file(username, user_data)

        console.print("Everything is set to play!", style="bold underline green", justify="center")
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        break

def login_user():
    display_login_table()

    while True:
        username = Prompt.ask("[bold magenta]Enter username (or b to go back)[/bold magenta]", default="", show_default=False)
        if username == 'b':
            clear_screen()
            return

        user = load_user(username)
        if not user:
            console.print("Error: Username does not exist.", style="bold underline red", justify="center")
            continue

        password = get_password("[bold magenta]Enter password (or b to go back): [/bold magenta]")
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

def main_menu(username):
    while True:
        clear_screen()
        display_main_menu_table()

        choice = Prompt.ask("[bold yellow]Enter choice[/bold yellow]", default="", show_default=False)
        if choice == '1':
            console.print("Starting new game...", style="bold green")
        elif choice == '2':
            console.print("Viewing game history...", style="bold green")
        elif choice == '3':
            console.print("Viewing leaderboard...", style="bold green")
        elif choice == '4':
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]", justify="center")

def main():
    while True:
        clear_screen()
        display_entry_table()

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

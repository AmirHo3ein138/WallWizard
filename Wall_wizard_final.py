import sys
import bcrypt
import uuid
import time
import re
import json
import os
import msvcrt
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from colorama import Fore, Style
import sys

def safe_input(prompt=""):
    try:
        return input(prompt)
    except RuntimeError:
        
        sys.stdout.write(prompt)
        return sys.stdin.readline().strip()

class ColoredTableCharacters:
    def __init__(self):
        self.reset = Style.RESET_ALL
        self.horizontal_simple = f"{Fore.CYAN}\u2501{self.reset}"
        self.vertical_simple = f"{Fore.CYAN}\u2503{self.reset}"
        self.plus_simple = f"{Fore.CYAN}\u254b{self.reset}"
        self.plus_between_walls_h = f"{Fore.RED}\u254b{self.reset}"
        self.plus_between_walls_v = f"{Fore.RED}\u2542{self.reset}"
        self.vertical_wall = f"{Fore.RED}\u2503{self.reset}"  
        self.horizontal_wall = f"{Fore.RED}\u2501{self.reset}"
        self.white_piece = f"{Fore.WHITE}\u2659{self.reset}"
        self.red_piece = f"{Fore.RED}\u2659{self.reset}"
table_chars = ColoredTableCharacters()
normal_h = table_chars.horizontal_simple
normal_v = table_chars.vertical_simple
wall_h = table_chars.horizontal_wall
wall_v = table_chars.vertical_wall
hashtag_v = table_chars.plus_between_walls_v
hashtag_h = table_chars.plus_between_walls_h
plus = table_chars.plus_simple
red_player = table_chars.red_piece
white_player = table_chars.white_piece
logged_in_user = []
player_piece = {}

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print("[bold white]     In the name of GOD[/bold white]")
    console.print("        made by RASM",style="bold red")
    print('----------------------------')

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

def load_user1(username):
    player_file_path = os.path.join("players", f"{username}.json")
    if os.path.exists(player_file_path):
        with open(player_file_path, "r") as file:
            return json.load(file)
    return None

def load_user2(username):
    player_file_path = os.path.join("players", f"{username}.json")
    if os.path.exists(player_file_path):
        with open(player_file_path, "r") as file:
            return json.load(file)
    return None

def update_player_stats(winner, loser):
    winner_data = load_user1(winner)
    loser_data = load_user1(loser)
    
    winner_data["wins"] = winner_data.get("wins", 0) + 1
    loser_data["losses"] = loser_data.get("losses", 0) + 1

    create_player_file(winner, winner_data)
    create_player_file(loser, loser_data)

def print_board(a, ply):
    col_numbers = "  " + "  ".join(f"{i:2}" for i in range(1,9))
    print(col_numbers)
    end_line_number = 1
    for i in range(17):
        board=""
        for j in range(17):
            board+=a[i][j]
        if i%2==0:
            board+=a[i][17]
            print(board)
        else:
            
            for i in range(1):
                end_line_number +=1
            print(board, end_line_number-1)
    if ply == 2:
        print(f"Red player's turn ({red_player}):")
    else:
        print(f"White player's turn ({white_player})")

def get_leaderboard_data():
    players_folder = "players"
    leaderboard = []

    if os.path.exists(players_folder):
        for filename in os.listdir(players_folder):
            if filename.endswith(".json"):
                player_file_path = os.path.join(players_folder, filename)
                with open(player_file_path, "r") as file:
                    player_data = json.load(file)
                    leaderboard.append({
                        "username": player_data.get("username", "Unknown"),
                        "wins": player_data.get("wins", 0),
                        "losses": player_data.get("losses", 0)
                    })


    leaderboard.sort(key=lambda x: (-x["wins"], x["losses"]))
    return leaderboard

def view_leaderboard():
    leaderboard = get_leaderboard_data()

    if not leaderboard:
        console.print("No players found! Leaderboard is empty.", style="bold red", justify="center")
        Prompt.ask("[bold yellow]Press Enter to return to the main menu...[/bold yellow]")
        return

    
    table = Table(title="[bold green]==| Leaderboard |==[/bold green]", show_header=True, header_style="bold cyan")
    table.add_column("Rank", justify="center")
    table.add_column("Username", justify="center")
    table.add_column("Wins", justify="center")
    table.add_column("Losses", justify="center")

    for rank, player in enumerate(leaderboard, start=1):
        table.add_row(
            str(rank),
            player["username"],
            str(player["wins"]),
            str(player["losses"])
        )

    console.print(table)
    Prompt.ask("[bold yellow]Press Enter to return to the main menu...[/bold yellow]")


def dfsFunction(x,y,a,p):
    table_chars = ColoredTableCharacters()

    
    ky=0
    dfs=[[y,x]]
    while True:
        k=0
        if y!=0:
            if a[y-1][x-1]==(3 * normal_h) and y>=2 and dfs.count([y-2,x])==0 and dfs.count([y-2,x,"t"])==0:
                dfs.append([y-2,x])
        if y!=16:
            if a[y+1][x-1]==(3 * normal_h) and y<=15 and dfs.count([y+2,x])==0 and dfs.count([y+2,x,"t"])==0:
                dfs.append([y+2,x])
        if x!=17:
            if a[y][x+1]==(" "+normal_v+" ") and x<=15 and dfs.count([y,x+2])==0 and dfs.count([y,x+2,"t"])==0:
                dfs.append([y,x+2])
        if a[y][x-1]==(" "+normal_v+" ") and x>=2 and dfs.count([y,x-2])==0 and dfs.count([y,x-2,"t"])==0:
            dfs.append([y,x-2])
        dfs[dfs.index([y,x])].append("t")
        for i in range(len(dfs)):
            if dfs[i].count("t")==0:
                y=dfs[i][0]
                x=dfs[i][1]
                break
            elif i==len(dfs)-1:
                k=1
        if k==1:
            break
    for i in range(len(dfs)):
        if p==2:
            if dfs[i][0]==16:
                ky=1
                break
        else:
            if dfs[i][0]==0:
                ky=1
                break
    if ky==0:
        return(False)
    else:
        return(True) 


def save_game(game_state):
    save_folder = "saved_games"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    
    save_filename = f"{save_folder}/{int(time.time())}_{uuid.uuid4().hex}.json"

    
    with open(save_filename, "w") as file:
        json.dump(game_state, file, indent=4)

    console.print(f"Game saved successfully! Save file: {save_filename}", style="bold green", justify="center")
def initialize_board():
    ky=0
    a=[]
    counter = 1
    for i in range(17):
        a.append([])
        if i%2==0:
            a[i].append(" ")
            for j in range(9):
                a[i].append(" ")
                if j<8:
                    a[i].append((" "+normal_v+" "))
        else:
            for j in range(9):
                a[i].append(3 * normal_h)
                if j<8:
                    a[i].append(plus)
        counter += 0.5
        a[i].append(f' {int(counter-1)}')
    return a

def load_game():
    save_folder = "saved_games"
    if not os.path.exists(save_folder):
        console.print("No saved games found!", style="bold red", justify="center")
        return None

    
    save_files = [f for f in os.listdir(save_folder) if f.endswith(".json")]
    if not save_files:
        console.print("No saved games found!", style="bold red", justify="center")
        return None

    console.print("Available saved games:", style="bold cyan")
    for idx, save_file in enumerate(save_files, start=1):
        console.print(f"{idx}. {save_file}", style="bold yellow")

    
    choice = Prompt.ask("[bold cyan]Enter the number of the save file to load (or 'b' to go back): [/bold cyan]", default="", show_default=False)
    if choice.lower() == 'b':
        return None

    try:
        choice = int(choice)
        if 1 <= choice <= len(save_files):
            save_file_path = os.path.join(save_folder, save_files[choice - 1])
            with open(save_file_path, "r") as file:
                game_state = json.load(file)
            console.print("Game loaded successfully!", style="bold green", justify="center")
            return game_state
        else:
            console.print("Invalid choice. Returning to the menu.", style="bold red", justify="center")
    except ValueError:
        console.print("Invalid input. Returning to the menu.", style="bold red", justify="center")
    
    return None


def start_game(game_state=None):
    global player_piece
    if game_state:
    # Load saved game state
        a = game_state["board"]  # The game board
        x2, y2 = game_state["red_position"]  # Red player's position
        x1, y1 = game_state["white_position"]  # White player's position
        w2, w1 = game_state["red_walls"], game_state["white_walls"]  # Walls remaining
        ply = game_state["current_turn"]  # Current turn: 1 for red, 2 for white
    else:
    # Initialize a new game
        a = initialize_board()  # Function to set up the board (your existing logic)
        x2, y2 = 9, 0  # Red player's starting position
        x1, y1 = 9, 16  # White player's starting position
        w2, w1 = 10, 10  # Each player has 10 walls initially
        ply = 1  # Current turn: 1 for red, 2 for white
        a[y2][x2] = red_player
        a[y1][x1] = white_player
    
    move="t"
    
    clear_screen()
    print_board(a, ply)
    while move!="n":
        ctr=0
        if ply==2:
            move=safe_input("Enter your move(w, a, s, d or p for place wall|n to exit|[save] to save the game):")
            if move=="w" and y2>0 and a[y2-1][x2-1]!=(3 * wall_h):
                if a[y2-2][x2]!=white_player:
                    a[y2][x2]=" "
                    y2-=2
                    ctr=1
                elif y2>2:
                    if a[y2-3][x2-1]!=(3 * wall_h):
                        a[y2][x2]=" "
                        y2-=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter your move(a, d) : ")
                        if move2move=="a" and x2>2 and a[y2-2][x2-1]!=(" " + wall_v + " "):
                            a[y2][x2]=" "
                            y2-=2
                            x2-=2
                            ctr=1
                        elif move2move=="d" and x2<16 and a[y2-2][x2+1]!=(" " + wall_v + " "):
                            a[y2][x2]=" "
                            y2-=2
                            x2+=2
                            ctr=1
            elif move == "save":
               
                game_state = {
                    "board": a,
                    "red_position": (x2, y2),
                    "white_position": (x1, y1),
                    "red_walls": w2,
                    "white_walls": w1,
                    "current_turn": ply,
                }
                save_game(game_state)  
                console.print("Game saved! You can resume it later.", style="bold green", justify="center")
                continue  
            elif move=="s" and y2<16 and a[y2+1][x2-1]!=(3 * wall_h):
                if a[y2+2][x2]!=white_player:
                    a[y2][x2]=" "
                    y2+=2
                    ctr=1
                elif y2<13:
                    if a[y2+3][x2-1]!=(3 * wall_h):
                        a[y2][x2]=" "
                        y2+=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter your move(a, d) : ")
                        if move2move=="a" and x2>2 and a[y2+2][x2-1]!=(" " + wall_v + " "):
                            a[y2][x2]=" "
                            y2+=2
                            x2-=2
                            ctr=1
                        elif move2move=="d" and x2<16 and a[y2+2][x2+1]!=(" " + wall_v + " "):
                            a[y2][x2]=" "
                            y2+=2
                            x2+=2
                            ctr=1
                        else:
                            console.print("Invalid Input!!!", style="bold red")
            elif move=="a" and x2>1 and a[y2][x2-1]!=(" " + wall_v + " "):
                if a[y2][x2-2]!=white_player:
                    a[y2][x2]=" "
                    x2-=2
                    ctr=1
                elif x2>2:
                    if a[y2][x2-3]!=(" " + wall_v + " "):
                        a[y2][x2]=" "
                        x2-=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter your move(w, s) : ")
                        if move2move=="w" and y2>0 and a[y2-1][x2-1]!=(3 * wall_h):
                            a[y2][x2]=" "
                            x2-=2
                            y2-=2
                            ctr=1
                        elif move2move=="s" and y2<16 and a[y2+1][x2-1]!=(3 * wall_h):
                            a[y2][x2]=" "
                            y2+=2
                            x2-=2
                            ctr=1
            elif move=="d" and x2<16 and a[y2][x2+1]!=(" " + wall_v + " "):
                if a[y2][x2+2]!=white_player:
                    a[y2][x2]=" "
                    x2+=2
                    ctr=1
                elif x2<13:
                    if a[y2][x2+3]!=(" " + wall_v + " "):
                        a[y2][x2]=" "
                        x2+=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter your move(w, s) : ")
                        if move2move=="w" and y2>0 and a[y2-1][x2-1]!=(3 * wall_h):
                            a[y2][x2]=" "
                            x2+=2
                            y2-=2
                            ctr=1
                        elif move2move=="s" and y2<16 and a[y2+1][x2-1]!=(3 * wall_h):
                            a[y2][x2]=" "
                            y2+=2
                            x2+=2
                            ctr=1
                        else:
                            console.print("Invalid move!!!", style="bold red")
            elif move=="p":
                if w2>0:
                    t = safe_input("You have "+str(w2)+" wall(s)\nEnter your wall type (h/v/b for back): ")
                    if t=="v" :
                        xw, yw = map(int,input("Enter the coordinates(x, y): ").split())
                        if xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-2][xw*2]!=(" " + wall_v + " ") and a[yw*2][xw*2]!=(" " + wall_v + " "):
                            a[yw*2-2][xw*2]=(" " + wall_v + " ")
                            a[yw*2][xw*2]=(" " + wall_v + " ")
                            a[yw*2-1][xw*2-1]=hashtag_h
                            ply=1
                            w2-=1
                            clear_screen()
                            print_board(a, ply)
                            if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                                a[yw*2-2][xw*2]=(" "+normal_v+" ")
                                a[yw*2][xw*2]=(" "+normal_v+" ")
                                a[yw*2-1][xw*2-1]=plus
                                clear_screen()
                                ply=2
                                print_board(a, ply)
                                print("Error:\nboarder is close.")
                            
                            w2+=1
                    elif t=="h" :
                        xw, yw = map(int,input("Enter the coordinates(x, y): ").split())
                        if xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-1][xw*2-2]!=(3 * wall_h) and a[yw*2-1][xw*2]!=(3 * wall_h):
                            a[yw*2-1][xw*2-1]=hashtag_h
                            a[yw*2-1][xw*2-2]=(3 * wall_h)
                            a[yw*2-1][xw*2]=(3 * wall_h)
                            ply=1
                            w2-=1
                            clear_screen()
                            print_board(a, ply)
                            if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                                a[yw*2-1][xw*2]=(3 * normal_h)
                                a[yw*2-1][xw*2-2]=(3 * normal_h)
                                a[yw*2-1][xw*2-1]=plus
                                clear_screen()
                                ply=2
                                print_board(a, ply)
                                print("Error:\nboarder is close.")
                                w2+=1
                    elif t=="b":
                        return
                    else:
                        console.print("Invalied move!!!", style="bold red")
                        continue
                else:
                    print("Error:\nYou don't have a wall anymore!")
            elif move!="n":
                print("Error:\nplease enter a valid value.")
            if ctr==1:
                a[y2][x2]=red_player
                ply=1
                clear_screen()
                print_board(a, ply)

            if y2==16:
                    red_username = [user for user, piece in player_piece.items() if piece == "red" ][0]
                    white_username = [user for user, piece in player_piece.items() if piece == "white"][0]
                    console.print(f"🎉 Congratulations, {red_username}! You have won the game 🎉", style="bold green", justify="center")
                    console.print(f"Better luck next time, {white_username}.", style="bold yellow", justify="center")
                    update_player_stats(winner=red_username, loser=white_username)
                    #Prompt.ask("[bold cyan]Press Enter to return to the main menu...[/bold cyan]")
                    safe_input("Press Enter to return to the mein menu...")
                    break
            
            '''if y2==16:
                print("Red player is winner!")
                break'''
        else:
            move=safe_input("Enter your move(w, a, s, d or p for place wall|/[n] to exit|[save] to save the game):")
            if move=="w" and y1>0 and a[y1-1][x1-1]!=(3 * wall_h):
                if a[y1-2][x1]!=red_player:
                    a[y1][x1]=" "
                    y1-=2
                    ctr=1
                elif y1>2:
                    if a[y1-3][x1-1]!=(3 * wall_h):
                        a[y1][x1]=" "
                        y1-=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter four move(a, d) : ")
                        if move2move=="a" and x1>2 and a[y1-2][x1-1]!=(" " + wall_v + " "):
                            a[y1][x1]=" "
                            y1-=2
                            x1-=2
                            ctr=1
                        elif move2move=="d" and x1<16 and a[y1-2][x1+1]!=(" " + wall_v + " "):
                            a[y1][x1]=" "
                            y1-=2
                            x1+=2
                            ctr=1
            elif move=="s" and y1<16 and a[y1+1][x1-1]!=(3 * wall_h):
                if a[y1+2][x1]!=red_player:
                    a[y1][x1]=" "
                    y1+=2
                    ctr=1
                elif y1<13:
                    if a[y1+3][x1-1]!=(3 * wall_h):
                        a[y1][x1]=" "
                        y1+=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter four move(a, d) : ")
                        if move2move=="a" and x1>2 and a[y1+2][x1-1]!=(" " + wall_v + " "):
                            a[y1][x1]=" "
                            y1+=2
                            x1-=2
                            ctr=1
                        elif move2move=="d" and x1<16 and a[y1+2][x1+1]!=(" " + wall_v + " "):
                            a[y1][x1]=" "
                            y1+=2
                            x1+=2
                            ctr=1
            elif move=="a" and x1>1 and a[y1][x1-1]!=(" " + wall_v + " "):
                if a[y1][x1-2]!=red_player:
                    a[y1][x1]=" "
                    x1-=2
                    ctr=1
                elif x1>2:
                    if a[y1][x1-3]!=(" " + wall_v + " "):
                        a[y1][x1]=" "
                        x1-=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter four move(w, s) : ")
                        if move2move=="w" and y1>0 and a[y1-1][x1-1]!=(3 * wall_h):
                            a[y1][x1]=" "
                            x1-=2
                            y1-=2
                            ctr=1
                        elif move2move=="s" and y1<16 and a[y1+1][x1-1]!=(3 * wall_h):
                            a[y1][x1]=" "
                            y1+=2
                            x1-=2
                            ctr=1
            elif move=="d" and x1<16 and a[y1][x1+1]!=(" " + wall_v + " "):
                if a[y1][x1+2]!=red_player:
                    a[y1][x1]=" "
                    x1+=2
                    ctr=1
                elif x1<14:
                    if a[y1][x1+3]!=(" " + wall_v + " "):
                        a[y1][x1]=" "
                        x1+=4
                        ctr=1
                    else:
                        move2move=safe_input("Enter four move(w, s) : ")
                        if move2move=="w" and y1>0 and a[y1-1][x1-1]!=(3 * wall_h):
                            a[y1][x1]=" "
                            x1+=2
                            y1-=2
                            ctr=1
                        elif move2move=="s" and y1<16 and a[y1+1][x1-1]!=(3 * wall_h):
                            a[y1][x1]=" "
                            y1+=2
                            x1+=2
                            ctr=1
            elif move == "save":
                # Save the game state
                game_state = {
                    "board": a,
                    "red_position": (x2, y2),
                    "white_position": (x1, y1),
                    "red_walls": w2,
                    "white_walls": w1,
                    "current_turn": ply,
                }
                save_game(game_state)  
                console.print("Game saved! You can resume it later.", style="bold green", justify="center")
                continue  
            elif move=="p":
                if w1>0:
                    t = safe_input("You have "+str(w1)+" wall(s)\nEnter your wall type (h/v/b for back): ")
                    if t=="v" :
                        xw, yw = map(int,input("Enter the coordinates (x, y): ").split())
                        if xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-2][xw*2]!=(" " + wall_v + " ") and a[yw*2][xw*2]!=(" " + wall_v + " "):
                            a[yw*2-2][xw*2]=(" " + wall_v + " ")
                            a[yw*2][xw*2]=(" " + wall_v + " ")
                            a[yw*2-1][xw*2-1]=hashtag_h
                            ply=2
                            w1-=1
                            clear_screen()
                            print_board(a, ply)
                            if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                                a[yw*2-2][xw*2]=(" "+normal_v+" ")
                                a[yw*2][xw*2]=(" "+normal_v+" ")
                                a[yw*2-1][xw*2-1]=plus
                                clear_screen()
                                ply=1
                                print_board(a, ply)
                                print("Error:\nboarder is close.")
                                w1+=1
                    elif t=="h" :
                        xw, yw = map(int,input("Enter the coordinates (x, y): ").split())
                        if xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-1][xw*2-2]!=(3 * wall_h) and a[yw*2-1][xw*2]!=(3 * wall_h):
                            a[yw*2-1][xw*2-1]=hashtag_h
                            a[yw*2-1][xw*2-2]=(3 * wall_h)
                            a[yw*2-1][xw*2]=(3 * wall_h)
                            ply=2
                            w1-=1
                            clear_screen()
                            print_board(a, ply)
                            if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                                a[yw*2-1][xw*2]=(3 * normal_h)
                                a[yw*2-1][xw*2-2]=(3 * normal_h)
                                a[yw*2-1][xw*2-1]=plus
                                clear_screen()
                                ply=1
                                print_board(a, ply)
                                print("Error:\nboarder is close.")
                                w1+=1
                    elif t=="b":
                        return
                    else:
                        console.print("Invalied move!!!", style="bold red")
                        continue
                else:
                    print("Error:\nYou don't have a wall anymore!")
            elif move != "n":
                print("Error:\nPlease enter a valid value.")
            if ctr == 1:
                a[y1][x1] = white_player
                clear_screen()
                ply=2
                print_board(a, ply)
            
                #red_username = [user for user, piece in player_piece.items() if piece == "red" ][0]
                #white_username = [user for user, piece in player_piece.items() if piece == "white"][0]
                
            if y1==0:
                red_username = [user for user, piece in player_piece.items() if piece == "red"][0]
                white_username = [user for user, piece in player_piece.items() if piece == "white"][0]
                console.print(f"🎉 Congratulations, {white_username}! You have won the game 🎉", style="bold green", justify="center")
                console.print(f"Better luck next time, {red_username}.", style="bold yellow", justify="center")
                update_player_stats(winner=white_username, loser=red_username)
                #Prompt.ask("[bold cyan]Press Enter to return to the main menu...[/bold cyan]")
                safe_input("Press Enter to return to the main menu...")
                break

            
            '''if y1==0:
                print("White player is winner!")
                break'''

def display_entry_table():
    table = Table(title="[bold cyan]==| Entry Menu |==[/bold cyan]", show_header=True, header_style="bold cyan", padding=(0, 2))
    table.add_column("Option", style="bold cyan", justify="center")
    table.add_column("Description", style="bold cyan", justify="center")
    table.add_row("1", "Sign-Up")
    table.add_row("2", "Login")
    table.add_row("3", "Exit")
    console.print(table)

def display_login_table():
    table = Table(title="[bold magenta]==| Login Menu |==[/bold magenta]")
    table.add_column("Field", style="bold magenta", justify="center")
    table.add_column("Description", style="bold magenta", justify="center")
    table.add_row("Username", "Unique username for the user")
    table.add_row("Email", "Valid email address")
    table.add_row("Password", "Password must be at least 8 characters long")
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
    table.add_row("2", "View Leaderboard")
    table.add_row("3", "saved games")
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
        if load_user1(username):
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
            "email": email,
            "wins" : 0,
            "losses" : 0
        }

        create_player_file(username, user_data)

        console.print("Everything is set to play!", style="bold underline green", justify="center")
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        break

def login_user1():
    global logged_in_user, player_piece

    display_login_table()

    while True:
        username = Prompt.ask("[bold magenta]First user logging in.Enter username (or b to go back)[/bold magenta]", default="", show_default=False)
        if username == 'b':
            clear_screen()
            return

        user = load_user1(username)
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
        logged_in_user.append(username)
        if len(player_piece) == 0:
            player_piece[username] = "red"
        elif len(player_piece) == 1 :
            player_piece[username] = "white" 
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        main_menu(username)
        break

def login_user2():
    global logged_in_user, player_piece
    display_login_table()

    while True:
        username = Prompt.ask("[bold magenta]Second user logging in.Enter username (or b to go back)[/bold magenta]", default="", show_default=False)
        if username == 'b':
            clear_screen()
            return

        user = load_user2(username)
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
        logged_in_user.append(username)
        if len(player_piece) == 0 :
            player_piece[username] = "red"
        elif len(player_piece) == 1 :
            player_piece[username] = "white"
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        main_menu(username)
        break

def main_menu(username):
    
    while True:
        clear_screen()
        display_main_menu_table()

        choice = Prompt.ask("[bold yellow]Enter choice[/bold yellow]", default="", show_default=False)
        if choice == '1' and len(logged_in_user) == 2:
            console.print("Starting new game...", style="bold green")
            clear_screen()
            # login_user1()
            start_game()
        elif choice == "1" and len(logged_in_user) < 2 :
            console.print("[bold red] Second user must log in![/bold red]")
            login_user2()
        elif choice == '2':
            console.print("Viewing leaderboard...", style="bold green")
            view_leaderboard()
        elif choice == '3' :
            console.print("Loading saved game...", style="bold green")
            game_state = load_game()
            if game_state:
                start_game(game_state)
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
            login_user1()
        elif choice == '3':
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]", justify="center")
            Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
if __name__ == "__main__":
    main()

import bcrypt
import re
import json
import os
import msvcrt
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from colorama import Fore, Style

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

def start_game():
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
    move="t"
    x2=9
    y2=0
    a[y2][x2]=red_player
    w2=10
    x1=9
    y1=16
    a[y1][x1]=white_player
    w1=10
    ply=1
    clear_screen()
    print_board(a, ply)
    while move!="n":
        ctr=0
        if ply==2:
            move=input("Enter your move(w, a, s, d or p for place wall) : ")
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
                        move2move=input("Enter your move(a, d) : ")
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
                        move2move=input("Enter your move(a, d) : ")
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
                        move2move=input("Enter your move(w, s) : ")
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
                        move2move=input("Enter your move(w, s) : ")
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
                    t = input("You have "+str(w2)+" wall(s)\nEnter your wall type (h/v/b for back): ")
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
                print("Red player is winner!")
                break
        else:
            move=input("Enter your move(w, a, s, d or p for place wall) : ")
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
                        move2move=input("Enter four move(a, d) : ")
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
                        move2move=input("Enter four move(a, d) : ")
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
                        move2move=input("Enter four move(w, s) : ")
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
                        move2move=input("Enter four move(w, s) : ")
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
            elif move=="p":
                if w1>0:
                    t = input("You have "+str(w1)+" wall(s)\nEnter your wall type (h/v/b for back): ")
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
            if y1==0:
                print("White player is winner!")
                break

def display_entry_table():
    table = Table(title="[bold cyan]==| Entry Menu |==[/bold cyan]", show_header=True, header_style="bold cyan", padding=(0, 2))
    table.add_column("Option", style="bold cyan", justify="center")
    table.add_column("Description", style="bold cyan", justify="center")
    table.add_row("1", "SignIn")
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
    table.add_row("3", "Exit")
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
            "email": email
        }

        create_player_file(username, user_data)

        console.print("Everything is set to play!", style="bold underline green", justify="center")
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        break

def login_user1():
    display_login_table()

    while True:
        username = Prompt.ask("[bold magenta]Enter username (or b to go back)[/bold magenta]", default="", show_default=False)
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
        Prompt.ask("[bold yellow]Press Enter to continue...[/bold yellow]")
        clear_screen()
        main_menu(username)
        break

def login_user2():
    display_login_table()

    while True:
        username = Prompt.ask("[bold magenta]Enter username (or b to go back)[/bold magenta]", default="", show_default=False)
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
            clear_screen()
            # login_user1()
            start_game()
        elif choice == '2':
            console.print("Viewing leaderboard...", style="bold green")
        elif choice == '3':
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

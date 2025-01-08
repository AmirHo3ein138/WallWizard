from colorama import Fore, Style
import os
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

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(a, ply):
    for i in range(17):
        c=""
        for j in range(17):
            c+=a[i][j]
        if i%2==0:
            c+=a[i][17]
        print(c)
    if ply == 2:
        print(f"Red player's turn ({red_player}):")
    else:
        print(f"White player's turn ({white_player})")

def dfsFunction(x,y,a,p):
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
a=[]
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
clear_console()
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
        elif move=="p":
            if w2>0:
                t = input("Enter your wall type (h/v): ")
                xw, yw = map(int,input("Enter the coordinates(x, y): ").split()) 
                if t=="v" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_v and a[yw*2-2][xw*2]!=(" " + wall_v + " ") and a[yw*2][xw*2]!=(" " + wall_v + " "):
                    a[yw*2-2][xw*2]=(" " + wall_v + " ")
                    a[yw*2][xw*2]=(" " + wall_v + " ")
                    a[yw*2-1][xw*2-1]=hashtag_v
                    ply=1
                    w2-=1
                    clear_console()
                    print_board(a, ply)
                    if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                        a[yw*2-2][xw*2]=(" "+normal_v+" ")
                        a[yw*2][xw*2]=(" "+normal_v+" ")
                        a[yw*2-1][xw*2-1]=plus
                        clear_console()
                        ply=2
                        print_board(a, ply)
                        print("Error:\nboarder is close.")
                        
                        w2+=1
                elif t=="h" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-1][xw*2-2]!=(3 * wall_h) and a[yw*2-1][xw*2]!=(3 * wall_h):
                    a[yw*2-1][xw*2-1]=hashtag_h
                    a[yw*2-1][xw*2-2]=(3 * wall_h)
                    a[yw*2-1][xw*2]=(3 * wall_h)
                    ply=1
                    w2-=1
                    clear_console()
                    print_board(a, ply)
                    if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                        a[yw*2-1][xw*2]=(3 * normal_h)
                        a[yw*2-1][xw*2-2]=(3 * normal_h)
                        a[yw*2-1][xw*2-1]=plus
                        clear_console()
                        ply=2
                        print_board(a, ply)
                        print("Error:\nboarder is close.")
                        w2+=1
            else:
                print("Error:\nYou don't have a wall anymore!")
        elif move!="n":
            print("Error:\nplease enter a valid value.")
        if ctr==1:
            a[y2][x2]=red_player
            ply=1
            clear_console()
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
            elif x1<13:
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
                t = input("Enter your wall type (h/v): ")
                xw, yw = map(int,input("Enter the coordinates (x, y): ").split())
                if t=="v" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_v and a[yw*2-2][xw*2]!=(" " + wall_v + " ") and a[yw*2][xw*2]!=(" " + wall_v + " "):
                    a[yw*2-2][xw*2]=(" " + wall_v + " ")
                    a[yw*2][xw*2]=(" " + wall_v + " ")
                    a[yw*2-1][xw*2-1]=hashtag_v
                    ply=2
                    w1-=1
                    clear_console()
                    print_board(a, ply)
                    if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                        a[yw*2-2][xw*2]=(" "+normal_v+" ")
                        a[yw*2][xw*2]=(" "+normal_v+" ")
                        a[yw*2-1][xw*2-1]=plus
                        clear_console()
                        ply=1
                        print_board(a, ply)
                        print("Error:\nboarder is close.")
                        w1+=1
                elif t=="h" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-1][xw*2-2]!=(3 * wall_h) and a[yw*2-1][xw*2]!=(3 * wall_h):
                    a[yw*2-1][xw*2-1]=hashtag_h
                    a[yw*2-1][xw*2-2]=(3 * wall_h)
                    a[yw*2-1][xw*2]=(3 * wall_h)
                    ply=2
                    w1-=1
                    clear_console()
                    print_board(a, ply)
                    if dfsFunction(x1, y1, a, 1) == False or dfsFunction(x2, y2, a, 2) == False:
                        a[yw*2-1][xw*2]=(3 * normal_h)
                        a[yw*2-1][xw*2-2]=(3 * normal_h)
                        a[yw*2-1][xw*2-1]=plus
                        clear_console()
                        ply=1
                        print_board(a, ply)
                        print("Error:\nboarder is close.")
                        w1+=1
            else:
                print("Error:\nYou don't have a wall anymore!")
        elif move != "n":
            print("Error:\nPlease enter a valid value.")
        if ctr == 1:
            a[y1][x1] = white_player
            clear_console()
            ply=2
            print_board(a, ply)
        if y1==0:
            print("White player is winner!")
            break

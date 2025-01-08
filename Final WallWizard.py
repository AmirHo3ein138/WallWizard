from colorama import Fore, Style
# Class for color Shapes
class ColoredTableCharacters:
    def __init__(self):
        self.reset = Style.RESET_ALL

        # تعریف کاراکترهای جدول با رنگ‌ها
        self.horizontal_simple = f"{Fore.BLUE}\u2501{self.reset}"  # جدول ساده افقی (آبی)
        self.vertical_simple = f"{Fore.BLUE}\u2503{self.reset}"    # جدول عمودی ساده (آبی)
        self.plus_simple = f"{Fore.BLUE}\u254b{self.reset}"        # مثبت‌های ساده بین خطوط جدول (آبی)
        self.plus_between_walls_h = f"{Fore.RED}\u254b{self.reset}"
        self.plus_between_walls_v = f"{Fore.RED}\u2542{self.reset}" # مثبت‌های بین دو دیوار هشتگ‌ها (آبی)
        self.vertical_wall = f"{Fore.RED}\u2503{self.reset}"       # دیوار عمودی (قرمز)
        self.horizontal_wall = f"{Fore.RED}\u2501{self.reset}"  # دیوار افقی (زرد)
table_chars = ColoredTableCharacters()

# Map Shapes
normal_h = table_chars.horizontal_simple
normal_v = table_chars.vertical_simple
wall_h = table_chars.horizontal_wall
wall_v = table_chars.vertical_wall
hashtag_v = table_chars.plus_between_walls_v
hashtag_h = table_chars.plus_between_walls_h
plus = table_chars.plus_simple

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
x=9
y=0
a[y][x]="\u2659"
w2=10
g=9
f=16
a[f][g]="\u265f"
w1=10
ply=1
while move!="n":
    for i in range(17):
        c=""
        for j in range(17):
            c+=a[i][j]
        if i%2==0:
            c+=a[i][17]
        print(c)
    ctr=0
    if ply==2:
        move=input("Enter your move(w, a, s, d or p for place wall) : ")
        if move=="w" and y>0 and a[y-1][x-1]!=(3 * wall_h):
            if a[y-2][x]!="o":
                a[y][x]=" "
                y-=2
                ctr=1
            elif y>2:
                if a[y-3][x-1]!=(3 * wall_h):
                    a[y][x]=" "
                    y-=4
                    ctr=1
                else:
                    move2move=input("Enter your move(a, d) : ")
                    if move2move=="a" and x>2 and a[y-2][x-1]!=(" " + wall_v + " "):
                        a[y][x]=" "
                        y-=2
                        x-=2
                        ctr=1
                    elif move2move=="d" and x<16 and a[y-2][x+1]!=(" " + wall_v + " "):
                        a[y][x]=" "
                        y-=2
                        x+=2
        elif move=="s" and y<16 and a[y+1][x-1]!=(3 * wall_h):
            if a[y+2][x]!="o":
                a[y][x]=" "
                y+=2
                ctr=1
            elif y<13:
                if a[y+3][x-1]!=(3 * wall_h):
                    a[y][x]=" "
                    y+=4
                    ctr=1
                else:
                    move2move=input("Enter your move(a, d) : ")
                    if move2move=="a" and x>2 and a[y+2][x-1]!=(" " + wall_v + " "):
                        a[y][x]=" "
                        y+=2
                        x-=2
                        ctr=1
                    elif move2move=="d" and x<16 and a[y+2][x+1]!=(" " + wall_v + " "):
                        a[y][x]=" "
                        y+=2
                        x+=2
        elif move=="a" and x>1 and a[y][x-1]!=(" " + wall_v + " "):
            if a[y][x-2]!="o":
                a[y][x]=" "
                x-=2
                ctr=1
            elif x>2:
                if a[y][x-3]!=(" " + wall_v + " "):
                    a[y][x]=" "
                    x-=4
                    ctr=1
                else:
                    move2move=input("Enter your move(w, s) : ")
                    if move2move=="w" and y>0 and a[y-1][x-1]!=(3 * wall_h):
                        a[y][x]=" "
                        x-=2
                        y-=2
                        ctr=1
                    elif move2move=="s" and y<16 and a[y+1][x-1]!=(3 * wall_h):
                        a[y][x]=" "
                        y+=2
                        x-=2
                        ctr=1
        elif move=="d" and x<16 and a[y][x+1]!=(" " + wall_v + " "):
            if a[y][x+2]!="o":
                a[y][x]=" "
                x+=2
                ctr=1
            elif x<13:
                if a[y][x+3]!=(" " + wall_v + " "):
                    a[y][x]=" "
                    x+=4
                    ctr=1
                else:
                    move2move=input("Enter your move(w, s) : ")
                    if move2move=="w" and y>0 and a[y-1][x-1]!=(3 * wall_h):
                        a[y][x]=" "
                        x+=2
                        y-=2
                        ctr=1
                    elif move2move=="s" and y<16 and a[y+1][x-1]!=(3 * wall_h):
                        a[y][x]=" "
                        y+=2
                        x+=2
                        ctr=1
        elif move=="p":
            if w2>0:
                t = input("Enter your wall type (h/v): ")
                xw, yw = map(int,input("Enter the coordinates (x, y): ").split()) 
                if t=="v" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_v and a[yw*2-2][xw*2]!=(" " + wall_v + " ") and a[yw*2][xw*2]!=(" " + wall_v + " "):
                    a[yw*2-2][xw*2]=(" " + wall_v + " ")
                    a[yw*2][xw*2]=(" " + wall_v + " ")
                    a[yw*2-1][xw*2-1]=hashtag_v
                    ply=1
                    w2-=1
                    if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                        a[yw*2-2][xw*2]=(" "+normal_v+" ")
                        a[yw*2][xw*2]=(" "+normal_v+" ")
                        a[yw*2-1][xw*2-1]=plus
                        print("Error:\nboarder is close.")
                        ply=2
                        w2+=1
                else:
                    print("Error:\nYou don't have a wall anymore!")
            elif t=="h" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-1][xw*2-2]!=(3 * wall_h) and a[yw*2-1][xw*2]!=(3 * wall_h):
                a[yw*2-1][xw*2-1]=hashtag_h
                a[yw*2-1][xw*2-2]=(3 * wall_h)
                a[yw*2-1][xw*2]=(3 * wall_h)
                ply=1
                w2-=1
                if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                    a[yw*2-1][xw*2]=(3 * normal_h)
                    a[yw*2-1][xw*2-2]=(3 * normal_h)
                    a[yw*2-1][xw*2-1]=plus
                    print("Error:\nboarder is close.")
                    ply=2
                    w2+=1
        elif move!="n":
            print("Error:\nplease enter a valid value.")
        if ctr==1:
            a[y][x]="x"
            ply=1
        if y==16:
            print("Player 2 is winner!")
            break
    else:
        move=input("Enter your move(w, a, s, d or p for place wall) : ")
        if move=="w" and f>0 and a[f-1][g-1]!=(3 * wall_h):
            if a[f-2][g]!="o":
                a[f][g]=" "
                f-=2
                ctr=1
            elif f>2:
                if a[f-3][g-1]!=(3 * wall_h):
                    a[f][g]=" "
                    f-=4
                    ctr=1
                else:
                    move2move=input("Enter four move(a, d) : ")
                    if move2move=="a" and g>2 and a[f-2][g-1]!=(" " + wall_v + " "):
                        a[f][g]=" "
                        f-=2
                        g-=2
                        ctr=1
                    elif move2move=="d" and g<16 and a[f-2][g+1]!=(" " + wall_v + " "):
                        a[f][g]=" "
                        f-=2
                        g+=2
        elif move=="s" and f<16 and a[f+1][g-1]!=(3 * wall_h):
            if a[f+2][g]!="o":
                a[f][g]=" "
                f+=2
                ctr=1
            elif f<13:
                if a[f+3][g-1]!=(3 * wall_h):
                    a[f][g]=" "
                    f+=4
                    ctr=1
                else:
                    move2move=input("Enter four move(a, d) : ")
                    if move2move=="a" and g>2 and a[f+2][g-1]!=(" " + wall_v + " "):
                        a[f][g]=" "
                        f+=2
                        g-=2
                        ctr=1
                    elif move2move=="d" and g<16 and a[f+2][g+1]!=(" " + wall_v + " "):
                        a[f][g]=" "
                        f+=2
                        g+=2
        elif move=="a" and g>1 and a[f][g-1]!=(" " + wall_v + " "):
            if a[f][g-2]!="o":
                a[f][g]=" "
                g-=2
                ctr=1
            elif g>2:
                if a[f][g-3]!=(" " + wall_v + " "):
                    a[f][g]=" "
                    g-=4
                    ctr=1
                else:
                    move2move=input("Enter four move(w, s) : ")
                    if move2move=="w" and f>0 and a[f-1][g-1]!=(3 * wall_h):
                        a[f][g]=" "
                        g-=2
                        f-=2
                        ctr=1
                    elif move2move=="s" and f<16 and a[f+1][g-1]!=(3 * wall_h):
                        a[f][g]=" "
                        f+=2
                        g-=2
                        ctr=1
        elif move=="d" and g<16 and a[f][g+1]!=(" " + wall_v + " "):
            if a[f][g+2]!="o":
                a[f][g]=" "
                g+=2
                ctr=1
            elif g<13:
                if a[f][g+3]!=(" " + wall_v + " "):
                    a[f][g]=" "
                    g+=4
                    ctr=1
                else:
                    move2move=input("Enter four move(w, s) : ")
                    if move2move=="w" and f>0 and a[f-1][g-1]!=(3 * wall_h):
                        a[f][g]=" "
                        g+=2
                        f-=2
                        ctr=1
                    elif move2move=="s" and f<16 and a[f+1][g-1]!=(3 * wall_h):
                        a[f][g]=" "
                        f+=2
                        g+=2
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
                    if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                        a[yw*2-2][xw*2]=(" "+normal_v+" ")
                        a[yw*2][xw*2]=(" "+normal_v+" ")
                        a[yw*2-1][xw*2-1]=plus
                        print("Error:\nboarder is close.")
                        ply=1
                        w1+=1
                elif t=="h" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!=hashtag_h and a[yw*2-1][xw*2-2]!=(3 * wall_h) and a[yw*2-1][xw*2]!=(3 * wall_h):
                    a[yw*2-1][xw*2-1]=hashtag_h
                    a[yw*2-1][xw*2-2]=(3 * wall_h)
                    a[yw*2-1][xw*2]=(3 * wall_h)
                    ply=2
                    w1-=1
                    if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                        a[yw*2-1][xw*2]=(3 * normal_h)
                        a[yw*2-1][xw*2-2]=(3 * normal_h)
                        a[yw*2-1][xw*2-1]=plus
                        print("Error:\nboarder is close.")
                        ply=1
                        w1+=1
            else:
                print("Error:\nYou don't have a wall anymore!")
        elif move != "n":
            print("Error:\nPlease enter a valid value.")
        if ctr == 1:
            a[f][g] = "o"
            ply=2
        if f==0:
            print("Player 1 is winner!")
            break

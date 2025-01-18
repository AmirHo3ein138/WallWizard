def dfsFunction(x,y,a,p):
    ky=0
    dfs=[[y,x]]
    while True:
        k=0
        if y!=0:
            if a[y-1][x-1]=="---" and y>=2 and dfs.count([y-2,x])==0 and dfs.count([y-2,x,"t"])==0:
                dfs.append([y-2,x])
        if y!=16:
            if a[y+1][x-1]=="---" and y<=15 and dfs.count([y+2,x])==0 and dfs.count([y+2,x,"t"])==0:
                dfs.append([y+2,x])
        if x!=17:
            if a[y][x+1]==" | " and x<=15 and dfs.count([y,x+2])==0 and dfs.count([y,x+2,"t"])==0:
                dfs.append([y,x+2])
        if a[y][x-1]==" | " and x>=2 and dfs.count([y,x-2])==0 and dfs.count([y,x-2,"t"])==0:
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

v_wall = 0
h_wall = 0
v_path = '\u2506'
h_path = '\u2508'
hashtag = '\u2541'
plus = '\u2543'
a=[]
for i in range(17):
    a.append([])
    if i%2==0:
        a[i].append(" ")
        for j in range(9):
            a[i].append(" ")
            if j<8:
                a[i].append(" "+v_path+" ")
    else:
        for j in range(9):
            a[i].append(3 * h_path)
            if j<8:
                a[i].append("" + plus + "")
move="t"
x=9
y=0
a[y][x]="x"
w2=10
g=9
f=16
a[f][g]="o"
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
    move=input("Do your move(w, a, s, d or p for place wall) : ")
    if ply==2:
        if move=="w" and y>0 and a[y-1][x-1]!="===":
            a[y][x]=" "
            y-=2
            ctr=1
        elif move=="s" and y<16 and a[y+1][x-1]!="===":
            a[y][x]=" "
            y+=2
            ctr=1
        elif move=="a" and x>1 and a[y][x-1]!="|||":
            a[y][x]=" "
            x-=2
            ctr=1
        elif move=="d" and x<16 and a[y][x+1]!="|||":
            a[y][x]=" "
            x+=2
            ctr=1
        elif move=="p":
            t = input("Enter your wall type (h/v): ")
            xw = int(input("Enter your mo: "))
            yw = int(input("Enter your ma: "))
            if t=="h" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!="#" and a[yw*2-2][xw*2]!="|||" and a[yw*2][xw*2]!="|||":
                a[yw*2-2][xw*2]="|||"
                a[yw*2][xw*2]="|||"
                a[yw*2-1][xw*2-1]="#"
                ply=1
                w2-=1
                if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                    a[yw*2-2][xw*2]=" |  "
                    a[yw*2][xw*2]=" | "
                    a[yw*2-1][xw*2-1]="+"
                    print("Error:\nboarder is close.")
                    ply=2
                    w2+=1
            elif t=="v" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!="#" and a[yw*2-1][xw*2-2]!="===" and a[yw*2-1][xw*2]!="===":
                a[yw*2-1][xw*2-1]="#"
                a[yw*2-1][xw*2-2]="==="
                a[yw*2-1][xw*2]!="==="
                ply=1
                w2-=1
                if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                    a[yw*2-2][xw*2]=" |  "
                    a[yw*2][xw*2]=" | "
                    a[yw*2-1][xw*2-1]="+"
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
        if move=="w" and f>0 and a[f-1][g-1]!="===":
            a[f][g] = " "
            f -= 2
            ctr = 1
        elif move=="s" and f<16 and a[f+1][g-1]!="===":
            a[f][g] = " "
            f += 2
            ctr = 1
        elif move=="a" and g>1 and a[f][g-1]!="|||":
            a[f][g] = " "
            g -= 2
            ctr = 1
        elif move=="d" and g<16 and a[f][g+1]!="|||":
            a[f][g] = " "
            g += 2
            ctr = 1
        elif move=="p":
            t = input("Enter your wall type (h/v): ")
            xw = int(input("Enter your mo: "))
            yw = int(input("Enter your ma: "))
            if t=="h" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!="#" and a[yw*2-2][xw*2]!="|||" and a[yw*2][xw*2]!="|||":
                a[yw*2-2][xw*2]="|||"
                a[yw*2][xw*2]="|||"
                a[yw*2-1][xw*2-1]="#"
                ply=2
                w1-=1
                if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                    a[yw*2-2][xw*2]=" |  "
                    a[yw*2][xw*2]=" | "
                    a[yw*2-1][xw*2-1]="+"
                    print("Error:\nboarder is close.")
                    ply=1
                    w1+=1
            elif t=="v" and xw<9 and yw<9 and xw>0 and yw>0 and a[yw*2-1][xw*2-1]!="#" and a[yw*2-1][xw*2-2]!="===" and a[yw*2-1][xw*2]!="===":
                a[yw*2-1][xw*2-1]="#"
                a[yw*2-1][xw*2-2]="==="
                a[yw*2-1][xw*2]!="==="
                ply=2
                w1-=1
                if dfsFunction(g, f, a, 1) == False or dfsFunction(x, y, a, 2) == False:
                    a[yw*2-2][xw*2]=" |  "
                    a[yw*2][xw*2]=" | "
                    a[yw*2-1][xw*2-1]="+"
                    print("Error:\nboarder is close.")
                    ply=1
                    w1+=1
        elif move != "n":
            print("Error:\nPlease enter a valid value.")
        if ctr == 1:
            a[f][g] = "o"
            ply=2
        if f==0:
            print("Player 1 is winner!")
            break

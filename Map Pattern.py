def draw_quoridor_board():
    horizontal_wall = '\u2501'  
    vertical_wall = '\u2503'   
    empty_space = '   '   
    wall = "\u2551"     
    intersection = '\u254b'   

    board = []

    for row in range(17):
        if row % 2 == 0:
            line = []
            for col in range(17):
                if col % 2 == 0:
                    line.append('   ')
                else:
                    line.append(vertical_wall)
            board.append(''.join(line))
        else:
            line = []
            for col in range(17):
                if col % 2 == 0:
                    line.append(horizontal_wall * 3)
                else:
                    line.append(intersection) 
            board.append(''.join(line))

    for line in board:
        print(line)

draw_quoridor_board()
horizental = "\u2551"
vertical = "\u2550"
print(vertical)
print(horizental)

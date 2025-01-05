def draw_quoridor_board():
    horizontal_wall = '\u2508' 
    vertical_wall = '\u2506'    
    empty_space = '   '         
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

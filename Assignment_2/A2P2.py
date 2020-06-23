def print_board(board, delim=' '):
    print()
    for row in board:
        for element in row:
            print(element, end=delim)
        print()
    print()
    
def is_legal(board, row, col):
    return True if board[row][col] == [] else False

def diagonals(row, col, n):
    diagonals_positions = []

    # lower-left diagonals
    i, j = row, col
    while i<n and j<n:
        diagonals_positions.append((i,j))
        i+=1
        j+=1

    # upper-right diagonals
    i, j = row, col
    while i>=0 and j>=0:
        diagonals_positions.append((i,j))
        i-=1
        j-=1
    
    # upper-left diagonals
    i, j = row, col
    while i>=0 and j<n:
        diagonals_positions.append((i,j))
        i-=1
        j+=1
    
    # lower-right diagonals
    i, j = row, col
    while i<n and j>=0:
        diagonals_positions.append((i,j))
        i+=1
        j-=1

    # removing duplicates : set()
    return list(set(diagonals_positions))
    

def place_queen(board, row, col, n):
    # marking row
    for i in range(n):
        board[row][i].append("Q"+str(row+1)+"A")

    # marking col
    for i in range(n):
        board[i][col].append("Q"+str(row+1)+"A")

    # marking diagonal
    diagonal = diagonals(row, col, n)
    for diag in diagonal:
        board[diag[0]][diag[1]].append("Q"+str(row+1)+"A")
    
    board[row][col] = ["Q"+str(row+1)]

def remove_queen(board, row, col, n):
    board[row][col] = ["Q"+str(row+1)+"A"]
    # removing row
    for i in range(n):
        try:
            board[row][i].remove("Q"+str(row+1)+"A")
        except Exception as e:
            if e == "list.remove(x): x not in list":
                continue

    # removing col
    for i in range(n):
        try:
            board[i][col].remove("Q"+str(row+1)+"A")
        except Exception as e:
            if e == "list.remove(x): x not in list":
                continue

    # rempving diagonal
    diagonal = diagonals(row, col, n)
    for diag in diagonal:
        try:
            board[diag[0]][diag[1]].remove("Q"+str(row+1)+"A")
        except Exception as e:
            if e == "list.remove(x): x not in list":
                continue
    
    board[row][col] = []
    

def solve_N_queens_helper(board, current_row, n):

    if current_row >= n:
        return True
    
    for col in range(n):
        if is_legal(board, current_row, col):
            # Choice
            place_queen(board, current_row, col, n)
            if solve_N_queens_helper(board, current_row+1, n) == True:
                return True
            # Undo Choice
            remove_queen(board, current_row, col, n)

    return False
            

def solve_N_queens(n):
    board = [[[] for i in range(n)] for i in range(n)]
    solve_N_queens_helper(board, 0, n)
    
    clean_board = []
    count=0
    for row in board:
        temp = []
        for element in row:
            if len(element) == 1:
                temp.append(element[0])
            else:
                temp.append("0")
                count+=1
        clean_board.append(temp)
    if count==n*n:
        print("No solution exists!")
    else:
        print_board(clean_board, delim='\t')

if __name__ == "__main__":
    n = int(input("Size of grid: "))
    solve_N_queens(n)

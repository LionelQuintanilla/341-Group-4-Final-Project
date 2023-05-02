# -*- coding: utf-8 -*-
"""Object-Oriented Connect4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17hCx-WuQ_yJ50EcEa3l-cacyVLvhbi_8

### **CECS 451 Final Project - Connect-4 with Minimax Algorithm**

*Sierra Harris, Justin Le, Lionel Quintanilla, Amanuel Reda, Salvador Villanueva*

**1 - Print Board**

Prints current state of the board with aesthetic formatting. The board is a 6x7 matrix* arranged by rows and columns (rows first).

*Ignore the issue of **i** and **j** in this function; this function was adapted from another source and the way **i** and **j** are implemented is different from the rest of the game logic.*
"""

# print board
def printBoard(board):
    rows = ['0','1','2','3','4','5']
    top = '    0   1   2   3   4   5   6   '
    row = [[n] for n in range(0,7)]
    row[0][0] = '0 | '
    row[1][0] = '1 | '
    row[2][0] = '2 | '
    row[3][0] = '3 | '
    row[4][0] = '4 | '
    row[5][0] = '5 | '
    print('')
    print('  ' + '-'*(len(top)-3))
    for i in range(0,len(rows)):
        for j in range(1,8):
            row[i][0] = row[i][0] + str(board[i][j-1]) + ' | '
        print(row[i][0])
        print('  ' + '-'*((len(row[i][0])-3)))
    print(top)
    print('')

"""**2 - Stack Class**

This class implements a FILO stack. Each column in the Connect-4 board is represented by a stack in order to simulate the way pieces are dropped in the real game. It also simplifies the game logic by:


1.   Not worrying having to determine where the positions of valid moves are. If a stack is not full, it is assumed that there is a valid move there (similar to real Connect-4). 
2.   Since we only care about the piece on top of the column when determining valid moves, we can use the **peep()** and **pop()** functions of the stack to simply piece placement.
"""

# Class stack (for each column)
class Stack:

    # Intializes the stack as an empty list
    def __init__(self):
        self._list = []
    
    # Returns the length of the list as the length of the stack
    def __len__(self):
        return len(self._list)    
    
    # Pushes an element onto the top of the stack as long as there are fewer 
    # than 6 pieces (the maximum number in a column)
    def push(self, element):
        if len(self._list) < 6:
            self._list.append(element)
        else:
            return
    
    # Removes the top element from the stack
    def pop(self):
        self._list.pop()
    
    # Returns the value of the element on top of the stack
    def peek(self):
        return self._list[-1]

    # Prints the current contents of the stack, from bottom to top (the order they were placed in)
    # FOR DIAGNOSTIC PURPOSES ONLY
    def printStack(self):
      for i in range(len(self)):
        print(self._list[i], end = ' ')
      print()

"""**3 - Initialize Board**

Creates an empty 6x7 matrix. An empty space is presented by ' '. The board is used for aesthetic purposes only and is not used to run game logic.
"""

# Initialize an empty board
def initBoard():
    # empty board
    rows = ['a','b','c','d','e','f']
    board = []
    for i in range(0,len(rows)):
        board.append([' '] * 7)
    
    return board

"""**4 - Initialize Stacks**

Creates an array of 7 stacks, where each stack represents a column on the board. The game logic is run here. While the Stacks array is never directly displayed, moves are mapped from the Stacks object to the board object for visualization. In this case, the **i** coordinate would be the height of the stack before the move is placed, and the column number is the **j** coordinate.
"""

# Initializes an array of empty stacks
def initStacks():
    S = [ Stack(), Stack(), Stack(), 
         Stack(), Stack(), Stack(), Stack() ]
    return S

"""**5 - Check Win**

Checks to see if there is a winning condition* on the board. If a winning score is detected, a score of 10 is returned for the maximizing player and a score of -10 is returned for the minimizing player.

*The win cases for a diagonal win had to be hard-coded. This was due to the complexity of dynamically computing all the possible diagonal routes without casuing a index boudary error. *italicized text*
"""

# Check wins
def checkWin(player, computer, board):
    # Initializes the score at 0
    game = 0   
    # Horizontal checker for the left half of the board
    for i in range(0,6):
        for j in range(0,4):
            # Checks if four pieces in a row horizontally contain the same piece
            if (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]) and board[i][j] != ' ':
                    # If four pieces in a row horizontally contain the same piece
                    # and the piece is the human player's piece, a score of 10 is
                    # returned. If the piece is the computer's piece, a score of
                    # -10 is returned.
                    if board[i][j] == player.getPiece():
                      return 10
                    elif board[i][j] == computer.getPiece():
                      return -10

    # Horizontal checker for the right half second half of the board
    for i in range(0,6):
        for j in range(3,7):
            if (board[i][j] == board[i][j-1] == board[i][j-2] == board[i][j-3]) and board[i][j] != ' ':
                    if board[i][j] == player.getPiece():
                      return 10
                    elif board[i][j] == computer.getPiece():
                      return -10

    # Vertical checker for the top half of the board
    for i in range(0,3):
        for j in range(0,7):
            if (board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j]) and board[i][j] != ' ':
                    if board[i][j] == player.getPiece():
                      return 10
                    elif board[i][j] == computer.getPiece():
                      return -10

    # Vertical checker for the botton half of the board
    for i in range(3,6):
        for j in range(0,7):
            if (board[i][j] == board[i-1][j] == board[i-2][j] == board[i-3][j]) and board[i][j] != ' ':
                    if board[i][j] == player.getPiece():
                      return 10
                    elif board[i][j] == computer.getPiece():
                      return -10

    # Diagonal checker

    # Diagonals that run from the bottom-left to the top-right
    if (board[3][0] == board[2][1] == board[1][2] == board[0][3]) and board[3][0] != ' ':
        if board[3][0] == player.getPiece(): 
            return 10
        elif board[3][0] == computer.getPiece():
            return -10

    if (board[4][0] == board[3][1] == board[2][2] == board[1][3]) and board[4][0] != ' ':
        if board[4][0] == player.getPiece(): 
            return 10
        elif board[4][0] == computer.getPiece():
            return -10

    if (board[3][1] == board[2][2] == board[1][3] == board[0][4]) and board[3][1] != ' ':
        if board[3][1] == player.getPiece(): 
            return 10
        elif board[3][1] == computer.getPiece():
            return -10

    if (board[5][0] == board[4][1] == board[3][2] == board[2][3]) and board[5][0] != ' ':
        if board[5][0] == player.getPiece(): 
            return 10
        elif board[5][0] == computer.getPiece():
            return -10

    if (board[4][1] == board[3][2] == board[2][3] == board[1][4]) and board[4][1] != ' ':
        if board[4][1] == player.getPiece(): 
            return 10
        elif board[4][1] == computer.getPiece():
            return -10

    if (board[3][2] == board[2][3] == board[1][4] == board[0][5]) and board[3][2] != ' ':
        if board[3][2] == player.getPiece(): 
            return 10
        elif board[3][2] == computer.getPiece():
            return -10

    if (board[5][1] == board[4][2] == board[3][3] == board[2][4]) and board[5][1] != ' ':
        if board[5][1] == player.getPiece(): 
            return 10
        elif board[5][1] == computer.getPiece():
            return -10

    if (board[4][2] == board[3][3] == board[2][4] == board[1][5]) and board[4][2] != ' ':
        if board[4][2] == player.getPiece(): 
            return 10
        elif board[4][2] == computer.getPiece():
            return -10

    if (board[3][3] == board[2][4] == board[1][5] == board[0][6]) and board[3][3] != ' ':
        if board[3][3] == player.getPiece(): 
            return 10
        elif board[3][3] == computer.getPiece():
            return -10

    if (board[5][2] == board[4][3] == board[3][4] == board[2][5]) and board[5][2] != ' ':
        if board[5][2] == player.getPiece(): 
            return 10
        elif board[5][2] == computer.getPiece():
            return -10

    if (board[4][3] == board[3][4] == board[2][5] == board[1][6]) and board[4][3] != ' ':
        if board[4][3] == player.getPiece(): 
            return 10
        elif board[4][3] == computer.getPiece():
            return -10

    if (board[5][3] == board[4][4] == board[3][5] == board[2][6]) and board[5][3] != ' ':
        if board[5][3] == player.getPiece(): 
            return 10
        elif board[5][3] == computer.getPiece():
            return -10

    # Diagonals that run from the bottom-right to the top-left
    if (board[2][0] == board[3][1] == board[4][2] == board[5][3]) and board[2][0] != ' ':
        if board[2][0] == player.getPiece(): 
            return 10
        elif board[2][0] == computer.getPiece():
            return -10

    if (board[1][0] == board[2][1] == board[3][2] == board[4][3]) and board[1][0] != ' ':
        if board[1][0] == player.getPiece(): 
            return 10
        elif board[1][0] == computer.getPiece():
            return -10

    if (board[2][1] == board[3][2] == board[4][3] == board[5][4]) and board[2][1] != ' ':
        if board[2][1] == player.getPiece(): 
            return 10
        elif board[2][1] == computer.getPiece():
            return -10

    if (board[0][0] == board[1][1] == board[2][2] == board[3][3]) and board[0][0] != ' ':
        if board[0][0] == player.getPiece(): 
            return 10
        elif board[0][0] == computer.getPiece():
            return -10

    if (board[1][1] == board[2][2] == board[3][3] == board[4][4]) and board[1][1] != ' ':
        if board[1][1] == player.getPiece(): 
            return 10
        elif board[1][1] == computer.getPiece():
            return -10

    if (board[2][2] == board[3][3] == board[4][4] == board[5][5]) and board[2][2] != ' ':
        if board[2][2] == player.getPiece(): 
            return 10
        elif board[2][2] == computer.getPiece():
            return -10

    if (board[0][1] == board[1][2] == board[2][3] == board[3][4]) and board[0][1] != ' ':
        if board[0][1] == player.getPiece(): 
            return 10
        elif board[0][1] == computer.getPiece():
            return -10

    if (board[1][2] == board[2][3] == board[3][4] == board[4][5]) and board[1][2] != ' ':
        if board[1][2] == player.getPiece(): 
            return 10
        elif board[1][2] == computer.getPiece():
            return -10

    if (board[2][3] == board[3][4] == board[4][5] == board[5][6]) and board[2][3] != ' ':
        if board[2][3] == player.getPiece(): 
            return 10
        elif board[2][3] == computer.getPiece():
            return -10
    
    if (board[0][2] == board[1][3] == board[2][4] == board[3][5]) and board[0][2] != ' ':
        if board[2][3] == player.getPiece(): 
            return 10
        elif board[2][3] == computer.getPiece():
            return -10

    if (board[1][3] == board[2][4] == board[3][5] == board[4][6]) and board[1][3] != ' ':
        if board[2][3] == player.getPiece(): 
            return 10
        elif board[2][3] == computer.getPiece():
            return -10

    if (board[0][3] == board[1][4] == board[2][5] == board[3][6]) and board[0][3] != ' ':
        if board[2][3] == player.getPiece(): 
            return 10
        elif board[2][3] == computer.getPiece():
            return -10

    # Returns the current score
    return game

"""**6 - Moves Left**

Checks to see if ther eare moves left on the board. The board is completely full when all of the stacks in the Stacks array have length of 6 (the maximum height of the Connect-4 board).
"""

# Checks if there are moves left
def movesLeft(stacks):

  # A boolean array with 7 entries. Each entry represents whether or not the
  # stack at that index is full. The default value is FALSE (not full).
  stackFull = [False, False, False, False, False, False, False]

  # Checks the length of each stack. If a stack has six pieces, it is marked 
  # as full.
  for i in range(len(stacks)):
    if len(stacks[i]) == 6:
      stackFull[i] == True
  
  # Checks the results of the full check. If at least one stack is not full, 
  # then a value of TRUE is returned. If all the stacks are full, then a value
  # of FALSE is returned.
  for i in range(0, 7, 1):
    if stackFull[i] == False:
        return True

  return False

"""**7 - Move Finder**

Checks the pieces around a potential move to see if they could be used to create potential scoring routes. Moves are weighted* based on the number of pieces they can reach: each piece found in a particular direction increases the weight of the move by 1, and additional points are added if multiple pieces can be reached consectutively.

**Example**: If a piece can touch 1 piece below it and touches 2 pieces in a row to its right, it would have a score of 3.

*The move finder is implemented differently for the maximizing and minimizing players. For the maximizing player, moves are scored based on how many pieces they can touch to possible create a winning score. For the minimizing player, moves are score based on how many pieces they can block that could be used by the maximizing player to create a winning score. *italicized text*
"""

def MoveFinder(currPlayer, oppPlayer, board, Stacks):

  # Initializes the value of the best maximizing move
  bestPotential = -1000
  # Initializes the position of the best maximizing move
  bestPotentialMove = -1

  # Initializes the value of the best minimizing move
  worstPotential = 1000
  # Initializes the position of the best minimizing move
  worstPotentialMove = -1

  # Gets the piece the human player is using
  currPiece = currPlayer.getPiece()
  # Gets the piece the computer is using
  oppPiece = oppPlayer.getPiece()

  # For the maximizing player, checks to see which move has the greatest potential to create a win

  # Iterates through each stack to search for possible moves
  for j in range(7):

    # Initializes the value of the move currently being considered. 
    movePotential = 0

    # Checks to see if the current stack is full
    if len(Stacks[j]) < 6:

      # If the stack is not full, the row position of the current move is 
      # obtained by using the height of the stack as the offset from the 
      # bottom of the board
      i = 5 - len(Stacks[j])
      
      if (j > 0):

        # Checks the pieces to the left of the current move for pieces in a row
        for h in range(j, -1, -1):
          #print('R-L: Dynamic horizontal checker test: (', i, ', ', h, ') = ', board[i][h], ', (', i, ', ', h-1, ') = ', board[i][h-1])
          if (h == j and board[i][h] == ' ' and board[i][h-1] == currPiece) or (board[i][h] == currPiece and board[i][h-1] == currPiece):
            # Increases the score by 1 for each piece in a row
            movePotential += 1
          else:
            # Stops checking if there are no pieces to the left of the current
            # move or the run of pieces ends
            break
        
        # Checks if there is a diagonal piece to the bottom-left of the 
        # current move
        if (i < 5):
          if (board[i+1][j-1] == currPiece):
            movePotential += 1

      if (j < 6):

        # Checks the pieces to the right of the current move for pieces in a row
        for h in range (j, 6, 1):
          #print('L-R: Dynamic horizontal checker test: (', i, ', ', h, ') = ', board[i][h], ', (', i, ', ', h+1, ') = ', board[i][h+1])
          if (h == j and board[i][h] == ' ' and board[i][h+1] == currPiece) or (board[i][h] == currPiece and board[i][h+1] == currPiece):
            movePotential += 1
          else:
            break
        
        # Checks if there is a diagonal piece to the bottom-right of the 
        # current move
        if (i < 5):
          if (board[i+1][j+1] == currPiece):
            movePotential += 1
      
      # Checks the pieces to the below the current move for pieces in a row vertically
      if (i < 5):
        #print('U-D: Dynamic vertical checker test: (', h, ', ', j, ') = ', board[h][j], ', (', h+1, ', ', j, ') = ', board[h+1][j])
        for h in range(i, 5, 1):
          if (h == i and board[h][j] == ' ' and board[h+1][j] == currPiece) or (board[h][j] == currPiece and board[h+1][j] == currPiece):
              movePotential += 1
          else:
            break
    
      print("Value of move (", i, ", ", j, ") = ", movePotential)

      # If the score of the current move is better than the score of the best
      # move, the score and position of the best move are updated with the 
      # score and position of the current move.
      if movePotential > bestPotential:
        bestPotential = movePotential
        bestPotentialMove = j
  
  # For the minimizing opponent, checks to see which move has the greatest 
  # potential to block an opponent's win
  for j in range(7):

    # The logic for finding the best minimizing move is the same for finding the
    # best maximizing move. The only difference is that the moves are scored 
    # based on how many of the opponent's pieces in a row they block, and the 
    # score is decreased for each piece found.
    movePotential = 0

    if len(Stacks[j]) < 6:
      i = 5 - len(Stacks[j])
      
      if (j > 0):
        for h in range(j, -1, -1):
          #print('R-L: Dynamic horizontal checker test: (', i, ', ', h, ') = ', board[i][h], ', (', i, ', ', h-1, ') = ', board[i][h-1])
          if (h == j and board[i][h] == ' ' and board[i][h-1] == oppPiece) or (board[i][h] == oppPiece and board[i][h-1] == oppPiece):
            movePotential -= 1
          else:
            break
        """
        if (i < 5):
          if (board[i+1][j-1] == oppPiece):
            movePotential -= 1
        """

      if (j < 6):
        for h in range (j, 6, 1):
          #print('L-R: Dynamic horizontal checker test: (', i, ', ', h, ') = ', board[i][h], ', (', i, ', ', h+1, ') = ', board[i][h+1])
          if (h == j and board[i][h] == ' ' and board[i][h+1] == oppPiece) or (board[i][h] == oppPiece and board[i][h+1] == oppPiece):
            movePotential -= 1
          else:
            break
        
        """
        if (i < 5):
          if (board[i+1][j+1] == oppPiece):
            movePotential -= 1
        """
      
      if (i < 5):
        #print('U-D: Dynamic vertical checker test: (', h, ', ', j, ') = ', board[h][j], ', (', h+1, ', ', j, ') = ', board[h+1][j])
        for h in range(i, 5, 1):
          if (h == i and board[h][j] == ' ' and board[h+1][j] == oppPiece) or (board[h][j] == oppPiece and board[h+1][j] == oppPiece):
              movePotential -= 1
          else:
            break
    
      print("Value of move (", i, ", ", j, ") = ", movePotential)

      if movePotential < worstPotential:
        worstPotential = movePotential
        worstPotentialMove = j

  # If the score of the best maximizing move is 0, a random move is chosen. This
  # should only occur if the game is just starting
  if bestPotential == 0:

    #print("Possible Move Value Error?")

    bestPotentialMove = -1

    while (bestPotentialMove < 0) or (bestPotentialMove > 6) or len(Stacks[bestPotentialMove]) >= 6:
      bestPotentialMove = randint(0,6)

  if worstPotential == 0:

    print("Possible Move Value Error?")

    worstPotentialMove = -1

    while (worstPotentialMove < 0) or (worstPotentialMove > 6) or len(Stacks[worstPotentialMove]) >= 6:
      worstPotentialMove = randint(0,6)

  # Returns the values and position for best maximizing and minimizing moves
  return bestPotentialMove, bestPotential, worstPotentialMove, worstPotential

"""**8 - Minimax**

The minimax algorithm implemented with Connect-4 game logic. The human player is maximizing player and the computer is the minimizing player. The value of a particular state is weighted based on how close it gets to a game-winning scenario: if the state represents a winning game, is value is the winning score, or if there are no other moves left, its value is 0. Otherwise, the value of the state is weight of the best move for the current player.
"""

import math
from random import randint

def minimax(board, Stacks, depth, isMax, player, computer):

  # Checks if there is a win
  score = checkWin(player, computer, board)
  if score == 10:
    return score
  if score == -10:
    return score
  # Checks if there are no moves left
  if not movesLeft(Stacks):
    return 0

  # Gets the piece being used by the human player
  playerPiece = player.getPiece()
  # Gets the piece being used by the computer
  computerPiece = computer.getPiece()

  if isMax == True:
    # Maximizing player

    print("Maximizing Player")

    # Intializes the best score
    best = -math.inf

    # Gets the set of best moves for the current game state
    moveResults = MoveFinder(player, computer, board, Stacks)
    # Parses the values and positions for the best moves
    bestPos, bestMoveVal, worstPos, worstMoveVal = moveResults

    # Sets the current move and move value to the move and move value of the 
    # best maximizing move
    colPos = bestPos
    currMoveVal = bestMoveVal
    
    # If the value of the current move is better than the best score, the best
    # score is set the value of the current move
    if currMoveVal > best:
      best = currMoveVal

    print('Column ', colPos, ' has ', len(Stacks[colPos]), ' pieces in it')
    
    # Obtains the row position of the current move by using the height of the 
    # stacks as the offset from the bottom of the board
    rowPos = 5-len(Stacks[colPos])

    # Places a piece onto the stack indicated by the current move. A piece is 
    # placed on the correpsonding position on the visual board
    Stacks[colPos].push(player.getPiece())
    board[rowPos][colPos] = Stacks[colPos].peek()

    print('Placing a ', playerPiece, ' in (', rowPos, ', ', colPos, ')')
    # DELETE LATER
    printBoard(board)
    # Calls minimax on the game state after placing the current move. The value 
    # of the best move is set to the max of the current best value and the 
    # result of minimax  
    best = max(best, minimax(board, Stacks, depth+1, False, player, computer))
    print('Clearing (', rowPos, ', ', colPos, ')')
    # Clears the current move from the board and stack
    board[rowPos][colPos] = ' '
    Stacks[colPos].pop()

    # Returns the best score
    return best

    pass

  else:
    # Minimizing player

    print("Minimizing Player")

    best = math.inf

    moveResults = MoveFinder(computer, player, board, Stacks)

    bestPos, bestMoveVal, worstPos, worstMoveVal = moveResults

    print("Best position: ", bestPos, ", Best value: ", bestMoveVal, ", Worst position: ", worstPos, ", Worst value: ", worstMoveVal)

    colPos = worstPos
    currMoveVal = worstMoveVal

    if currMoveVal < best:
      best = currMoveVal
    
    print('Column ', colPos, ' has ', len(Stacks[colPos]), ' pieces in it')
    
    rowPos = 5-len(Stacks[colPos])

    Stacks[colPos].push(computer.getPiece())
    board[rowPos][colPos] = Stacks[colPos].peek()



    print('Placing a ', computerPiece, ' in (', rowPos, ', ', colPos, ')')
    # DELETE LATER
    printBoard(board)
    best = min(best, minimax(board, Stacks, depth+1, True, player, computer))
    print('Clearing (', rowPos, ', ', colPos, ')')
    board[rowPos][colPos] = ' '
    Stacks[colPos].pop()

    return best

    pass

"""**9 - Find Best Move**

The driver code for the computer's logic. The computer tests two moves: placing a piece in the first column (the default move) and a move generated by the move finder. The minimax algorithm is called on the move from the move finder to score it. If minimax scores the move finder move higher than the default move, the move finder move is returned instead.
"""

def findBestMove(player, computer, board, Stacks):
  bestVal = 1000
  bestMove = 0
  
  moveResults = MoveFinder(computer, player, board, Stacks)

  _, _, colPos, _ = moveResults
  """
  while len(Stacks[colPos]) >= 6:
      colPos = randint(0,6)
  """

  print('Column ', colPos, ' has ', len(Stacks[colPos]), ' pieces in it')
    
  rowPos = 5-len(Stacks[colPos])

  Stacks[colPos].push(computer.getPiece())
  board[rowPos][colPos] = Stacks[colPos].peek()

  moveVal = minimax(board, Stacks, 0, True, player, computer)
  board[rowPos][colPos] = ' '
  Stacks[colPos].pop()
  
  if moveVal < bestVal:
    bestMove = colPos
    bestVal = moveVal

  print('COMPUTER: The best column (val: ,', bestVal, ') to drop a piece in is: ', bestMove)
  print()
  return bestMove

"""**10 - Move**

Places the move that was created for the computer from **Find Best Move** onto the board.
"""

# Move
from random import randint

def move(player, computer, board, Stacks):

    print("Minimizing Player")
    
    bestMove = findBestMove(player, computer, board, Stacks)

    Set0 = {'1','2','3','4','5','6','7'}
    #pos = randint(0,6)
    pos = bestMove
    if len(Stacks[pos]) < 6:
          Stacks[pos].push(computer.getPiece())
          board[6-len(Stacks[pos])][pos] = \
              Stacks[pos].peek()

    return board, Stacks

"""**11 - Human Move**

Takes in input from the human player and implements their move onto the board. The difference between **Human Move** and **Move** is that Human Move takes in manual input and does not call minimax.
"""

# The drive code for the human player's turn
def humanMove(player, computer, board, Stacks):

  #bestMove = findBestMove(player, computer, board, Stacks)

  """
  print('---------------------- THE REAL BOARD ----------------------')
  printBoard(board)
  print('---------------------- THE REAL BOARD ----------------------')
  """
  #print('The best move would be column ', bestMove)

  # Initializes the move for the player
  choice = -1

  # Asks the player for the column they wish to place a piece in. Continues 
  # asking until the player enters a column that is not full
  while (choice < 0) or (choice > 6) or len(Stacks[int(choice)]) == 6:
    try:
      choice = int( input('Choose a column to place a piece in: ').split()[0] )
    except:
      choice = int( input('Please enter the number of the desired column: ').split()[0] )
  
  pos = choice

  # Places the piece onto the stack corresponding to the chosen column and also
  # places the piece on the visual board
  if len(Stacks[pos]) < 6:
          Stacks[pos].push(player.getPiece())
          board[6-len(Stacks[pos])][pos] = \
              Stacks[pos].peek()
              
  return board, Stacks

"""**12 - Player**

The class representing a player. Both human users and the computer are players. The **Player** class tracks which piece a player has been assigned and how many pieces they have left.
"""

# Class stack (for each column)
class Player:

    # Initializes a new player. They are given 21 pieces to start, but the 
    # type of the pieces is not set yet
    def __init__(self, numPieces):
        self.piece = ''
        self.numPieces = numPieces
    
    # Sets the type of piece the player is using (either X or O)
    def setPiece(self, piece):
      self.piece = piece

    # Returns the piece the player is currently using
    def getPiece(self):
      return self.piece

    # Adds 1 to the player's piece count
    def increasePieces(self):
      self.numPieces = self.numPieces + 1
    
    # Subtracts 1 from the player's piece count
    def decreasePieces(self):
      self.numPieces = self.numPieces - 1

    def getNumPieces(self):
      return self.numPieces

"""**13 - Game Logic**

An object that contains the functions necessary for running the game (user input, printing the board, handling turns, etc).
"""

class GameLogic:

  def __init__(self):
    self.human = Player(21)
    self.computer = Player(21)
    self.board = initBoard()
    self.Stacks = initStacks()
    print('---------------------------- CONNECT 4 ----------------------------')
    print('To play: enter an integer between 1 to 7 ' + \
          'corresponding to each \ncolumn in the board. ' + \
          'Whoever stacks 4 pieces next to each other, ' + \
          '\neither horizontally, vertically or diagonally wins.')

  def assignPieces(self):
    humanPiece = ''

    print()
    
    while humanPiece != 'X' and humanPiece != 'x' and humanPiece != 'O' and humanPiece != 'o':
      humanPiece = str( input('Choose X or O: ') )

    if humanPiece == 'X' or humanPiece == 'x':
        self.human.setPiece('X')
        self.computer.setPiece('O')
    else:
        self.human.setPiece('O')
        self.computer.setPiece('X')
    
    print()
    print('You will be: ', self.human.getPiece())
    print('The computer will be: ', self.computer.getPiece())
  
  def runGame(self):
    while movesLeft(self.Stacks) == True and (self.human.getNumPieces() > 0 and self.computer.getNumPieces() > 0):
        printBoard(self.board)
        print('Moves left: ')
        print('Player: ', self.human.getNumPieces(), " | Computer: ", self.computer.getNumPieces())
        # Human player
        humanMove(self.human, self.computer, self.board, self.Stacks)
        printBoard(self.board)
        game = checkWin(self.human, self.computer, self.board)
        if game == 10:
            print(self.human.getPiece(), ' wins!')
            break
        self.human.decreasePieces()
        # Computer player
        move(self.human, self.computer, self.board, self.Stacks)
        printBoard(self.board)
        game = checkWin(self.human, self.computer, self.board)
        if game == -10:
            print(self.computer.getPiece(), ' wins!')
            break
        self.computer.decreasePieces()
    print('Good game.')

"""**14 - Main**

The driver code for the Connect-4 game.
"""

# Main program
def main():

    connect_four = GameLogic()
    connect_four.assignPieces()
    connect_four.runGame()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 20:43:07 2019

@author: xumin
"""
import numpy as np
import random


#part a and b

class Vertex: 
    '''
    * @name: __init__
    * @description: the constructor of the class, save the input board
    * @param board: the input board which is saved in a 3X3 matrix
    '''
    def __init__(self,board):
        self.board = board
    '''
    * @name: get_status
    * @description: check the result of the current board
    * @return: the result('X wins', 'O wins' or 'in progress')
    '''    
    def get_status(self):        
        #check all rows
        for i in range(3):
            #if the current row has three same element
            if self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2]:
                if self.board[i][0] == 1:
                    return "X wins"
                if self.board[i][0] == -1:
                    return "O wins"
        #check all cols
        for i in range(3):
            #if the current col has three same element
            if self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i]:
                if self.board[0][i] == 1:
                    return "X wins"
                if self.board[0][i] == -1:
                    return "O wins"
        #check diagonal
        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]:
            if self.board[0][0] == 1:
                return "X wins"
            if self.board[0][0] == -1:
                return "O wins"        
        #check diagonal
        if self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0]:
            if self.board[0][2] == 1:
                return "X wins"
            if self.board[0][2] == -1:
                return "O wins"
        
        return 'in progress'
    '''
    * @name: get_children
    * @description: get all possible board with one additional move from the current board
    * @return: the result('X wins', 'O wins' or 'in progress')
    '''         
    def get_children(self,index):
        #get the current row and col
        row = index // 3
        col = index % 3
        #the 8 neighbors
        offsetRow = [-1,-1,-1, 0, 0, 1, 1, 1]
        offsetCol = [-1, 0, 1,-1, 1,-1, 0, 1]
        #the list to save final results
        result = []
        
        for i in range(8):
            y = row + offsetRow[i]
            x = col + offsetCol[i]
            
            if y>=0 and y<3 and x>=0 and x<3:
                if self.board[y][x] == 0:
                    result.append(3*y+x)
        return result
    '''
    * @name: isFull
    * @description: check whether the current board is full
    * @return: boolean, whether the current boad is full
    '''    
    def isFull(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return False
        return True
    '''
    * @name: get_empty
    * @description: get all empty positinos on the board
    * @return: list, the list storing all position indexes
    '''     
    def get_empty(self):
        result = []
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    result.append(row*3+col)
                    
        return result
    '''
    * @name: print_board
    * @description: print the board with "X" and "O"
    '''  
    def print_board(self):
        matrix = []
        for i in range(3):
            row = []
            for j in range(3):
                if self.board[i][j] == 0:
                    row.append(" ")
                elif self.board[i][j] == 1:
                    row.append("X")
                else:
                    row.append("O")
            matrix.append(row)
        
        for row in range(3):
            s=''
            s = s+matrix[row][0]+" | "+matrix[row][1]+" | "+matrix[row][2]
            print(s)
     

#part c

         
'''
* @name: calculate_probability
* @description: calculate the win probability of all possible moves
* @param currentBoard: the object of Class Vertex storing the current board
* @param myTurn: the input indicate whose turn it is('X' or 'O')
* @return: dict, the total outcome and win times of each possible move
'''     
def calculate_probability(currentBoard,myTurn):
    emptyPositions = currentBoard.get_empty()
    emptyNum = len(emptyPositions)
    
    #initialize the final result
    result = []
    
    #base condition
    if emptyNum == 0:
        return result

    
    #get the number to be placed
    myNumber = 0
    if myTurn == 'X':
        myNumber = 1
        otherMove = 'O'
    else:
        myNumber = -1
        otherMove = 'X'
        
    #loop for all possiblities
    for position in emptyPositions:
        
        #intialize the total possiblities and win outcomes of current move
        totalResult = 0
        winResult = 0
        
        #get the row and col of the current empty position
        row = position//3
        col = position%3
        #get the current board
        board = np.copy(currentBoard.board)
        #set the current empty position by my Number
        board[row][col] = myNumber
        #create a new object of class Vertex based on the modified board
        newBoard = Vertex(board)
        #get the output of next move
        outcome = newBoard.get_status()
        
        #if win
        if outcome.startswith(myTurn):
            totalResult = 1
            winResult = 1
            result.append({"move":position,"total":totalResult, 'win':winResult}) 
        #if no direct result
        elif outcome == 'in progress':
            #if the board is full
            if newBoard.isFull():
                totalResult = 1
                winResult = 0
            #if the board is not full
            else:
                #loop all empty positions after the new move                
                newEmptyMoves = newBoard.get_empty()

                for newPosition in newEmptyMoves:
                    tempBoard = np.copy(newBoard.board)
                    tempRow = newPosition//3
                    tempCol = newPosition%3
                    #move a move as the other player
                    tempBoard[tempRow][tempCol] = -myNumber
                    
                    oppositeMove = Vertex(tempBoard)
                    #if the other player wins
                    if oppositeMove.get_status().startswith(otherMove):                        
                        totalResult = totalResult+1    
                    elif oppositeMove.isFull():
                        totalResult = totalResult+1
                    else:
                        tempResult = calculate_probability(oppositeMove,myTurn)
                        if len(tempResult)!= 0:
                            for item in tempResult:
                                totalResult = totalResult + item['total']
                                winResult = winResult + item['win']
                                
                
            result.append({"move":position,"total":totalResult, 'win':winResult})
        else:
            totalResult = 1
            winResult = 0
            result.append({"move":position,"total":totalResult, 'win':winResult}) 
            
    return result
            
'''
* @name: computer_move
* @description: make the move based on calculation of winning probability of all possible moves
* @param currentBoard: the object of Class Vertex storing the current board
* @param myTurn: the input indicate whose turn it is('X' or 'O')
* @return: Vertex, the object of Class Vertex after the move
'''         
def computer_move(currentBoard,myTurn):
    
    currentStatus = currentBoard.get_status()
    
    if currentStatus == 'O wins' or currentStatus == 'X wins':
        print(currentStatus)
        return currentBoard
    elif currentStatus == 'in progress' and currentBoard.isFull():
        print('It`s a tie!')
        return currentBoard
    
    possiblities = calculate_probability(currentBoard,myTurn)
    
    maxPossiblity = -1
    finalMove = -1
    totalWins = 0
    totalNum = 0
    
    board = np.copy(currentBoard.board)
    
    for move in possiblities:
        winRate = move['win']/move['total']
        if winRate>maxPossiblity:
            maxPossiblity = winRate
            finalMove = move['move']
            totalWins = move['win']
            totalNum = move['total']
    
    #get the row and col of the current empty position
    row = finalMove//3
    col = finalMove%3
    
    #get the number to be placed
    myNumber = 0
    if myTurn == 'X':
        myNumber = 1
    else:
        myNumber = -1
        
    board[row][col] = myNumber
    
    newBoard = Vertex(board)
    
    #print("The total number of possible outcome is "+str(totalNum))
    #print("The total number of possible wins is "+str(totalWins))
    
    return newBoard
           
    
    
    
##test case 1    
#A = np.array([[ 0, 0,-1],
#              [ 0, 1, 1],
#              [ 1, 0,-1]])   
#a = Vertex(A)
#nextMove = computer_move(a,'O')
#print(nextMove.board)
#
##test case 2    
#B = np.array([[ 0, 0,-1],
#              [ 0, 0, 0],
#              [ 0, 0, 0]])
#b = Vertex(B)
#nextMove = computer_move(b,'X')
#print(nextMove.board)
#
##test case 3
#C = np.array([[ 1, 0, 0],
#              [-1, 0, 0],
#              [ 1,-1, 1]])
#c = Vertex(C)
#nextMove = computer_move(c,'O')
#print(nextMove.board)
#
##test case 4
#D = np.array([[ 0, 0, 0],
#              [ 0,-1, 0],
#              [ 0, 0, 0]])
#d = Vertex(D)
#nextMove = computer_move(d,'X')
#print(nextMove.board)
##test case 5
#E = np.array([[ 0, 0, 0],
#              [ 0, 0, 0],
#              [ 0, 0, 0]])
#e = Vertex(E)
#nextMove = computer_move(e,'X')
#print(nextMove.board)
    


#part d

def game():
    #initialize the new board:
    board = np.array([[ 0, 0, 0],
                      [ 0, 0, 0],
                      [ 0, 0, 0]])
    initialBoard = Vertex(board)
    #print some welcome message
    print("Welcome to Tic-tac-toe! I`ll use ‘X’ and you`ll use 'O', now let`s see who goes first")
    #generate a random number between 0 and 1
    print("Generatering a random number to decide who goes first:")
    print("0 : I`ll go fisrt")
    print("1 : You`ll go fisrt")
    
    a = random.randint(0,1)
    if a == 0:
        msg = "I`ll go fisrt"
    else:
        msg = "You`ll go fisrt"
        
    print("The number is "+str(a)+", "+msg)
    
    #if the user starts first,wait for first move
    if a == 1:
        #print the initial board
        print("Here is the current board:")
        initialBoard.print_board()
        
        #check whether the input is valid
        isValid = False
        
        #loop until the input is valid
        while not isValid:
            #get user`s input coordinate
            move = input("Please enter move(in 'row,column' format and starts from 1):")
            move = np.array(move.split(','),dtype=int)
            row = move[0]-1
            col = move[1]-1           
      
            index = 3*row+col
            
            #check if it`s in the valid positions list
            emptyPositions = initialBoard.get_empty()
            
            if index in emptyPositions:
                isValid = True
            else:
                print("Invalid input, please input again!")
        
        #set the board based on user`s input        
        newMove = np.copy(initialBoard.board)
        newMove[row][col] = -1
        
        #declare a new Vertex object
        newBoard = Vertex(newMove)
        #print the board after move
        print("After move:")
        newBoard.print_board()
    else:
        #the initial board is our input
        newMove = np.copy(initialBoard.board)
        newBoard = Vertex(newMove)
    

    #get the status of current board, only process if the status is in process    
    result = newBoard.get_status()
    
    while result == 'in progress':
        #computer move
        print("My turn:")
        newBoard = computer_move(newBoard,'X')
        
        #get the new status
        result = newBoard.get_status()
        
        if newBoard.isFull():
            break
        
        if result != 'in progress':
            break
        
        #if still in process,print the board and wait for user`s input
        print("After move:")
        newBoard.print_board()
        
        
        print("Your turn:")
        
        #check whether the input is valid
        isValid = False
        #loop until the input is valid
        while not isValid:
            #get user`s input coordinate
            move = input("Please enter move(in 'row,column' format and starts from 1):")
            move = np.array(move.split(','),dtype=int)
            row = move[0]-1
            col = move[1]-1           
      
            index = 3*row+col
            #check if it`s in the valid positions list
            emptyPositions = newBoard.get_empty()
            
            if index in emptyPositions:
                isValid = True
            else:
                print("Invalid input, please input again!")
        
        #set the board based on user`s input
        newMove = np.copy(newBoard.board)
        newMove[row][col] = -1
        #declare a new Vertex object
        newBoard = Vertex(newMove)
        #print the board after move
        print("After move:")
        newBoard.print_board()
        #get the new status
        result = newBoard.get_status()
        
        if newBoard.isFull():
            break
    #print the final result and the final board    
    print("Final results:")
    newBoard.print_board()
    
    if result == 'in progress':
        print('Nobody won!')
    elif result == 'O wins':
        print('Good game! You won!')
    else:
        print("I won!")

if __name__=='__main__':
    game()       
      
        
        
        
    
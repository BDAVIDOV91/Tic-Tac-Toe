from tkinter import *
import numpy as np

sizeOfBoard = 800
symbolSize = (sizeOfBoard / 3 - sizeOfBoard / 8) / 2
symbolThickness = 30
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
GreenColor = '#7BC043'


class Tic_Tac_Toe():

    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=sizeOfBoard, height=sizeOfBoard)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        

        self.initializeBoard()
        self.player_X_turns = True
        self.boardStatus = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.resetBoard = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initializeBoard(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * sizeOfBoard / 3, 0, (i + 1) * sizeOfBoard / 3, sizeOfBoard)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * sizeOfBoard / 3, sizeOfBoard, (i + 1) * sizeOfBoard / 3)

    def play_again(self):
        self.initializeBoard()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.boardStatus = np.zeros(shape=(3, 3))

    
    def draw_O(self, logicalPosition):
        logicalPosition = np.array(logicalPosition)
        gridPosition = self.convertLogicalToGridPosition(logicalPosition)
        self.canvas.create_oval(gridPosition[0] - symbolSize, gridPosition[1] - symbolSize,
                                gridPosition[0] + symbolSize, gridPosition[1] + symbolSize, width=symbolThickness, 
                                outline=symbol_O_color)

    def draw_X(self, logicalPosition):
        gridPosition = self.convertLogicalToGridPosition(logicalPosition)
        self.canvas.create_line(gridPosition[0] + symbolSize, gridPosition[1] - symbolSize,
                                 gridPosition[0] + symbolSize, gridPosition[1] + symbolSize, width=symbolSize,
                                 fill=symbol_X_color)
        self.canvas.create_line(gridPosition[0] - symbolSize, gridPosition[1] - symbolSize,
                                gridPosition[0] + symbolSize, gridPosition[1] - symbolSize, width=symbolThickness,
                                fill=symbol_X_color)     

    def displayGameOver(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'


        self.canvas.delete('all')
        self.canvas.create_text(sizeOfBoard / 2, sizeOfBoard / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(sizeOfBoard / 2, 5 * sizeOfBoard / 8, font="cmr 40 bold", fill=GreenColor,
                                text=score_text)
        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O) : ' + str(self.O_score) + '\n'
        score_text += 'Tie'
        self.canvas.create_text(sizeOfBoard / 2, 3 * sizeOfBoard / 4 , font="cmr 30 bold", fill=GreenColor,
                                text=score_text)
        self.resetBoard = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(sizeOfBoard / 2, 15 * sizeOfBoard / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)


    def convertLogicalToGridPosition(self, logicalPosition):
        logicalPosition = np.array(logicalPosition, dtype=int)
        return (sizeOfBoard / 3) * logicalPosition + sizeOfBoard / 6

    def convertGridToLogicalPosition(self, gridPosition):
        gridPosition = np.array(gridPosition)
        return np.array(gridPosition // (sizeOfBoard /3), dtype=int)

    def isGridOccupied(self, logicalPosition):
        if self.boardStatus[logicalPosition[0]][logicalPosition[1]] == 0:
            return False
        else:
            return True

    def isWinner(self, player):

        player = -1 if player == "X" else 1

        for i in range(3):
            if self.boardStatus[i][0] == self.boardStatus[i][1] == self.boardStatus[i][2] == player:
                return True
            if self.boardStatus[0][i] == self.boardStatus[1][i] == self.boardStatus[2][i] == player:
                return True


        if self.boardStatus[0][0] == self.boardStatus[1][1] == self.boardStatus[2][2] == player:
            return True
        if self.boardStatus[0][2] == self.boardStatus[1][1] == self.boardStatus[2][0] == player:
            return True

        return False

    def isTie(self):
        r, c = np.where(self.boardStatus == 0 )
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def isGameOver(self):
        self.X_wins = self.isWinner('X')
        if not self.X_wins:
            self.O_wins = self.isWinner('O')

        if not self.O_wins:
            self.tie = self.isTie()
        gameover = self.X_wins or self.O_wins or self.tie
        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')
        return gameover

    def click(self, event):
        gridPosition = [event.x, event.y]
        logicalPosition = self.convertGridToLogicalPosition(gridPosition)

        if not self.resetBoard:
            if self.player_X_turns:
                if not self.isGridOccupied(logicalPosition):
                    self.draw_X(logicalPosition)
                    self.boardStatus[logicalPosition[0]][logicalPosition[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.isGridOccupied(logicalPosition):
                    self.draw_O(logicalPosition)
                    self.boardStatus[logicalPosition[0]][logicalPosition[1]] = 1
                    self.player_X_turns = not self.player_X_turns

        
            if self.isGameOver():
                self.displayGameOver()

        else:
            self.canvas.delete('all')
            self.play_again()
            self.resetBoard = False


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
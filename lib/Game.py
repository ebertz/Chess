from tkinter import *
from .Pieces import *

#represents a single square on the chess board
class Space():
    def __init__(self,game,x,y):
        self.piece = None
        self.x = x
        self.y = y
        self.game = game
        #draw graphics
        fill = 'gray' if (self.x + self.y)%2 else 'white'
        self.rect = game.canvas.create_rectangle(
            60*x,60*y, 60*x + 60, 60*y + 60, fill = fill)
        #bind click function to square
        game.canvas.tag_bind(self.rect, '<Button-1>', self.onClick)

    def onClick(self, event):
        if self.game.selected is not None:
            if self in self.game.selected.get_moves():
                self.game.selected.unhighlight_moves()
                self.game.selected.move(self.x,self.y)
                self.game.switch_turn()

class Game():
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width = 480, height = 480)
        self.canvas.pack()
        self.board = self.draw_board()
        self.place_pieces()
        self.turn = 'white'
        self.selected = None
        
    def draw_board(self):
        board = [[None for x in range(8)] for y in range(8)]
        for x in range(8):
            for y in range(8):
                board[x][y] = Space(self,x,y)
        return board

    def switch_turn(self):
        self.selected = None
        if self.turn is 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def place_pieces(self):
        #place pawns
        for i in range(8):
            b_space = self.board[i][1]
            w_space = self.board[i][6]
            b_space.piece = Pawn(self,'black',b_space.x,b_space.y)
            w_space.piece = Pawn(self,'white',w_space.x,w_space.y)
        #place rooks
        for i in [0,7]:
            b_space = self.board[i][0]
            w_space = self.board[i][7]
            b_space.piece = Rook(self,'black',b_space.x,b_space.y)
            w_space.piece = Rook(self,'white',w_space.x,w_space.y)
        #place knights
        for i in [1,6]:
            b_space = self.board[i][0]
            w_space = self.board[i][7]
            b_space.piece = Knight(self,'black',b_space.x,b_space.y)
            w_space.piece = Knight(self,'white',w_space.x,w_space.y)
        #place bishops
        for i in [2,5]:
            b_space = self.board[i][0]
            w_space = self.board[i][7]
            b_space.piece = Bishop(self,'black',b_space.x,b_space.y)
            w_space.piece = Bishop(self,'white',w_space.x,w_space.y)
        #place kings and queens
        self.board[4][0].piece = Queen(self, 'black', 4,0)
        self.board[3][0].piece = King(self, 'black', 3,0)
        self.board[4][7].piece = Queen(self, 'white', 4,7)
        self.board[3][7].piece = King(self, 'white', 3,7)
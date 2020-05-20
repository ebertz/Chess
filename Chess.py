from tkinter import *
from abc import ABC, abstractmethod
from PIL import Image, ImageTk

images = []
pieces = []

def inBounds(x,y):
    if x < 0 or y < 0:
        return 0
    if x > 7 or y > 7:
        return 0
    return 1

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
            
            
            


class Piece():

    def __init__(self, game,color,x,y, img):
        self.x = x
        self.y = y
        self.game = game
        self.color = color
        self.dir = 1 if color is 'black' else -1
        self.rawimage = ImageTk.PhotoImage(file = img)
        images.append(self.rawimage)
        self.image = self.game.canvas.create_image((x*60 + 30,y*60 + 30), image = self.rawimage)
        game.canvas.tag_bind(self.image, '<Button-1>', self.onClick)
        #game.canvas.tag_bind(self.image, '<Enter>', self.highlight_moves)
        #game.canvas.tag_bind(self.image, '<Leave>', self.unhighlight_moves)
        pieces.append(self)

    def onClick(self, event):
        print('{},{}'.format(self.x,self.y))
        if self.game.turn is self.color:
            if self.game.selected is not None:
                self.game.selected.unhighlight_moves()
            self.highlight_moves()
            self.game.selected = self
        else:
            if self.game.selected is None:
                return
            if self.game.board[self.x][self.y] in self.game.selected.get_moves():
                self.game.selected.unhighlight_moves()
                self.game.selected.move(self.x,self.y)
                self.game.switch_turn()
        
    def highlight_moves(self):
        for space in self.get_moves():
            self.game.canvas.itemconfig(space.rect, fill = 'red')

    def unhighlight_moves(self):
        for space in self.get_moves():
            fill = 'gray' if (space.x + space.y)%2 else 'white'
            self.game.canvas.itemconfig(space.rect, fill = fill)
    def move(self, x, y):
        space = self.game.board[x][y]
        if space not in self.get_moves():
            print("invalid move: [{},{}] to [{},{}]".format(self.x,self.y,x,y))
            return
        self.game.board[self.x][self.y].piece = None
        #update fields
        self.x, self.y = x,y
        #delete image
        self.game.canvas.delete(self.image)
        #redraw image
        self.image = self.game.canvas.create_image((x*60 + 30, y*60 + 30), image = self.rawimage)
        self.game.canvas.tag_bind(self.image, '<Button-1>', self.onClick)
        if self.game.board[x][y].piece is not None:
            self.game.canvas.delete(self.game.board[x][y].piece.image)
        self.game.board[x][y].piece = self
        print('moved')
    def get_moves(self):
        pass
    
    

class Pawn(Piece):
    def __init__(self, game,color,x,y):
        image_path = r'chess_pieces/b_pawn.png' if color is 'black' else r'chess_pieces/w_pawn.png'
        Piece.__init__(self, game, color, x, y, image_path)
    def get_moves(self):
        moves = []
        #check forward movement
        dist = [1]
        if (self.color is 'black' and self.y is 1) or (self.color is 'white' and self.y is 6):
            dist = [1,2]
            
        for i in dist:
            x,y = self.x, self.y + i * self.dir
            if not inBounds(x,y):
                continue
            space = self.game.board[x][y]
            if space.piece is None:
                moves.append(space)
            else:
                break
        #check diagonal captures
        for i in [-1,1]:
            x,y = self.x + i, self.y + self.dir
            if not inBounds(x,y):
                continue
            space = self.game.board[x][y]
            if space.piece is not None and space.piece.color is not self.color:
                moves.append(space)
        #self.game.canvas.delete(self.image)
        return moves
            
            
class Rook(Piece):
    def __init__(self, game,color,x,y):
        image_path = r'chess_pieces/b_rook.png' if color is 'black' else r'chess_pieces/w_rook.png'
        Piece.__init__(self, game, color, x, y, image_path)
    def get_moves(self):
        moves = []
        dirs = [[-1,0],[1,0],[0,-1],[0,1]]
        for d in dirs:
            x,y = self.x, self.y
            x,y = x+d[0], y+d[1]
            while inBounds(x,y):

                move = self.game.board[x][y]
                if move.piece is None:
                    moves.append(move)
                elif move.piece.color is not self.color:
                    moves.append(move)
                    break
                else:
                    break
                x,y = x+d[0], y+d[1]
        return moves
            
             
class Knight(Piece):
    def __init__(self, game,color,x,y):
        image_path = r'chess_pieces/b_knight.png' if color is 'black' else r'chess_pieces/w_knight.png'
        Piece.__init__(self, game, color, x, y, image_path)
    def get_moves(self):
        moves = []
        dirs = [[-2,-1],[-2,1],[-1,2],[1,2],[2,-1],[2,1],[-1,-2],[1,-2]]
        for dir in dirs:
            x,y = self.x+dir[0],self.y+dir[1]
            if not inBounds(x,y):
                continue
            if self.game.board[x][y].piece is None:
                moves.append(self.game.board[x][y])
            elif self.game.board[x][y].piece.color is not self.color:
                moves.append(self.game.board[x][y])
        return moves
        
class Bishop(Piece):
    def __init__(self, game,color,x,y):
        image_path = r'chess_pieces/b_bishop.png' if color is 'black' else r'chess_pieces/w_bishop.png'
        Piece.__init__(self, game, color, x, y, image_path)
    def get_moves(self):
        moves = []
        for xdir in [-1,1]:
            for ydir in [-1,1]:
                x,y = self.x + xdir, self.y + ydir
                while inBounds(x,y):
                    move = self.game.board[x][y]
                    if move.piece is None:
                        moves.append(move)
                    elif move.piece.color is not self.color:
                        moves.append(move)
                        break
                    else:
                        break
                    x,y = x+ xdir, y + ydir
        return moves                      
        
class Queen(Piece):
    def __init__(self, game,color,x,y):
        image_path = r'chess_pieces/b_queen.png' if color is 'black' else r'chess_pieces/w_queen.png'
        Piece.__init__(self, game, color, x, y, image_path)
    def get_moves(self):
        moves = []
        dirs = [[-1,0],[1,0],[0,-1],[0,1]]
        for d in dirs:
            x,y = self.x, self.y
            x,y = x+d[0], y+d[1]
            while inBounds(x,y):

                move = self.game.board[x][y]
                if move.piece is None:
                    moves.append(move)
                elif move.piece.color is not self.color:
                    moves.append(move)
                    break
                else:
                    break
                x,y = x+d[0], y+d[1]

        for xdir in [-1,1]:
            for ydir in [-1,1]:
                x,y = self.x + xdir, self.y + ydir
                while inBounds(x,y):
                    move = self.game.board[x][y]
                    if move.piece is None:
                        moves.append(move)
                    elif move.piece.color is not self.color:
                        moves.append(move)
                        break
                    else:
                        break
                    x,y = x+ xdir, y + ydir
        return moves
    
class King(Piece):
    def __init__(self, game,color,x,y):
        image_path = r'chess_pieces/b_king.png' if color is 'black' else r'chess_pieces/w_king.png'
        Piece.__init__(self, game, color, x, y, image_path)
    def get_moves(self):
        moves = []
        for xdir in range(-1,2):
            for ydir in range(-1,2):
                x,y = self.x+xdir, self.y+ydir
                if not inBounds(x,y):
                    continue
                move = self.game.board[x][y]
                if move.piece is None:
                    moves.append(move)
                elif move.piece.color is not self.color:
                    moves.append(move)
        return moves


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

        
    
mygame = Game()
mygame.root.mainloop()
import time
start = time.time()
for piece in pieces:
    piece.get_moves()
total = time.time() - start
print(total)
    

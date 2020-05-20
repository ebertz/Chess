from abc import ABC, abstractmethod
from PIL import Image, ImageTk

def inBounds(x,y):
    if x < 0 or y < 0:
        return 0
    if x > 7 or y > 7:
        return 0
    return 1

class Piece():
    def __init__(self, game,color,x,y, img):
        self.x = x
        self.y = y
        self.game = game
        self.color = color
        self.dir = 1 if color is 'black' else -1
        self.rawimage = ImageTk.PhotoImage(file = img)
        self.image = self.game.canvas.create_image((x*60 + 30,y*60 + 30), image = self.rawimage)
        game.canvas.tag_bind(self.image, '<Button-1>', self.onClick)
        #game.canvas.tag_bind(self.image, '<Enter>', self.highlight_moves)
        #game.canvas.tag_bind(self.image, '<Leave>', self.unhighlight_moves)

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
from static_main import B




class Piece:
    def __init__(self, x, y, type, image):
        self.x=x
        self.y=y
        self.type=type
        self.image = image
        self.atx = 0
        self.aty = 0
        pass
    
    def render(self, win, int, size):
        win.blit(B[self.image], (int+(size*self.x), int+(size*self.y)))
        pass
    
    def tick(self, x, y):
        self.x=x
        self.y=y
        self.moved = True
    
    def check(self, piece):
        if piece == 0:
            return True
        return False
    
    def vaild(self, a, b):
        if a+b>7 or a+b<0:
            return False
        return True

    def diagonal_kill(self, board, move_to):
        moves = []
        if self.vaild(self.y,move_to) and self.x<7 and not self.check(board[self.y+move_to][self.x+1]) and self.type!=board[self.y+move_to][self.x+1].type:
            moves.append([self.x+1, self.y+move_to])
        
        if self.vaild(self.y,move_to) and self.x>0 and not self.check(board[self.y+move_to][self.x-1]) and self.type!=board[self.y+move_to][self.x-1].type:
            moves.append([self.x-1, self.y+move_to])
        return moves
class Pawn_Piece(Piece):
    
    def __init__(self, x, y, type='w'):

        image = 9
        if type == 'b':
            image = 3
        super().__init__(x, y, type,image)
        self.king = self.moved = False
        pass
    
    def get_moves(self, board):
        moves = []
        move_to = -1
        if self.type == 'b':
            move_to = 1

        if (self.y+move_to==7 ) or (self.y+move_to==0 ):
            self.king = True
        if self.check(board[self.y+move_to][self.x]):
            moves.append([self.x, self.y+move_to])
            if self.moved==False:
                moves.append([self.x, self.y+move_to*2])
        
        list = (self.diagonal_kill(board, move_to))
        for i in list:
             moves.append(i)
        return moves

 
class Rock_Piece(Piece):

    def __init__(self, x, y, type='w'):
        image = 11
        if type == 'b':
            image = 5
        super().__init__(x, y,type, image)
        pass

    def get_moves(self, board):
        moves = [ ]
        c=1
        for i in range(self.y-1, -1, -1):#up
            if not self.check(board[self.y-c][self.x]):
                if board[self.y-c][self.x].type ==self.type:
                    break
                elif type(board[self.y-c][self.x]) == King_Piece:
                    return 'check_mate'
                else:
                    moves .append([self.x,i])
                    break
            moves .append([self.x,i])
            c+=1
        c=1
        for i in range(self.y+1,8,1):#down
            if not self.check(board[self.y+c][self.x]):
                if board[self.y+c][self.x].type ==self.type:
                    break
                elif type(board[self.y+c][self.x]) == King_Piece:
                    return 'check_mate'
                else:
                    moves .append([self.x,i])
                    break
            moves .append([self.x,i])
            c+=1
        c=1
        for i in range(self.x+1,8,1):#right
            if not self.check(board[self.y][self.x+c]):
                if board[self.y][self.x+c].type ==self.type:
                    break
                elif type(board[self.y][self.x+c]) == King_Piece:
                    return 'check_mate'
                else:
                    moves .append([i,self.y])
                    break
            moves .append([i, self.y])
            c+=1
        c=1
        for i in range(self.x-1,-1,-1):#right
            if not self.check(board[self.y][self.x-c]):
                if board[self.y][self.x-c].type ==self.type:
                    break
                elif type(board[self.y][self.x-c]) == King_Piece:
                    return 'check_mate'
                else:
                    moves .append([i,self.y])
                break
            moves.append([i, self.y])
            c+=1
        return moves

class Queen_Piece(Piece):

    def __init__(self, x, y, type='w'):
        image = 10
        if type == 'b':
            image = 4
        super().__init__(x, y, type, image)
    def get_moves(self, board):
        moves = []
        
        list = Rock_Piece.get_moves(self, board)
        list1 = Bishop_Piece.get_moves(self, board)
        if type(list) is str or type(list1) is str:
            return 'check_mate'
        for i in list:
            moves.append(i)
        for i in list1:
            moves.append(i)
        return moves

class Bishop_Piece(Piece):

    def __init__(self, x, y, type='w'):
        image = 6
        if type == 'b':
            image = 0
        super().__init__(x, y, type,image)
        pass

    def get_moves(self, board):
        moves = [ ]
        a,b = 1, 1
        for i in range(4):
            k = Bishop_Piece.move_to(self, self.y, self.x, a, b, board)
            if type(k) is str:
                return 'check_mate'
            for i in k:
                moves.append(i)
            if a==-1:
                b*=-1
            a*=-1
        return moves

    
    def move_to(self, y, x, inc_y, inc_x, board):
        moves=[]    
        #self.y-c>=0 and self.x+c<8:
        while self.vaild(y, inc_y) and  self.vaild(x, inc_x): 
            if not self.check(board[self.y+inc_y][self.x+inc_x]) :
                if  board[self.y+inc_y][self.x+inc_x].type == self.type:
                    break
                if type(board[self.y+inc_y][self.x+inc_x]) == King_Piece:
                    return 'check_mate'
                else:
                    moves.append([self.x+inc_x, self.y+inc_y])
                    break
            moves.append([self.x+inc_x, self.y+inc_y])
            if inc_y<0:
                inc_y-=1
            else:
                inc_y+=1
            if inc_x<0:
                inc_x-=1
            else:
                inc_x+=1
        return moves
       
class Knight_Piece(Piece):

    def __init__(self, x, y, type='w'):
        image = 8
        if type == 'b':
            image = 2
        super().__init__(x, y,type, image)

    def get_moves(self, board):
        moves = []
        a=1
        b=1
        v=1
        for i in range(4):
            if i>1:
                b=2
                v=-1
            for i in self.move_to(self.y, self.x, a*(b+1*v), b):
                row, col = i
                if not self.check(board[col][row]) and board[col][row].type == self.type:
                    continue
                if not self.check(board[col][row]) and type(board[col][row]) == King_Piece:
                    return 'check_mate'
                moves.append(i)
                
            a*=-1
        return moves    


    
    def move_to(self, v, h, inc, inc_2):
        moves = []
        if self.vaild(v, inc):
            if self.vaild(h,inc_2):
                moves.append([ h+inc_2, v+inc])
            if self.vaild(h, -inc_2):
                moves.append([h-inc_2, v+inc])  
        return moves

class King_Piece(Piece):

    def __init__(self, x, y, type='w'):
        image = 7
        if type == 'b':
            image = 1
        super().__init__(x, y,type, image)
        pass
        
    def get_moves(self, board):
        moves = []
        for i in range(self.y-1, max(-1,self.y-2),-1):#up
            if  self.check(board[self.y-1][self.x]):
                moves .append([self.x, self.y-1])

        for i in range(self.y+1,min(self.y+2, 8),1):#down
            if  self.check(board[self.y+1][self.x]):
                moves .append([self.x,self.y+1])


        for i in range(self.x+1,min(self.x+2, 8),1):#right
            if  self.check(board[self.y][self.x+1]):
                moves .append([self.x+1, self.y])

        for i in range(self.x-1,max(-1,self.x-2),-1):#right
            if  self.check(board[self.y][self.x-1]):
                moves.append([self.x-1, self.y])
        list = self.diagonal_kill(board, 1)
        list2 = self.diagonal_kill(board, -1)
        for i in list:
            moves.append(i)
        for i in list2:
            moves.append(i)
        return moves



import pickle
import threading
from button import Button
from network import Network
from piece import King_Piece, Knight_Piece, Pawn_Piece, Queen_Piece, Rock_Piece, Bishop_Piece
from static_main import*


list_moves = []
piece = None
class Game:
    def __init__(self, game_type) -> None:
        self.board = []
        self.BOAED_NUMBERS = pygame.transform.scale(pygame.image.load("image/numbers.png"), (15, HEIGHT-250))
        self.BOAED_TEXT = pygame.transform.scale(pygame.image.load("image/text.png"), (WIDTH-250, 20))
        self.BOAED = pygame.transform.scale(pygame.image.load("image/board_alt.png"), (WIDTH, HEIGHT))
        self.INTENT = 150
        self.CELL_SIZE = 77
        self.active=False
        self.texts = []
        self.game_type = game_type
        self.recv = False
        self.n = None

        pass
    def render_pecies(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]!=0:
                    self.board[i][j].render(WINDOW, self.INTENT, self.CELL_SIZE)

    def render_moves(self):
        for move in list_moves:
            if move:
                row, col = move
                pygame.draw.circle(WINDOW, BLUE, (self.INTENT+30+(self.CELL_SIZE*row), self.INTENT+20+(self.CELL_SIZE*col)), 15)


    def render(self):
        WINDOW.blit(BACKGROUND, (0, 0))
        WINDOW.blit(self.BOAED, (0, 0))
        WINDOW.blit(self.BOAED_NUMBERS, (800, 130))
        WINDOW.blit(self.BOAED_TEXT, (130, 850))
        WINDOW.blit(CHAT, (1140, 15))
        if self.active == False and self.recv:
            WINDOW.blit(READ_NOTE, (1170, 15))


        self.render_pecies()
        self.render_moves()

    def vaild(self, a, b):
        if a+b>7 or a+b<0:
            return False
        return True
    def ckeck_mate(self, thing):

        for i in range(8):
            for j in range(8):
                f=0    
                if self.board[i][j]!=0:
                    move = self.board[i][j].get_moves(self.board)
                    for y in move:
                        if y == 'c':
                            return True
                        if type(thing)!=str:
                            if type(thing) == King_Piece and self.board[i][j].type != thing.type and y in thing.get_moves(self.board):
                                thing.get_moves(self.board).remove(y)
                                return False
                            if self.board[y[1]][y[0]] == thing:
                                a = y[1]-f[1]
                                b = f[0]-y[0]
                            
                                f= y[0] 
                                y= y[1]
                                while self.vaild(y,a) and self.vaild(f,-b):
                                    if type(self.board[y][f])==King_Piece :
                                        return True
                                    y = y+a
                                    f = f-b
                                if type(self.board[y][f])==King_Piece :
                                        return True
                            
                                return False

                            f=y
        return False
    def flip(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]!=0:

                    c= 7-self.board[i][j].y  
                    self.board[i][j], self.board[c][j] = self.board[c][j], self.board[i][j] 
        for i in range(8):
            for j in range(8):
                if self.board[i][j]!=0:
                    if self.board[i][j].type == 'w':
                        self.board[i][j].type = 'b'
                    else:
                        self.board[i][j].type = 'w'
                
                    self.board[i][j].y=7-self.board[i][j].y
    def tick(self, y, x):
        global list_moves, piece

        if self.board[y][x]!=0 and [x, y] in list_moves:
            self.board[y][x] = self.board[piece.y][piece.x]
            self.board[piece.y][piece.x] =0
        
        elif [x, y] in list_moves:
            self.board[piece.y][piece.x], self.board[y][x] =self. board[y][x], self.board[piece.y][piece.x]

        elif self.board[y][x]!=0:
            piece = self.board[y][x]
            #if ckeck_mate(piece):
            #   return
            list_moves = self.board[y][x].get_moves(self.board)
            return
        else:
            return   
        piece.atx = piece.x
        piece.aty = piece.y     

        piece.tick(x, y)
        list_moves=[]   
        if type(piece) == Pawn_Piece and piece.king == True:
            self.board[piece.y][piece.x] = Queen_Piece(piece.x, piece.y, piece.type) 

        if self.game_type == 'local':
            self.flip()
        else:
            self.n.send(piece)
    def get_pos(self,pos):
        x, y = pos[0], pos[1]
         
        if x >=self.INTENT-10 and x<800 and y >=self.INTENT-10 and y<800:
            x=x-self.INTENT+10
            x=(x//self.CELL_SIZE)
            y=y-self.INTENT+10
            y=(y//self.CELL_SIZE)


            return x, y
        
        elif x>=WIDTH-60 and y>=15 and y <=75:
            if self.active == True:
                self.active = False
                self.reset()
                return None
            self.BOAED = pygame.transform.scale(pygame.image.load("image/board_alt.png"), (WIDTH-100, HEIGHT-100))
            #self.BOAED_NUMBERS = pygame.transform.scale(self.BOAED_NUMBERS, (WIDTH-350, 15))   
            #self.BOAED_TEXT = pygame.transform.scale(self.BOAED_TEXT, (10, HEIGHT-350))   
            self.INTENT = 135
            self.CELL_SIZE = 70 
            self.active = True
        return None

    def init(self):
        for i in range(8):
            self.board.append([])
            for j in range(8):
                if i==0:
                    if (j==0 or j==7):
                        self.board[i].append(Rock_Piece(j, i, 'b'))
                    elif j==1 or j == 6:
                        self.board[i].append(Knight_Piece(j, i, 'b'))
                    elif (j==2 or j==5):
                        self.board[i].append(Bishop_Piece(j, i, 'b'))
                    elif j==3:
                        self.board[i].append(Queen_Piece(j, i, 'b'))
                    elif j==4 :
                        self.board[i].append(King_Piece(j, i, 'b'))
                    else:   
                        self.board[i].append(0)
                elif i == 1:
                    self.board[i].append(Pawn_Piece(j, i, 'b'))
                elif i==6:
                    self.board[i].append(Pawn_Piece(j, i))
                elif i==7:
                    if (j==0 or j==7):
                        self.board[i].append(Rock_Piece(j, i ))
                    elif j==1 or j == 6:
                        self.board[i].append(Knight_Piece(j, i ))
                    elif(j==2 or j==5):
                        self.board[i].append(Bishop_Piece(j, i ))
                    elif j==3:
                        self.board[i].append(Queen_Piece(j, i))
                    elif j==4 :
                        self.board[i].append(King_Piece(j, i ))
                    else:
                        self.board[i].append(0)
                    
                else:
                    self.board[i].append(0)
        if self.n != None and self.n.get_status() == 'w':
            self.flip()


    def render_input(self, text):
        COLOR = (255, 250, 251)
    
        pygame.draw.rect(WINDOW, COLOR, CHAT_RECT)    
        text_surface = base_font.render(text, True, (0, 0, 0))
        CHAT_RECT.w = max(CHAT_RECT.w, text_surface.get_width()+10)
        CHAT_RECT.x = 1150-text_surface.get_width()  
        WINDOW.blit(text_surface, (CHAT_RECT.x+5, CHAT_RECT.y+5))


    def render_usertext(self):
        space = 0
        
        for text in self.texts:
            text_surface = upper_font.render(text, True, (255, 255, 255))
            WINDOW.blit(text_surface, (1200-(text_surface.get_width()+40), 80+space))
            space+=20  

    def reset(self):
        CHAT_RECT.w = 30
        CHAT_RECT.x = 1150
        self.INTENT = 150
        self.CELL_SIZE = 77
        self.BOAED = pygame.transform.scale(pygame.image.load("image/board_alt.png"), (WIDTH, HEIGHT))


    def send_usertext(self, user_text):
        self.n.server.send(user_text.encode())

    def get_msg(self, n):
        while True:
            t = n.server.recv(256)
            try:
                t.decode()
                 
                self.recv = True
                self.texts.append(t)
               
            except:
                t = pickle.loads(t)
                t.y= 7-t.y  
                self.board[7-t.aty][t.atx], self.board[t.y][t.x] = self.board[t.y][t.x], self.board[7-t.aty][t.atx]
                self.board[t.y][t.x].tick(t.x, t.y)
                 
    def set_network(self, n):
        self.n = n

def game_board(n ):
    text = ''
    b = []
    while True:
        WINDOW.blit(GAME_BOARD_BACKGROUND, (0, 0))
        create_game = 'Create game'
        create_surface = base_font.render(create_game, True, (255, 255, 255))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                break
            if e.type == pygame.MOUSEBUTTONDOWN:
          
                x, y =pygame.mouse.get_pos()
                if x >=(600-(text_surface.get_width()//2 )) and x<text_surface.get_width()+(600-(text_surface.get_width()//2 )) and y>160 and y<text_surface.get_height()+160 :
                    n.server.send("create game".encode())
                    return
                for bt in b:
                    result = bt.get_pressed(e.pos)
                    if result != False:
                        n.server.send("start game".encode())
                        n.server.send(result.encode())
                        return

        n.client_addr()
        obj = (n.server.recv(1024)) 
        if  len((pickle.loads(obj))) == 0:
            text = 'No Active Games!'
            text_surface = base_font.render(text, True, (255, 255, 255))
            WINDOW.blit(text_surface, (600-(text_surface.get_width()//2 ), 80))

        else:
            obj= pickle.loads(obj)
            space = 0
            for i in obj:
                text = str(i )
                text_surface = base_font.render("waiting", True, (255, 255, 255))
                WINDOW.blit(text_surface, (200-(text_surface.get_width()//2 ), 180))
                counter =0
                for bt in b:
                    if text != bt.str    :
                        counter+=1
                if counter == len(b):
                    b.append(Button(text, 100, 250+space))
                for bt in b:
                    bt.render(WINDOW)
                space+=120

        WINDOW.blit(create_surface, (600-(create_surface.get_width()//2 ), 160))

        pygame.display.update()

def main(game_type):
    game = Game(game_type)
    if game_type == 'online':
        n  = Network()
        game_board(n  )

        game.set_network(n)

        thread = threading.Thread(target=game.get_msg, args=(n, ))
        thread.start()

    user_text = ''
    game.init()
    running = True
    mate = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
            if e.type == pygame.KEYDOWN:

                if game.active:
                    if(e.key == pygame.K_RETURN):
                        game.send_usertext(user_text )
                        CHAT_RECT.w = 30
                        CHAT_RECT.x = 1150
                        game.texts.append(user_text)
                        user_text = ''
                    else:
                        user_text += e.unicode

            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = game.get_pos(pygame.mouse.get_pos())

                if pos != None:
               
                    if not piece or not mate:
                        game.tick(pos[1], pos[0])
                    #mate = ckeck_mate(' ')
        game.render()

        if game.active:
            game.recv = False
            game.render_input(user_text)
            game.render_usertext( )
            
        pygame.display.update()
    pygame.quit()

def ask():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                break
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                s = 'online'
                if x>=300 and x<900 and y>200 and y<400:
                    s = 'local'
                main(s)

        WINDOW.blit(ASK_BACKGROUND, (0, 0))

        pygame.display.update()

def pre_main():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                break
            if e.type == pygame.MOUSEBUTTONDOWN:
                ask()
          

        WINDOW.blit(BACKGROUND, (0, 0))

        pygame.display.update()

pre_main()
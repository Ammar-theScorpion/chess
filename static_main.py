import pygame
from pygame import mixer

WIDTH, HEIGHT = 900, 900
WINDOW = pygame.display.set_mode((1200, HEIGHT))
pygame.display.set_caption("chess")
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.font.init()
base_font = pygame.font.SysFont('Comic Sans Ms', 64)
upper_font =  pygame.font.SysFont('Comic Sans Ms', 22)
w_pawn = pygame.transform.scale(pygame.image.load("image/white_pawn.png"), (50, 50))
b_pawn = pygame.transform.scale(pygame.image.load("image/black_pawn.png"), (50, 50))
w_rook = pygame.transform.scale(pygame.image.load("image/white_rook.png"), (50, 50))
b_rook = pygame.transform.scale(pygame.image.load("image/black_rook.png"), (50, 50))
w_bishop = pygame.transform.scale(pygame.image.load("image/white_bishop.png"), (50, 50))
b_bishop = pygame.transform.scale(pygame.image.load("image/black_bishop.png"), (50, 50))
w_king = pygame.transform.scale(pygame.image.load("image/white_king.png"), (50, 50))
b_king = pygame.transform.scale(pygame.image.load("image/black_king.png"), (50, 50))
w_queen = pygame.transform.scale(pygame.image.load("image/white_queen.png"), (50, 50))
b_queen = pygame.transform.scale(pygame.image.load("image/black_queen.png"), (50, 50))
w_knight = pygame.transform.scale(pygame.image.load("image/white_knight.png"), (50, 50))
b_knight = pygame.transform.scale(pygame.image.load("image/black_knight.png"), (50, 50))
B = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook, w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

 
 

BACKGROUND = pygame.transform.scale(pygame.image.load("image/bc.png"), (1200, HEIGHT))
ASK_BACKGROUND = pygame.transform.scale(pygame.image.load("image/2bc.png"), (1200, HEIGHT))
GAME_BOARD_BACKGROUND = pygame.transform.scale(pygame.image.load("image/bc.jpg"), (1200, HEIGHT))
CHAT = pygame.transform.scale(pygame.image.load("image/chat.png"), (50, 50))
READ_NOTE = pygame.transform.scale(pygame.image.load("image/R.png"), (20, 20))
CHAT_RECT = pygame.Rect(1150, HEIGHT-50, 30, 30)

#CHECK_MATE = pygame.mixer.music.load("image/checkmate.wav")
#pygame.mixer.music.play()
#CHECK_MATE.set_volume(0.25)
BLUE = (0, 0 ,255)
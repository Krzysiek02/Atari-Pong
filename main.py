# box2.py
import sys
import pygame
import random
# COLORS
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# INITIALIZE THE GAME
pygame.init()   # to zawsze na starcie
size = width, height = (1600, 800)
screen = pygame.display.set_mode(size)   # display Surface
pygame.display.set_caption('Atari Pong')

# CLOCK
FPS = 120  # frames per second setting
clock = pygame.time.Clock()

# SETTINGS
PAD_HEIGHT = 100
PAD_WIDTH = 15
PAD_SPEED_PLAYER = 4.2
BALL_SPEED = [3,3]
BALL_SIZE = 15

# POINTS
player1_score = 0
player2_score = 0

class Pad(pygame.sprite.Sprite):
    def __init__(self, color, PAD_WIDTH, PAD_HEIGHT):
        super().__init__()
        self.image = pygame.Surface([PAD_WIDTH, PAD_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, BALL_SIZE):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
    def movement(self):
        self.rect.x += BALL_SPEED[0]
        self.rect.y += BALL_SPEED[1]
        
# LOAD IMAGES
player2_PAD = Pad(blue,PAD_WIDTH, PAD_HEIGHT)   # Rect object
player2_PAD.rect.topleft = (50, (height - PAD_HEIGHT) //2 )
player1_PAD = Pad(white,PAD_WIDTH, PAD_HEIGHT)   # Rect object
player1_PAD.rect.topleft = (width - PAD_WIDTH - 50, (height - PAD_HEIGHT) //2)
ball = Ball(red, BALL_SIZE)
ball.rect.topleft = (width //2, height // 2)

font = pygame.font.Font(None, 60)   # load the pygame default font
winning_points = 11


computer = 0
game_play = 2

# MAIN GAME LOOP
while True:
    # HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # QUIT Event
            pygame.quit()
            sys.exit(0)
    
    
    # MENU
    if game_play == 2:
        screen.fill(black)
        
        # TEXT
        text1 = font.render("Press C to play against Computer", True, white)
        text2 = font.render("Press P to play against Player", True, white)
        text_rect1 = text1.get_rect(center=(width // 2, height // 3))
        text_rect2 = text2.get_rect(center=(width // 2, height // 3 +50))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        
        # CHOOSING
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:  # Computer
            computer = 1
            game_play = 1 #start game
        if keys[pygame.K_p]:  # Player
            computer = 0
            game_play = 1  # start game

        pygame.display.flip()
    
    # ADDING PADS AND BALL TO GROUP
    PADS_GROUP = pygame.sprite.Group()
    PADS_GROUP.add(player1_PAD,player2_PAD)
    
    BALL_GROUP = pygame.sprite.Group()
    BALL_GROUP.add(ball)

    
    # CHECKING INPUTS
    keys = pygame.key.get_pressed()   # tablica/tuple 0/1
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit(0)
    
    # PLAYER 1
    if keys[pygame.K_UP]:
        if player1_PAD.rect.y>2:
            player1_PAD.rect.y -= PAD_SPEED_PLAYER
    if keys[pygame.K_DOWN]:
        if player1_PAD.rect.y<height-PAD_HEIGHT - 2:
            player1_PAD.rect.y += PAD_SPEED_PLAYER   
    
    if computer==0:
        
        # PLAYER 2
        if keys[pygame.K_w]:
            if player2_PAD.rect.y>2:
                player2_PAD.rect.y -= PAD_SPEED_PLAYER
        if keys[pygame.K_s]:
            if player2_PAD.rect.y<height-PAD_HEIGHT - 2:
                player2_PAD.rect.y += PAD_SPEED_PLAYER    
    else:
        # COMPUTER
        if ball.rect.x < width //1.2:
            if ball.rect.centery < player2_PAD.rect.centery:
                if player2_PAD.rect.y>2:
                    player2_PAD.rect.y += -PAD_SPEED_PLAYER + 0.6
            elif ball.rect.centery > player2_PAD.rect.centery:
                if player2_PAD.rect.y<height-PAD_HEIGHT -2:
                    player2_PAD.rect.y += PAD_SPEED_PLAYER - 0.6
                    
    
    
    
    # BALL COLLISION WITH SCREEN
    if ball.rect.y >= height - ball.rect.height or ball.rect.y <= 0: 
        BALL_SPEED[1] = -BALL_SPEED[1]    
        
    # BALL COLLISION WITH PAD
    #if pygame.sprite.groupcollide(BALL_GROUP, PADS_GROUP, False, False):
    #    if BALL_SPEED[0] >0:
    #        BALL_SPEED[0] = random.uniform(8,18)
    #    else:
    #        BALL_SPEED[0] = random.uniform(-8,-18)
    #    BALL_SPEED[0] = -BALL_SPEED[0]
    #    if BALL_SPEED[1] >= 0:
    #        BALL_SPEED[1] = random.randint(0, 8)
    #    if BALL_SPEED[1] < 0:
    #        BALL_SPEED[1] = random.randint(-8, 0)
    
    # BALL COLLISION WITH PAD
    if player1_PAD.rect.colliderect(ball.rect) or player2_PAD.rect.colliderect(ball.rect):
        if player1_PAD.rect.colliderect(ball.rect):
            ball.rect.x = player1_PAD.rect.left - ball.rect.width - 5
        if player2_PAD.rect.colliderect(ball.rect):
            ball.rect.x = player2_PAD.rect.right + 5
        if BALL_SPEED[0] >0:
            BALL_SPEED[0] = random.uniform(6,11)
        else:
            BALL_SPEED[0] = random.uniform(-6,-11)
        BALL_SPEED[0] = -BALL_SPEED[0]
        if BALL_SPEED[1] >= 0:
            BALL_SPEED[1] = random.randint(0, 6)
        if BALL_SPEED[1] < 0:
            BALL_SPEED[1] = random.randint(-6, 0)
            
    # POINT FOR PLAYER 1
    if ball.rect.x <= 2:
        player1_score +=1
        ball.rect.topleft = (800, 350)
        BALL_SPEED = [5,5]
        
    # POINT FOR PLAYER 2
    if ball.rect.x >= width-2:
        player2_score +=1
        ball.rect.topleft = (800, 350)
        BALL_SPEED = [5,5]
    
    
    # WIN
    if player1_score >= winning_points or player2_score >= winning_points:
        screen.fill(black)
        if player1_score >= winning_points:
            text_win = "Player 1 won!"
        else:
            text_win = "Player 2 won!"
        win_text = font.render(text_win, True, white)
        text_rect1 = win_text.get_rect(center=(width // 2, height // 2))
        screen.blit(win_text, text_rect1)
        
        quit_text = font.render("Click anywhere to quit", True, white)
        quit_rect1 = win_text.get_rect(center=(width // 2-100, height // 2 + 100))
        screen.blit(quit_text, quit_rect1)
        game_play = 0
        pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit(0)
        
    # DRAWING
    screen.fill(black)   # na nowo czarny ekran
    
    
    # SHOWING POINTS
    text1 = "P1: {}".format(player1_score)
    text2 = "P2: {}".format(player2_score)
    player1_text = font.render(text1, True, white)
    player2_text = font.render(text2, True, white)
    text_rect1 = player1_text.get_rect(center=(width *3 // 4, 50))
    text_rect2 = player2_text.get_rect(center=(width // 4, 50))
    screen.blit(player1_text, text_rect1)
    screen.blit(player2_text, text_rect2)
    
    if game_play == 1:
        
        # SPRITES DRAWING
        PADS_GROUP.update()   # wywołuje update() dla sprites
        BALL_GROUP.update() # po co
    
        PADS_GROUP.draw(screen)
        BALL_GROUP.draw(screen)

        #LINES DRAWING
        pygame.draw.aaline(screen, green, (width // 2, height *3 // 4 - 50), (width // 2, height //4 + 50), 1)
        pygame.draw.aaline(screen, green, (width -3 , 0), (width -3, height), 1)
        pygame.draw.aaline(screen, green, (2, 0), (2, height), 1)
        
        # BALL UPDATE MOVEMENT
        ball.movement()
        pygame.display.flip()
        
    clock.tick(FPS)


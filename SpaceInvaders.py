import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()
#create screen
screen=pygame.display.set_mode((800,600))

#score
scorev=0
#font=pygame.font.Font('freesansbold.ttf',32)#size
font = pygame.font.SysFont('Comic Sans', 32, False,False)
tx=10
ty=10

#game over text
over_font= pygame.font.SysFont('Comic Sans', 72, False,False)

def show_score(x,y):
    score=font.render("Score: "+str(scorev),True,(255,255,255))
    screen.blit(score,(x,y))

def gameovert():
    over=font.render("Game over!",True,(255,255,255))
    screen.blit(over,(365,300))  
    
#background
background=pygame.image.load('space.png')
#background sound
mixer.music.load('music.mp3')
mixer.music.play(-1)

#title and icon(32px,png)
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#player
playerimg=pygame.image.load('battleship.png')
playerX=370
playerY=480
x_change=0

#enemy
enemyimg=[]
enemyX=[]
enemyY=[]
ex_change=[]
ey_change=[]
n=6
for i in range(n):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    ex_change.append(0.8)
    ey_change.append(40)

#bullet
#ready-cant see bullet
#fire-bullet is fired
bulletimg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bx_change=0
by_change=5
bullet_state="ready"

def player(x,y):
    screen.blit(playerimg,(x,y))#draws image

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
#game loop, runs until user clicks close button

def fire_bullet(x,y):
    
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def collision(enemyX,enemyY,bulletX,bulletY):
    dist=math.sqrt(((enemyX-bulletX)**2)+((enemyY-bulletY)**2))
    if dist<27:
        return True
    else:
        return False
while True:
    #background colour(r,g,b)
    screen.fill((128,128,128))
    #background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
            
        #if key is pressed check if left or right
        if event.type==pygame.KEYDOWN:#pressing key
            
            if event.key==pygame.K_LEFT:
                x_change=-1
            if event.key==pygame.K_RIGHT:
                x_change=1
            if event.key==pygame.K_SPACE:
                if bullet_state == "ready":
                    b=pygame.mixer.Sound('laser.wav')
                    b.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
                
        if event.type==pygame.KEYUP:#release key
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                x_change=0
            
    
    playerX+=x_change
    #boundary
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    
    #enemy movement
    for i in range(n):
        
        #game over
        if enemyY[i]>440:
            for j in range(n):
                enemyY[j]=2000
            gameovert()
            break
            
        enemyX[i]+=ex_change[i]
        if enemyX[i]<=0:
            ex_change[i]=0.8
            enemyY[i]+=ey_change[i]
        elif enemyX[i]>=736:
            ex_change[i]=-0.8
            enemyY[i]+=ey_change[i]
        #collision
        c=collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if c:
            explode=pygame.mixer.Sound('explosion.wav')
            explode.play()
            bulletY=480
            bullet_state="ready"
            scorev+=1            
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
        enemy(int(enemyX[i]),int(enemyY[i]),i)
        
    #bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=by_change
        
            
    player(playerX,playerY)
    show_score(tx,ty)
    
    #have to update window for every change
    pygame.display.update()

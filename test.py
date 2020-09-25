from math import *
import pygame
pygame.init()
#the width and height of the window
winwidth = 1400
winheight = 750
win = pygame.display.set_mode((winwidth,winheight))
run = True
playerWidth = 40
playerHeight = 60   
class character:
    def __init__(self, width, height, vel, jumpCount, id):
        self.width = width
        self.height = height
        self.vel = vel
        self.x = winwidth - width
        self.y = winheight - height
        self.isJump = False
        self.jumpCount = jumpCount
        self.constJump = jumpCount
        self.faceRight = -1
        self.id = id
        self.hitbox = (self.x + 20, self.y, 40,60)

    def playerMove(self):
        keys = pygame.key.get_pressed()
        if self.id == 0:
            if keys[pygame.K_LEFT] and self.x > self.vel:
                self.x -= self.vel
                self.faceRight = -1
            if keys[pygame.K_RIGHT] and self.x < winwidth - self.width:
                self.x += self.vel
                self.faceRight = 1
            if not self.isJump:
                if keys[pygame.K_SPACE]:
                    self.isJump = True
            else:
                if self.y <= winheight - self.height:
                    self.y -= int(self.jumpCount) // 2
                    self.jumpCount -= 0.2
                else:
                    self.y = winheight - self.height
                    self.isJump = False
                    self.jumpCount = self.constJump

    def draw(self):
        self.hitbox = (self.x, self.y, 40, 60)
        pygame.draw.rect(win, (255, 255, 255), self.hitbox)

MC = character(playerWidth,playerHeight,2,14,0)

class bullet:                           
    def __init__(self,x,y,direction,vel,rad):               
        self.direction = direction
        self.vel = vel 
        self.x = x
        self.y = y
        self.rad = rad
    
    def update(self):
        if self.x < winwidth and self.x > 0:
            self.x += self.vel*self.direction
            return True
        return False

    def draw(self):
        pygame.draw.circle(win,(255,255,255),(self.x,self.y),self.rad)
        
class platform:
    def __init__(self,x,y,width,image):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.tileSize = playerWidth
    
    def draw(self):
        for i in range(self.width):
            pygame.draw.rect(win,(255,0,0),(self.x+self.tileSize*i,self.y,self.tileSize,self.tileSize))

class healthBar:
    def __init__(self,image):
        self.image = image
        self.x = 20
        self.y = 20 
        self.width = 100
        self.height = 40
    def draw(self):
        win.blit(self.image,(self.x,self.y))
        
    

health = pygame.image.load("healthbar.png")
small = pygame.transform.rotozoom(health,0,0.3)
hb = healthBar(small)
test = platform(700,winheight-100,5,"abc")








def draw():
    win.fill((0,255,255))
    MC.draw()
    hb.draw()
    
    for x in bullets:
        x.draw()
    test.draw()
    pygame.display.update()




#mainloop
bullets = []
while run:
    #DON'T CHANGE THIS
    #START
    #I set the delay as 10 ms since it will give good fps
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #END
    for x in bullets:
        if not x.update():
            bullets.pop(bullets.index(x))

    MC.playerMove()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break
    if keys[pygame.K_x]:
        bullets.append(bullet(round(MC.x+MC.width//2),round(MC.y+MC.height//2),MC.faceRight,8,4))

    draw()
pygame.quit()
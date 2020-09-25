import pygame
pygame.init()
# the width and height of the window
winwidth = 1000
winheight = 500
win = pygame.display.set_mode((winwidth, winheight))
run = True
playerWidth = 40
playerHeight = 60
bulletTime = 0


# Classes
class character:
    def __init__(self, x, y, width, height, vel, jumpCount, id, walkleft, walkright, idleleft, idleright, damage):
        self.width = width
        self.height = height
        self.vel = vel
        self.x = x
        self.y = y
        self.isJump = True
        self.jumpCount = 0
        self.constJump = jumpCount
        self.faceRight = -1
        self.id = id
        self.hitbox = (self.x + 20, self.y, 40, 60)
        self.isMove = False
        self.moveCount = 0
        self.idleleft = idleleft
        self.idleright = idleright
        self.walkleft = walkleft
        self.walkright = walkright
        self.damage = damage
        self.level = 0


    def playerMove(self):
        keys = pygame.key.get_pressed()
        if self.id == 0:
            if keys[pygame.K_LEFT] and self.x > self.vel:
                if self.faceRight == 1:
                    self.moveCount = 0
                self.x -= self.vel
                self.faceRight = -1
                self.isMove = True
            if keys[pygame.K_RIGHT] and self.x < winwidth - self.width:
                if self.faceRight == -1:
                    self.moveCount = 0
                self.x += self.vel
                self.faceRight = 1
                self.isMove = True
            if not self.isJump:
                if keys[pygame.K_SPACE]:
                    self.jumpCount = self.constJump
                    self.isJump = True
                    self.isMove = True
            else:
                if self.y <= winheight - self.height:
                    self.y -= int(self.jumpCount) // 2
                    self.jumpCount -= 0.2
                else:
                    self.y = winheight - self.height
                    self.isJump = False
                    self.jumpCount = self.constJump
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not self.isJump:
                self.isMove = False

    def hit(self):
        print('hit')
        pass

    def draw(self):
        self.hitbox = (self.x, self.y, 40, 60)
        if self.moveCount < 79:
            self.moveCount += 1
        else:
            self.moveCount = 0
        if not self.isMove and self.faceRight == 1:
            win.blit(self.idleright[self.moveCount//20], (self.x, self.y))
        elif not self.isMove and self.faceRight == -1:
            win.blit(self.idleleft[self.moveCount//20], (self.x, self.y))
        elif self.isMove and self.faceRight == 1:
            win.blit(self.walkright[self.moveCount//20], (self.x, self.y))
        elif self.isMove and self.faceRight == -1:
            win.blit(self.walkleft[self.moveCount//20], (self.x, self.y))


class bullet:
    def __init__(self, x, y, direction, vel, rad):
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
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.rad)


class platform:
    def __init__(self, x, y, width, image):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.tileSize = playerWidth

    def draw(self):
        for i in range(self.width):
            pygame.draw.rect(
                win, (255, 0, 0), (self.x+self.tileSize*i, self.y, self.tileSize, self.tileSize))


class healthBar:
    def __init__(self, image):
        self.image = image
        self.x = 20
        self.y = 20
        self.lives = 3

    def draw(self):
        win.blit(self.image, (self.x, self.y))

    def hit(self):
        if self.lives == 1:
            return False
        self.lives -= 1
        return True


class checkPoint:
    def __init__(self, x, y, width, height, image, level):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.level = level
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.onAnimation = False
        self.timer = 0
        self.opened = False
        self.number = -1

    def save(self):
        data = []
        data.append(str(self.level)+"\n")
        data.append(str(MC.x)+"\n")
        data.append(str(MC.x)+"\n")
        with open("savefile.txt", "w") as f:
            f.writelines(data)

    def draw(self):
        win.blit(self.image[0], (self.x, self.y))

    def animation(self):
        if self.timer < 129:
            self.timer += 1
        else:
            self.onAnimation = False
            self.opened = True
            self.timer = 0
            win.blit(self.image[-1], (self.x, self.y))
            return
        win.blit(self.image[self.timer//10], (self.x, self.y))

    def blinkblink(self):
        if self.timer >= 20:
            self.timer = 1
            if self.number == -1:
                self.number = -2
            else:
                self.number = -1
        else:
            self.timer += 1
        win.blit(self.image[self.number], (self.x, self.y))

    def check(self):
        if not self.opened:
            if MC.hitbox[0] + MC.hitbox[2] > self.hitbox[0] and MC.hitbox[0] < self.hitbox[0] + self.hitbox[2]:
                if MC.hitbox[1] + MC.hitbox[3] > self.hitbox[1] and MC.hitbox[1] < self.hitbox[1] + self.hitbox[3]:
                    self.onAnimation = True


class items:
    def __init__(self, x, y, images, itemName, hitbox, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.images = images
        self.itemName = itemName
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.imageCount = 0

    def draw(self):
        if self.imageCount < 79:
            self.imageCount += 1
        else:
            self.imageCount = 0
        win.blit(self.images[self.imageCount//20], (self.x, self.y))


class enemy:
    def __init__(self, width, height, vel, jumpCount, id, walkleft, walkright, idleleft, idleright, damage):
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
        self.hitbox = (self.x + 20, self.y, 40, 60)
        self.isMove = False
        self.moveCount = 0
        self.idleleft = idleleft
        self.idleright = idleright
        self.walkleft = walkleft
        self.walkright = walkright
        self.damage = damage

    def move(self):
        pass

    def draw(self):
        pygame.draw.rect(win(255, 255, 0))


# When game start, this code will get the x,y position and the level the character is at
with open("savefile.txt", "r") as f:
    data = f.readlines()
    startx = int(data[1])
    starty = int(data[2])
    level = int(data[0])

# Item Functions


def speedPotion(item):
    MC.vel = 2.5


def addHealth(item):
    hb.lives = 3


def doubleDamage(item):
    MC.damage *= 2


# Importing Images
idleLeft = []
idleRight = []
walkLeft = []
walkRight = []
CP1 = []
for x in range(1, 5):
    idleLeft.append(pygame.image.load("idleLeft/"+str(x)+".png"))
for x in range(1, 5):
    idleRight.append(pygame.image.load("idleRight/"+str(x)+".png"))
for x in range(1, 5):
    walkRight.append(pygame.image.load("walkingRight/"+str(x)+".png"))
for x in range(1, 5):
    walkLeft.append(pygame.image.load("walkingLeft/"+str(x)+".png"))
for x in range(1, 14):
    temp = (pygame.image.load("CP1/"+str(x)+".png"))
    CP1.append(pygame.transform.rotozoom(temp, 0, 2))

# Creating Objects
MC = character(startx, starty, playerWidth, playerHeight, 2, 14,
               0, walkLeft, walkRight, idleLeft, idleRight, 2)
health = pygame.image.load("healthbar.png")
small = pygame.transform.rotozoom(health, 0, 0.3)
hb = healthBar(small)
test = platform(700, winheight-100, 5, "abc")
check1 = checkPoint(920, 380, 80, 120, CP1, 1)
Ttile1 = platform(500,350,3,1)
Ttile2 = platform(0,100,4,1)
Ttile3 = platform(0,140,4,1)
Ttile4 = platform(250,200,3,1)
# Defining Functions

def tutorial1():
    win.fill((0,0,0))
    Ttile1.draw()
    Ttile2.draw()
    Ttile3.draw()
    Ttile4.draw()
    MC.draw()
    pygame.display.update()

def draw():
    win.fill((0, 0, 0))

    hb.draw()
    for x in bullets:
        x.draw()
    test.draw()
    if check1.onAnimation:
        check1.animation()
    else:
        if check1.opened == False:
            check1.draw()
        else:
            check1.blinkblink()
    
    MC.draw()
    pygame.display.update()


# mainloop
bullets = []
while run:
    # DON'T CHANGE THIS
    # START
    # I set the delay as 10 ms since it will give good fps
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # END
    for x in bullets:
        if x.y - x.rad > MC.hitbox[1] and x.y + x.rad < MC.hitbox[1] + MC.hitbox[3]:
            if x.x - x.rad > MC.hitbox[0] + MC.hitbox[2] and x.x + x.rad < MC.hitbox[0]:
                MC.hit()
                bullets.pop(bullets.index(x))

        if not x.update():
            bullets.pop(bullets.index(x))

    MC.playerMove()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        break
    if keys[pygame.K_x] and len(bullets) < 1:
        bullets.append(bullet(round(MC.x+MC.width//2),
                              round(MC.y+MC.height//2), MC.faceRight, 12, 4))
    check1.check()

    draw()
pygame.quit()

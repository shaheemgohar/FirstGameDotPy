import pygame

pygame.init()
screenw = 500
screenh = 480
screen = pygame.display.set_mode((screenw,screenh))
pygame.display.set_caption("First game")
clk = pygame.time.Clock()
#to images
walkRight = [pygame.image.load(f'R{n}.png') for n in range(1,10)]
walkLeft = [pygame.image.load(f'L{n}.png') for n in range(1,10)]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

class player(object):
    def __init__(self,x,y , width, height):
        self. x= x
        self. y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right  = False
        self.walkCount = 0
        self.standing = True
        # #x, y
        # x = 50 #char spawn  co-ord
        # y = 400
        # width = 64 #char w
        # height = 64 #char h
        # vel = 5
        # #to jump
        # isJump = False
        # jumpCount = 10
        # #var to keep track of which direc is the char moving
        # #are they moving and how many steps have they already moved
        # left = False
        # right = False
        # walkCount = 0
    def draw(self,screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
            #if  moving we move him in that direc
        if not (self.standing):

            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else: #if not standing still we freeze him facing L or R
            # screen.blit(char, (self.x,self.y))
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

class projectile(object):
    def __init__(self,x,y,radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing 
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

def redrawGameScreen():
        screen.blit(bg,(0,0))
        man.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        pygame.display.update()

#main loop
man = player(300,410,64,64)
bullets = []
run = True

while run:
    #will get a list of all the events
    #and then we loop through those to check if they have happenend
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
#we make a list of all the keys this is to constantly move the charac instead of just one key stroke at a time
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y+ man.height//2), 6, (0,0,0),facing ))
    #we check turn by turn
    #if we do it zero then the char will go past the boudary 1xvel
    if keys[pygame.K_LEFT]and man.x >man.vel:
        #if you go down it adds to the y and if you go right it adds to the x
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        #check notes
    elif keys[pygame.K_RIGHT] and man.x < screenw - man.width - man.vel: 
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        # man.right = False
        # man.left = False
        man.walkCount = 0

    if not (man.isJump): #we dont let the user move up or down mid air while jumping is true
        # if keys[pygame.K_UP] and y > vel:
        #     y -= vel
        # if keys[pygame.K_DOWN] and y < screenh - height - vel:
        #     y += vel
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1 #so we can start moving downwards when we reach the -ve side of our loop
            man.y -= (man.jumpCount ** 2) * 0.5 * neg#we jump 100 then it subtracts 1 so 90,80
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

#now we draw rec charac
    redrawGameScreen()
    clk.tick(27)
pygame.quit()

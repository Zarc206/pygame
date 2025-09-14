import pygame
import math

pygame.init()

screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()
testFont = pygame.font.Font(None,50)

surfaces = []
animations = []
messages = []
aPressed = False
dPressed = False
wPressed = False
sPressed = False

class surfaceImage:
    def __init__(self,imageLocation,x,y):
        self.imageLocation = imageLocation
        self.image = pygame.image.load(imageLocation).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        surfaces.append(self)
    def draw(self):
        screen.blit(self.image,(self.rect.left,self.rect.top))
    def upkeep(self):
        None

class player(surfaceImage):
    def __init__(self,imageLocation,x,y,animationNumber,frameNumber,frameNumbers):
        super().__init__(imageLocation,x,y)
        self.image = pygame.transform.scale2x(self.image)
        self.animationNumber = animationNumber
        self.frameNumber = frameNumber
        self.frameNumbers = frameNumbers
        self.direction = "right"
        self.speed = 2
        self.effect = None
        animations.append(self)

    def draw(self):
        
        self.frameNumber += 0.2
        if self.frameNumber >= self.frameNumbers[self.animationNumber]:
            self.frameNumber = 0
        drawFrameNumber = self.frameNumber
        if self.effect != None:
            self.effect.follow(self)
            self.effect.draw()
        if self.direction == "left":
            drawFrameNumber = math.ceil(8 - self.frameNumber)
        screen.blit(self.image,(self.rect.left,self.rect.top),(200 * math.floor(drawFrameNumber) + 60,200 * self.animationNumber + 60,200,200))

    def upkeep(self):
        if "player attack" in messages and self.animationNumber != 2:
            self.animationNumber = 2
            self.frameNumber = 0
            while "player attack" in messages:
                messages.remove("player attack")
            self.effect = Effect("assets/soldier/attack1.png",self.rect.left,self.rect.top)
        if self.animationNumber != 2:
            self.animationNumber = 0
            if aPressed:
                self.animationNumber = 1
                self.rect.x -= self.speed
                if self.direction == "right":
                    self.direction = "left"
                    self.image = pygame.transform.flip(self.image,True,False)

            if dPressed:
                self.animationNumber = 1
                self.rect.x += self.speed
                if self.direction == "left":
                    self.direction = "right"
                    self.image = pygame.transform.flip(self.image,True,False)
        
            if wPressed:
                self.animationNumber = 1
                self.rect.y -= self.speed
            if sPressed:
                self.animationNumber = 1
                self.rect.y += self.speed
        elif math.floor(self.frameNumber) == self.frameNumbers[self.animationNumber] - 1:
            self.animationNumber = 0
            self.effect = None

class Effect(surfaceImage):
    def __init__(self,imageLocation,x,y):
        super().__init__(imageLocation,x,y)
        self.image = pygame.transform.scale2x(self.image)
        self.frameNumber = 0
        self.direction = "right"
        surfaces.remove(self)
        
    def follow(self,owner):
        self.rect.top = owner.rect.top
        self.rect.left = owner.rect.left
        self.frameNumber = owner.frameNumber
        if self.direction == "right" and owner.direction == "left":
            self.image = pygame.transform.flip(self.image,True,False)
        self.direction = owner.direction

            

    def draw(self):
        drawFrameNumber = self.frameNumber
        if self.direction == "left":
            drawFrameNumber = math.ceil(5 - self.frameNumber)
        screen.blit(self.image,(self.rect.left,self.rect.top),(200 * math.floor(drawFrameNumber) + 60, 60,200,200))




class surfaceText:
    def __init__(self,words,x,y):
        self.words = words
        self.text = testFont.render(words,False,"black").convert()
        self.x = x
        self.y = y
        surfaces.append(self)
    def draw(self):
        screen.blit(self.text,(self.x,self.y))
    def upkeep(self):
        None



background = surfaceImage('assets/background.png',0,0)
startButton = surfaceImage('assets/startButton.png',100,100)


while True:
    for surface in surfaces:
        surface.upkeep()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if startButton.rect.collidepoint(pos):
                if startButton in surfaces:
                    surfaces.remove(startButton)
                messages = []
                grid = surfaceImage('assets/grid.png',50,50)
                soldier = player('assets/soldier/Soldier.png',80 + 76 * 2,60 + 76 * 2,0,0,[6,8,6,6,9,4,4])
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                aPressed = True
            if event.key == pygame.K_d:
                dPressed = True
            if event.key == pygame.K_w:
                wPressed = True
            if event.key == pygame.K_s:
                sPressed = True
            if event.key == pygame.K_o:
                messages.append("player attack")


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                aPressed = False
            if event.key == pygame.K_d:
                dPressed = False
            if event.key == pygame.K_w:
                wPressed = False
            if event.key == pygame.K_s:
                sPressed = False


    for surface in surfaces:
        surface.draw()

    pygame.display.update()
    clock.tick(60)


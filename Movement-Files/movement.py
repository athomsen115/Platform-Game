import pygame, os

pygame.init()
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 500

win = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption("First Moving Pygame")

#need to fix the walk right character (or all the character pieces)
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('halloween-background.jpg')
char = pygame.image.load('standing.png')

bgX = 0
bgX2 = bg.get_width()

#bulletSound = pygame.mixer.Sound("bullet.wav")
#hitSound = pygame.mixer.Sound("hit.wav")
#music = pygame.mixer.music.load("music.mp3")
#pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
score = 0

class Player():
    run = [pygame.image.load(os.path.join('images', str(x) +'.png')) for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images', str(x) +'.png')) for x in range(1,8)]
    slide = [pygame.image.load(os.path.join('images', 'S' + str(x) +'.png')) for x in range(1,8)]
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.sliding = False
        self.walkCount = 0
        self.slideCount = 0
        self.runCount = 0
        self.standing = True
        self.hitbox = (self.x+20, self.y + 7, 24, 53)
        self.lives = 3
        
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        
        self.hitbox = (self.x+20, self.y + 7, 24, 53)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
    def collide(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        self.health -= 1
        print(self.health)
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render("-5", 1, (255,0,0))
        win.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        

class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)  
        

class Enemy():
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')] 
    
    def __init__(self, x, y, width, height, end):
        self.x = x 
        self.y = y 
        self.width = width
        self.height = height
        self.end = end
        self.path = (self.x, self.end)
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x+20, self.y + 7, 24, 53)
        self.health = 10
        self.visible = True
        
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
                
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0]-10, self.hitbox[1]-8, 50, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0]-10, self.hitbox[1]-8, 50 - ((5) * (10-self.health)), 10))
            self.hitbox = (self.x+20, self.y + 7, 24, 53)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)    
            
    def move(self):
        if self.vel > 0: # right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("Hit")
    
    def destroy(self):
        self.health -= self.health
        self.visible = False
        print("Destroyed")
    

def redrawWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: '+ str(score), 1, (0, 0, 0))
    win.blit(text, (10, 10))
    skeleton.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


def main():
    global skeleton, goblin, bullets, font, score
    font = pygame.font.SysFont('comicsans', 30, True)
    skeleton = Player(300, 410, 64, 64)
    goblin = Enemy(100, 410, 64, 64, 300)
    bullets = []
    shootLoop = 0
    run = True
    while run:
        clock.tick(27)
        if goblin.visible == True:
            if skeleton.hitbox[1] + skeleton.hitbox[3] == goblin.hitbox[1] + 5:
                goblin.destroy()
                score += 5
            elif skeleton.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and skeleton.hitbox[1] + skeleton.hitbox[3] > goblin.hitbox[1]:
                if skeleton.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and skeleton.hitbox[0] + skeleton.hitbox[2] > goblin.hitbox[0]:
                    skeleton.collide()
                    score -= 5
        
        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for bullet in bullets:
            if goblin.visible == True:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                    if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                        #hitSound.play()
                        goblin.hit()
                        score += 1
                        bullets.pop(bullets.index(bullet))
            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
                
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and shootLoop == 0:
            #bulletSound.play()
            if skeleton.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(Projectile(round(skeleton.x + skeleton.width//2), round(skeleton.y + skeleton.height//2), 6, (97,215,164), facing))
                
            shootLoop = 1
        
        if keys[pygame.K_LEFT] and skeleton.x > skeleton.vel:
            skeleton.x -= skeleton.vel
            skeleton.left = True
            skeleton.right = False
            skeleton.standing = False
        elif keys[pygame.K_RIGHT] and skeleton.x < SCREEN_WIDTH - skeleton.width - skeleton.vel:
            skeleton.x += skeleton.vel
            skeleton.left = False
            skeleton.right = True
            skeleton.standing = False
        else:
            skeleton.standing = True
            skeleton.walkCount = 0
             
        if not (skeleton.isJump):
            if keys[pygame.K_UP]:
                skeleton.isJump = True
                skeleton.left = False
                skeleton.right = False
                skeleton.walkCount = 0
        else:
            if skeleton.jumpCount >= -10:
                neg = 1
                if skeleton.jumpCount < 0:
                    neg = -1
                skeleton.y -= (skeleton.jumpCount ** 2) * 0.5 * neg
                skeleton.jumpCount -= 1
            else:
                skeleton.isJump = False
                skeleton.jumpCount = 10
    
        redrawWindow()
        
    pygame.quit()


if __name__ == '__main__':
    main()
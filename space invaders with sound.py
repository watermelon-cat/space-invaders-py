import pygame
import random
import time
pygame.init()
pygame.display.set_caption("Space Invaders")
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
gameover = False
my_font = pygame.font.SysFont('Sans Serif', 30)
text_surface = my_font.render('LIVES: ', False, (255, 0, 0))

#game variabels
timer = 0;

#player variable
xpos = 375
ypos = 750
moveLeft = False
moveRight = False
lives = 3

shoot = False
BulletX = xpos+28
BulletY = ypos

pygame.mixer.init()
DieSound = pygame.mixer.Sound("playerdieSPACE.wav")
killsound = pygame.mixer.Sound("killalien.wav")
alienshoot = pygame.mixer.Sound("alienshoot.wav")
missileshoot = pygame.mixer.Sound("missileshoot.wav")


class Missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
        
    def move(self):
        if self.isAlive == True: #only shoot live bullets
            self.ypos+=5 #move down when shot
        if self.ypos > 800: #check if you've hit the bottom of the screen
            self.isAlive = False #set to dead
            self.xpos = -10 #reset to offscreen positoin
            self.ypos = -10
            
    def draw(self):
        if self.isAlive:
            pygame.draw.rect(screen, (219, 50, 56), (self.xpos, self.ypos, 20, 5))
            pygame.draw.rect(screen, (219, 50, 56), (self.xpos+10, self.ypos, 5, 20))

missiles = [] #creates empty list
for i in range(10):
    missiles.append(Missile()) #push wall objects into list




class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0
    def draw(self):
        if self.numHits ==0:
            pygame.draw.rect(screen, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
        if self.numHits ==1:
            pygame.draw.rect(screen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
        if self.numHits ==2:
            pygame.draw.rect(screen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
    
    def collide(self, BulletX, BulletY):
        if self.numHits < 3: #only hits live aliens
            if BulletX > self.xpos: #checks if bullet is right of the left sife of the alien
                if BulletX < self.xpos + 40: #check if the bullet is left of the right side
                    if BulletY < self.ypos + 40: #check if the vullet is above the aliens bottom
                        if BulletY > self.ypos: #check if the bullet is below the top of the alien
                            print("oww") #for testing
                            self.numHits += 1 #set the alien to dead
                            return False #set the bullet to dead
                    
        return True #otherwise keep the bullet alive

walls = [] #create empty list
for k in range(4): #creates 4 sets
    for i in range (2): #handles rows
        for j in range (3): #handles collums
            walls.append(Wall(j*30+200*k+50, i*30+600)) #push wall objects into list




class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
    def move(self, xpos, ypos):
        if self.isAlive == True: #only shoot live bullets
            self.ypos-=5 #move up when shot
        if self.ypos < 0: #check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = xpos #reset to player positoin
            self.ypos = ypos
    def draw(self):
        pygame.draw.rect(screen, (250,250,250), (self.xpos, self.ypos, 3, 20))

#instantiate bullet object
bullet = Bullet(xpos+28, ypos) #create bullet object and pass player position



class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250,250,250), (self.xpos, self.ypos, 40, 40))
    def move(self, time):
        
        #reset what direction you're moving every 8 moves:
        if time % 800 == 0:
            self.ypos += 100 #move down
            self.direction *= -1 #flip direction
            return 0 #resets timer to 0
        
        #move everytime the timer increses by 100:
        if time % 100 == 0:
            self.xpos+=25*self.direction #move right
            #print("moving right")
        
        return time #doesn't reset if first if statement hasn't excetuted
    def collide(self, BulletX, BulletY):
        if self.isAlive: #only hits live aliens
            if BulletX > self.xpos: #checks if bullet is right of the left sife of the alien
                if BulletX < self.xpos + 40: #check if the bullet is left of the right side
                    if BulletY < self.ypos + 40: #check if the vullet is above the aliens bottom
                        if BulletY > self.ypos: #check if the bullet is below the top of the alien
                            print("hit!") #for testing
                            pygame.mixer.Sound.play(killsound)
                            self.isAlive = False #set the alien to dead
                            return False #set the bullet to dead
                    
        return True #otherwise keep the bullet alive
       
armada = [] #creates a empty list
for i in range (4): #handles rows
    for j in range (9): #handle columns
        armada.append(Alien(j*80+50, i*60+50)) #push alien object into list

while not gameover and lives > 0: #GAME LOOP################################################################################
    clock.tick(60)
    timer += 1
    
    
    #INPUT SECTION---------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moveRight = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moveRight = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shoot = False
    
    #physics section ------------------------------
    for i in range (len(armada)):
        timer = armada[i].move(timer)
        
    
    if shoot == True: #check keyboard input
        bullet.isAlive = True
        pygame.mixer.Sound.play(alienshoot)

        
    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos) #shoot from player position
        if bullet.isAlive == True:
            #check for collision between bullet and enemey
            for i in range (len(armada)): #check bullet with entire armada's positon
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos) #if we hit, set the bullet to false
                if bullet.isAlive == False:
                    break
                
            #shoot walls
            for i in range (len(walls)): #check bullet with entire walls's positon
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos) #if we hit, set the bullet to false
                if bullet.isAlive == False:
                    break
                
    else:#make bullet follow player when not moving up
        bullet.xpos = xpos + 28
        bullet.ypos = ypos
    
    #check for wall/missile collison
    for i in range (len(walls)):#check wall box
        for j in range (len(missiles)): #check each missile
            if missiles[j].isAlive == True:
                if walls[i].collide(missiles[j].xpos, missiles[j].ypos) == False: #call wall collision for each combo
                    missiles[j].isAlive = False #kill missile
                    break #stop killing walls if you are dead
                
                
    #2% chance every game loop that a missile will drop from a random alien
    randNum = random.randrange(100)
    if randNum < 2:
        print("missile drop") 
        pick = random.randrange(len(armada)) #pick a random alien from the armada
        if armada[pick].isAlive == True: #only drop from the live aliens
            for i in range (len(missiles)):#find the first llive missile to move
                if missiles[i].isAlive == False:#only fire missiles that aren't already goind
                    missiles[i].isAlive = True#set it to alive
                    missiles[i].xpos = armada[pick].xpos+5#set the missile position to the aliens posistion
                    missiles[i].ypos = armada[pick].ypos
                    break
             
    
        
    #check variables from the input section
    if moveLeft == True:
        vx =- 3 #if you switch the opperations like -= it accelerates
        
    elif moveRight == True:
        vx =+ 3
    else:
        vx = 0
        
    #check for collision between missiles and player
    for i in range (len(missiles)): # check for collision with each missile in the list
        if missiles[i].isAlive: #only get hit by live missiles
            if missiles[i].xpos > xpos: #check if missile is right of the left side of the player
                if missiles[i].xpos < xpos + 40: # check is the missile is left of the right side
                    if missiles[i].ypos < ypos + 40: #check if the missile is above the players bottom
                        if missiles[i].ypos > ypos: #check is the missile is below the top of the player
                            print("player hit!") #for testing
                            time.sleep(1)
                            pygame.mixer.Sound.play(DieSound)
                            xpos = vx
                            lives-=1
                            
            
    
    #update player position
    xpos += vx
    
    
    
    #call the move function
    
    for i in range (len(missiles)):
        missiles[i].move()
        
        
    
    #RENDER SECTION---------------------------------
    screen.fill((66, 58, 58))
    
    #player
    pygame.draw.rect(screen, (33, 207, 74), (xpos, ypos, 60, 20)) #draw character     # 400,750 as starting point
    pygame.draw.rect(screen, (33, 207, 74), (xpos+10, ypos-10, 40, 20)) #draw character
    pygame.draw.rect(screen, (33, 207, 74), (xpos+25, ypos-25, 10, 40)) #draw character
    
    #lives counter
    screen.blit(text_surface, (3,20))
    
    if lives == 3:
        pygame.draw.rect(screen, (33, 207, 74), (210, 20, 60, 20)) #draw character     # 400,750 as starting point
        pygame.draw.rect(screen, (33, 207, 74), (210+10, 20-10, 40, 20)) #draw character
        pygame.draw.rect(screen, (33, 207, 74), (210+25, 20-25, 10, 40)) #draw character
    if lives >= 2:
        pygame.draw.rect(screen, (33, 207, 74), (140, 20, 60, 20)) #draw character     # 400,750 as starting point
        pygame.draw.rect(screen, (33, 207, 74), (140+10, 20-10, 40, 20)) #draw character
        pygame.draw.rect(screen, (33, 207, 74), (140+25, 20-25, 10, 40)) #draw character
    if lives >= 1:
        pygame.draw.rect(screen, (33, 207, 74), (70, 20, 60, 20)) #draw character     # 400,750 as starting point
        pygame.draw.rect(screen, (33, 207, 74), (70+10, 20-10, 40, 20)) #draw character
        pygame.draw.rect(screen, (33, 207, 74), (70+25, 20-25, 10, 40)) #draw character
    
    #draw all aliens in the list
    for i in range (len(armada)):
        armada[i].draw()
        
    #draws bullet
    if bullet.isAlive == True:
        bullet.draw()
    
    #draws walls
    for i in range (len(walls)):
        walls[i].draw()
        
    #draws missiles
    for i in range (len(missiles)):
        if missiles[i].isAlive == True:
            missiles[i].draw()
            pygame.mixer.Sound.play(missileshoot)
    
    pygame.display.flip()
    
#end game loop################################################################################################
if lives == 0:
    print("GAME OVER")
pygame.quit()

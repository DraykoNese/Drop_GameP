import sys
import pygame
import random


#Click game part 2



################################
#LOAD
################################
pygame.init() #Starts the game

#scenes
# 0 = title, 1 = game, 2 = game over
scene = 0

#load images
circle = pygame.image.load("blue_body_circle.png")
square = pygame.image.load("blue_body_rhombus.png")
squircle = pygame.image.load("blue_body_squircle.png")

shapes = [circle, square, squircle]
# Set new size (width, height)
shape_size = (40, 40)  # adjust as needed

# Scale all shapes
circle = pygame.transform.scale(circle, shape_size)
square = pygame.transform.scale(square, shape_size)
squircle = pygame.transform.scale(squircle, shape_size)

# Flip circle after scaling
rCircle = pygame.transform.flip(circle, True, False)

#flipped circle (for aesthetics)
rCircle = pygame.transform.flip(circle, True, False) #slime, horizontal flip, vertical flip

#Set up screen
width = 800
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Don't Let The shapes Die!")
pygame.display.set_icon(circle)

#define colors
green = (74, 93, 35)
orange = (243, 121, 78)
black = (0, 0, 0)



#title and game over stuff
titleY = 100
titleFont = pygame.font.SysFont("Arial", 65)
circleTitle = titleFont.render("Circle Game", False, green, black)
gameOverTitle = titleFont.render("Circle Died :(", False, green, black)


playY = 300
btnMargin = 10
btnFont = pygame.font.SysFont("Arial", 30)
playWord = btnFont.render("Play", False, green)
quitWord = btnFont.render("Quit", False, green)
restartWord = btnFont.render("Restart", False, orange)

#rectangle = screen, color, (x, y, width, height, curve)
playBtn = pygame.draw.rect(screen, black, ((width/2)-(playWord.get_width()/2)- btnMargin, playY-btnMargin, playWord.get_width() + (btnMargin*2), playWord.get_height() + (btnMargin *2)), 0)
quitBtn = pygame.draw.rect(screen, black, ((width/4)-(quitWord.get_width()/2)- btnMargin, playY-btnMargin, quitWord.get_width() + (btnMargin*2), quitWord.get_height() + (btnMargin *2)), 0)
restartBtn = pygame.draw.rect(screen, green, ((width* .75)-(restartWord.get_width()/2)- btnMargin, playY-btnMargin, restartWord.get_width() + (btnMargin*2), restartWord.get_height() + (btnMargin *2)), 0)


# Dynamic background color system
background_color = (74, 93, 35)  # initial green
last_color_change_time = 0
color_change_interval = 5000  # change every 5 seconds (in milliseconds)

counter = 0
numOfThings = 7 #controls number of shapes that exist
circleImage = []
circleX = []
circleY = []
circleSpeed = []
baseSpeed = .1
speedMulti = 1.2

while counter < numOfThings:
        #add random circle to circle pool
        circleImage.append(random.choice(shapes))
        #ranomized x value between screen size
        circleX.append(random.randint(0, width - circle.get_width()))
        #randomized y value between screen size
        circleY.append(0 - random.randint(circle.get_height(), circle.get_height() * 2))
        #randomized speed
        circleSpeed.append((baseSpeed + random.random())/100)
        counter += 1 #counter = counter + 1
################################
#GAMELOOP
################################
gameOver = False
while gameOver == False:       
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:    
            gameOver = True
    ################################
    #MOUSE CLICKS
    ################################
    if pygame.mouse.get_pressed()[0]: #if left click
        coords = pygame.mouse.get_pos()
    
        if scene == 0: #if title screen
            if pygame.Rect.collidepoint(playBtn, coords):
                scene = 1
   
    
        elif scene == 1:
            counter = 0
            while counter < numOfThings:
            #box collision check
                if coords[0] >=circleX[counter] and coords[0] <= circleX[counter] + circle.get_width() and coords[1] >= circleY[counter] and coords[1] <= circleY[counter] + circle.get_height():
                    #Send it back to top with new identity
                    circleImage[counter] = random.choice(shapes)
                    circleX[counter] = random.randint(0, width - circle.get_width())
                    circleY[counter] = 0 - random.randint(circle.get_height(), circle.get_height() * 2)
                    #increase the speed
                    circleSpeed[counter] *= speedMulti
                counter +=1
        else: 
            if pygame.Rect.collidepoint(quitBtn, coords):
             gameOver = True
        
            if pygame.Rect.collidepoint(restartBtn, coords):
                counter = 0
                while counter < numOfThings:
                    circleImage[counter] = random.choice(shapes)
                    circleX[counter] = random.randint(0, width - circle.get_width())
                    circleY[counter] = 0  - random.randint(circle.get_height(), circle.get_height() * 2)
                    circleSpeed[counter] = (baseSpeed + random.random())/ 100
                    counter += 1
                scene = 0

    ################################
    #UPDATE
    ################################
    if scene == 1: #gameplay scene
        counter = 0
        while counter < numOfThings:
            #check if hit botom of screen
            if circleY[counter] + circle.get_height() > height:
                #gameover
                scene = 2
            circleY[counter] += circleSpeed[counter]
            counter +=1 
        current_time = pygame.time.get_ticks()

        # Check if it's time to change the background color
        if current_time - last_color_change_time > color_change_interval:
        # Pick a new random background color
            background_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            last_color_change_time = current_time
    ################################
    #DRAW
    ################################

    if scene == 0:
        screen.fill(orange)
        #centered title
        screen.blit(circleTitle, ((width/2)-(circleTitle.get_width()/2), titleY))
        #circle left
        screen.blit(circle, ((width/2)-(circleTitle.get_width()/2)-circle.get_width(), titleY + (circleTitle.get_height()-circle.get_height())))
        screen.blit(rCircle, ((width/2) + (circleTitle.get_width()/2), titleY + (circleTitle.get_height()-circle.get_height())))
        #button
        coords = pygame.mouse.get_pos() 
        if pygame.Rect.collidepoint(playBtn, coords): #green button
            playBtn = pygame.draw.rect(screen, green, ((width/2)-(playWord.get_width()/2)- btnMargin, playY-btnMargin, playWord.get_width() + (btnMargin*2), playWord.get_height() + (btnMargin *2)), 0)    
        else: #normal button
            playBtn = pygame.draw.rect(screen, black, ((width/2)-(playWord.get_width()/2)- btnMargin, playY-btnMargin, playWord.get_width() + (btnMargin*2), playWord.get_height() + (btnMargin *2)), 0)
            screen.blit(playWord, ((width/2)-(playWord.get_width()/2), playY))
    elif scene == 1: #gameplay
        screen.fill(background_color)
        #draw circles
        counter = 0
        while counter < numOfThings:
            screen.blit(circleImage[counter], (circleX[counter], circleY[counter]))
            counter += 1

    else: #gameover
        screen.fill(black)
        #text
        screen.blit(gameOverTitle, (width/2 - gameOverTitle.get_width()/2, titleY))
        screen.blit(circle, ((width/2)-(gameOverTitle.get_width()/2)-circle.get_width(), titleY + (gameOverTitle.get_height()-circle.get_height())))
        screen.blit(rCircle, ((width/2 + gameOverTitle.get_width() / 2), titleY + (gameOverTitle.get_height()-circle.get_height())))
    
        #buttons
        #quit
        coords = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(quitBtn, coords):
            #if mouse hovers over quit button it'll be green
            quitBtn = pygame.draw.rect(screen, green, ((width/4)-(quitWord.get_width()/2)- btnMargin, playY-btnMargin, quitWord.get_width() + (btnMargin*2), quitWord.get_height() + (btnMargin *2)), 0)    
        else:
            quitBtn = pygame.draw.rect(screen, green, ((width/4)-(quitWord.get_width()/2)- btnMargin, playY-btnMargin, quitWord.get_width() + (btnMargin*2), quitWord.get_height() + (btnMargin *2)), 0)    
            screen.blit(quitWord, ((width/4) - (quitWord.get_width()/2), playY))

        if pygame.Rect.collidepoint(restartBtn, coords): 
            restartBtn = pygame.draw.rect(screen, green, ((width* .75)-(restartWord.get_width()/2)- btnMargin, playY-btnMargin, restartWord.get_width() + (btnMargin*2), restartWord.get_height() + (btnMargin *2)), 0)
        else:
            restartBtn = pygame.draw.rect(screen, green, ((width* .75)-(restartWord.get_width()/2)- btnMargin, playY-btnMargin, restartWord.get_width() + (btnMargin*2), restartWord.get_height() + (btnMargin *2)), 0)
            screen.blit(restartWord,((width *.75) - (restartWord.get_width()/2), playY))
        
    pygame.display.flip()
    ################################
    #QUIT
    ################################
pygame.display.quit()
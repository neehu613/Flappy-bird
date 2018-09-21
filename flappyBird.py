import pygame
import time
import random

#color definitions
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,215,0)

#global game variables
winW = 800
winH = 600

pygame.init()
gameDisplay = pygame.display.set_mode((winW, winH))
pygame.display.set_caption("Flappy Birds")
clock = pygame.time.Clock()
FPS = 30
smallfont = pygame.font.SysFont(None, 30)
mediumfont = pygame.font.SysFont(None, 50)
largefont = pygame.font.SysFont(None, 80)


#image loading
bg = pygame.image.load("images/bg.jpeg")
bg = pygame.transform.scale(bg, (800, 600))

birdy1 = pygame.image.load("images/redbird.png")
birdy1 = pygame.transform.scale(birdy1, (50, 50))
birdy2 = pygame.image.load("images/yellowbird.png")
birdy2 = pygame.transform.scale(birdy2, (50, 50))
birdy3 = pygame.image.load("images/bluebird.png")
birdy3 = pygame.transform.scale(birdy3, (50, 50))

gameover = pygame.image.load('images/gameOver.jpg')
gameover = pygame.transform.scale(gameover, (600, 300))

pipeDown = pygame.image.load("images/pipeDown.jpeg")
pipeUp = pygame.image.load("images/pipeUp.jpeg")

#audio files
hit = pygame.mixer.Sound('sound/hit.wav')
point = pygame.mixer.Sound('sound/point.wav')
flap = pygame.mixer.Sound('sound/flap.wav')
die = pygame.mixer.Sound('sound/die.wav')

def gameQuit():
	pygame.quit()
	quit()

def printMessage(msg, color, font, yLoc=0):
	textSurface = font.render(msg, True, color)
	textRect = textSurface.get_rect()
	textRect.center = (winW/2), (winH/2)+yLoc
	gameDisplay.blit(textSurface, textRect)


def dispScore(score, level, prevHigh):
	spaces = str(10 * " ")
	pygame.draw.rect(gameDisplay, yellow, [0,0,500, 50])
	text = smallfont.render("Score -  "+ str(score), True, blue)
	gameDisplay.blit(text, [20, 15])
	text = smallfont.render("Level -  "+ str(level), True, blue)
	gameDisplay.blit(text, [150, 15])
	text = smallfont.render("Prev HighScore -  "+ str(prevHigh), True, blue)
	gameDisplay.blit(text, [270, 15])
	pygame.display.update()


def instructions():
	instructionPage = True	
	gameDisplay.fill(yellow)
	gameDisplay.blit(birdy1, (winW/8,winH/5))
	gameDisplay.blit(birdy3, (winW/4,winH/5))
	gameDisplay.blit(birdy2, (winW/2,winH/5))
	gameDisplay.blit(birdy3, (winW-winW/4,winH/5))
	gameDisplay.blit(birdy1, (winW-winW/8,winH/5))
	while instructionPage == True:
		msg = "Flap your way through the pipes"
		msg1 = "Controls are as follows"
		msg2 = "UP ARROW to flap"
		msg4 = "Press P to play and q to Quit"
		msg5 = "While playing, press P to pause"
		printMessage(msg, blue, mediumfont, -50)
		printMessage(msg1, black, smallfont)
		printMessage(msg2, black, smallfont, 30)
		printMessage(msg4, red, smallfont, 150)
		printMessage(msg5, red, smallfont, 180)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameQuit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					instructionPage = False
				elif event.key == pygame.K_q:
					gameQuit()
		
		clock.tick(10)
		pygame.display.update()


def gameIntro():
	intro = True
	introScreen = pygame.image.load('images/Flappy_Logo.png')
	introScreen = pygame.transform.scale(introScreen, (int(winW/2), int(winH/4)))
	while intro:
		gameDisplay.fill(yellow)
		gameDisplay.blit(introScreen, (winW/4, winH/3))

		msg1 = "Press I to view the instructions to play and q to Quit"
		printMessage(msg1, red, smallfont, +100)
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameQuit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_i:
					instructions()
					intro = False
				elif event.key == pygame.K_q:
					gameQuit()
		
		clock.tick(10)
		pygame.display.update()

def gamePaused():
	#pygame.mixer.music.pause()
	gameDisplay.fill(yellow)
	printMessage("Game Paused", red, largefont, -20)
	printMessage("Press P to continue playing and Q to quit", black, smallfont, 70)
	pygame.display.update()
	
	paused = True

	while paused == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameQuit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					#pygame.mixer.music.unpause()
					paused = False
				if event.key == pygame.K_q:
					gameQuit()

	clock.tick(10)

'''
def popUpLevel(level):
	msg = "Level = " + str(level)
	printMessage(msg, blue, largefont)
	pygame.display.update()
	clock.tick(20)
	time.sleep(1)
	gameDisplay.fill(white)
	pygame.display.update()
'''

def gameLoop():
	#variable declarations
	gameOver = gameExit = False
	birdW = 50
	birdH = 50
	birdX = winW/4
	birdY = winH/2
	y_change = 0
	y_disp = 20
	score = 0
	level = 1
	speed = 0
	i = j = 1

	global pipeUp
	global pipeDown

	pipeGap = 150
	pipeWidth = 100

	pipeDownHeight = random.randrange(100, 400)
	pipeUpHeight = winH - pipeGap - pipeDownHeight

	pipeX = winW + 500
	
	pipeDownY = 0
	pipeUpY = pipeDownHeight + pipeGap

	bgX = 0
	bgY = 0
	bgX1 = winW
	bgY1 = 0
	bgX_change = 10

	pipeDown = pygame.transform.scale(pipeDown, (pipeWidth, pipeDownHeight))
	pipeUp = pygame.transform.scale(pipeUp, (pipeWidth, pipeUpHeight))

	f = open("highScore.txt")
	prevHigh = int(f.read())
	f.close()
	
	randBird = random.randrange(1,4)	

	while not gameExit:
		#game over event handling
		while gameOver == True:
			gameDisplay.fill(yellow)
			gameDisplay.blit(gameover, (winW/8, winH/4))
			#printMessage("Flappy's dead", red, largefont)
			printMessage("Press P to play and q to Quit", black, smallfont, 200)

			with open("highScore.txt") as f:
				highScore = int(f.read())
				if score > highScore:
					highScore = score
			with open("highScore.txt", "w") as f:
				f.write(str(highScore))
			
			printMessage("High Score: "+ str(highScore), black, smallfont, 250)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameQuit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						f = open("highScore.txt")
						prevHigh = int(f.read())
						f.close()
						gameOver = False
					elif event.key == pygame.K_q:
						gameQuit()
			birdY = winH/4
			y_change = 0
			pipeX = winW+500
			score = 0
			level = 1
			randBird = random.randrange(1,4)
			clock.tick(10)
			pygame.display.update()
		
		y_change += 1

		#event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameQuit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					pygame.mixer.Sound.play(flap)
					y_change -= y_disp
				elif event.key == pygame.K_p:
					gamePaused()

			
		birdY += y_change
		bgX1 -= bgX_change
		bgX -= bgX_change
		pipeX -= 10 + speed

		#game rendering
		gameDisplay.fill(white)
		gameDisplay.blit(bg, (bgX,bgY))
		gameDisplay.blit(bg, (bgX1, bgY1))
		

		if randBird == 1:
			gameDisplay.blit(birdy1, (birdX,birdY))
		elif randBird == 2:
			gameDisplay.blit(birdy2, (birdX,birdY))
		elif randBird == 3:
			gameDisplay.blit(birdy3, (birdX,birdY))

		pipeDown = pygame.transform.scale(pipeDown, (pipeWidth, pipeDownHeight))
		pipeUp = pygame.transform.scale(pipeUp, (pipeWidth, pipeUpHeight))
		gameDisplay.blit(pipeUp, (pipeX, pipeUpY))
		gameDisplay.blit(pipeDown, (pipeX, pipeDownY))

		dispScore(score, level, prevHigh)
		pygame.display.update()
		clock.tick(FPS)
		
		#gameLogic

		if birdY+birdH >= winH:
			pygame.mixer.Sound.play(hit)
			gameOver = True

		if pipeX < 0:
			pipeDownHeight = random.randrange(100, 400)
			pipeUpHeight = winH - pipeGap - pipeDownHeight
			pipeDownY = 0
			pipeUpY = pipeDownHeight + pipeGap
			pipeX = winW
		
		if birdX+birdW >= pipeX and birdX<= pipeX+pipeWidth:
			if birdY < pipeDownHeight or birdY+birdH > pipeUpY:
				pygame.mixer.Sound.play(hit)
				gameOver = True

		if bgX+winW <= 0:
				bgX = winW
		if bgX1+winW <= 0:
				bgX1 = winW

		if birdX+birdW > pipeX:
			score += 1
			if birdX+birdW > pipeX+pipeWidth:
				score -= 1
		
		if score >= 10*j:
			pygame.mixer.Sound.play(point)
			j+=1

		if score >= 100*i:
			i+=1
			level+=1
			speed +=10

#function calls
gameIntro()
gameLoop()
gameQuit()
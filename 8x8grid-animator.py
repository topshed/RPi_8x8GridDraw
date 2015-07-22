# bookmarks http://www.one-tab.com/page/Ds6dSsBoSX24cD8OSxqKcA
import pygame
import sys
import math
from pygame.locals import *
from led import LED
from buttons import Button
import png # pypng
from astro_pi import AstroPi
import copy, time


pygame.init()
pygame.font.init()

ap=AstroPi()
#screen = pygame.display.set_mode((440, 500), 0, 32)
screen = pygame.display.set_mode((500, 500), 0, 32)
pygame.display.set_caption('Astro Pi Grid editor')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 51, 25))
colour = (255,0,0)
rotation = 0
frame_number  = 1
fps = 4



def setColourRed():
	global colour 
	colour = (255,0,0)

def setColourBlue():
	global colour 
	colour = (0,0,255)

def setColourGreen():
	global colour 
	colour = (0,255,0)

def setColourPurple():
	global colour 
	colour = (102,0,204)

def setColourPink():
	global colour 
	colour = (255,0,255)

def setColourYellow():
	global colour 
	colour = (255,255,0)

def setColourOrange():
	global colour 
	colour = (255,128,0)

def setColourWhite():
	global colour 
	colour = (255,255,255)

def clearGrid():
	
	# Clears the pygame LED grid and sets all the leds.lit back to False
	
	for led in leds:
		led.lit = False

def buildGrid():

	e = [0,0,0]
	e_png = (0,0,0)

	grid = [
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e,
	e,e,e,e,e,e,e,e
	]
	png_grid =[]

	png_grid = ['blank','blank','blank','blank','blank','blank','blank','blank']
	for led in leds:
		if led.lit:
			val = led.pos[0] + (8 * led.pos[1])
			#print val
			grid[val] = [led.color[0], led.color[1], led.color[2]]
			if png_grid[led.pos[0]] == 'blank':
				png_grid[led.pos[0]] = (led.color[0], led.color[1], led.color[2])
			else:
				png_grid[led.pos[0]] = png_grid[led.pos[0]] + (led.color[0], led.color[1], led.color[2])
		else: 
			if png_grid[led.pos[0]] == 'blank':
				png_grid[led.pos[0]] = (0,0,0)
			else:
				png_grid[led.pos[0]] = png_grid[led.pos[0]] + (0,0,0)
	return (grid, png_grid)

def piLoad():
	grid, grid_png = buildGrid()
	ap.set_pixels(grid)

def exportGrid():

	grid, png_grid = buildGrid()
	
	#print png_grid

	FILE=open('image8x8.png','wb')
	w = png.Writer(8,8)
	w.write(FILE,png_grid)
	FILE.close()

def exportCons():

	grid, png_grid = buildGrid()
	print grid

def clearGrid():
	
	# Clears the pygame  grid and sets all the leds.lit back to False
	
	for led in leds:
		led.lit = False

def rotate():
	global rotation
	if rotation == 270:
		rotation = 0
	else:
		rotation = rotation + 90
	ap.set_rotation(rotation)



def handleClick():
   
	pos = pygame.mouse.get_pos()
	led = findLED(pos, leds)
	if led:
		#print 'led ' + str(led) + ' clicked'
		led.clicked(colour)
	for butt in buttons:
		if butt.rect.collidepoint(pos):
			butt.click()
			#print 'button clicked'

 
def findLED(clicked_pos, leds):
	
	# reads leds and checks if clicked position is in one of them
	
	x = clicked_pos[0]
	y = clicked_pos[1]
	for led in leds:
		if math.hypot(led.pos_x - x, led.pos_y - y) <= led.radius:
			return led
			#print 'hit led'
	return None


def drawEverything():
	
	screen.blit(background, (0, 0))
	#draw the leds
	for led in leds:
		led.draw()
	for button in buttons:
		button.draw(screen)
	font = pygame.font.Font(None,16)
	
	frame_text = 'Frame ' + str(frame_number) 
	text = font.render(frame_text,1,(255,255,255))
	screen.blit(text, (445,335))
	fps_text = 'FPS ' + str(fps) 
	text = font.render(fps_text,1,(255,255,255))
	screen.blit(text, (445,380))
	font = pygame.font.Font(None,18)
	export_text = 'Export'
	text = font.render(export_text,1,(255,255,255))
	screen.blit(text, (35,440))
	pygame.draw.circle(screen,colour,(470,310),20,0)
	#flip the screen
	pygame.display.flip()


def nextFrame():
	
	global frame_number
	global leds
	print frame_number
	animation[frame_number] = copy.deepcopy(leds)
	#clearGrid()
	frame_number+=1
	if frame_number in animation:
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
		#leds = animation[frame_number]
		for saved_led in animation[frame_number]:
			if saved_led.lit:
				for led in leds:
					if led.pos == saved_led.pos:
						led.color = saved_led.color
						led.lit = True
			
	

def prevFrame():

	global frame_number
	global leds
	print frame_number
	animation[frame_number] = copy.deepcopy(leds)
	clearGrid()
	if frame_number != 1:
		frame_number-=1
	if frame_number in animation:
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
		#leds = animation[frame_number]
		for saved_led in animation[frame_number]:
			if saved_led.lit:
				for led in leds:
					if led.pos == saved_led.pos:
						led.color = saved_led.color
						led.lit = True
			

def getLitLEDs():

	points = []
	for led in leds:
		if led.lit:
			points.append(led.pos)
	return points

# Main program body - set up leds and buttons

leds = []
for x in range(0, 8):
	for y in range(0, 8):
		led = LED(pos=(x, y))
		leds.append(led)
buttons = []
animation={}
#global frame_number

def play():
	
	global leds
	global frame_number
	#print 'length of ani is ' + str(len(animation))
	for playframe in range(1,(len(animation)+1)):
		print playframe 
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
			#leds = animation[frame_number]
			for saved_led in animation[playframe]:
				if saved_led.lit:
					for led in leds:
						if led.pos == saved_led.pos:
							led.color = saved_led.color
							led.lit = True
		piLoad()
		time.sleep(1.0/fps)
		
def faster():
	global fps
	fps+=1

def slower():
	global fps
	if fps != 1:
		fps-=1

def exportAni():

	FILE=open('animation8x8.py','wb')
	FILE.write('from astro_pi import AstroPi\n')
	FILE.write('import time\n')
	FILE.write('ap=AstroPi()\n')
	FILE.write('FRAMES = [\n')
	global leds
	global frame_number
	#print 'length of ani is ' + str(len(animation))
	for playframe in range(1,(len(animation)+1)):
		print playframe 
		leds =[]
		for x in range(0, 8):
			for y in range(0, 8):
				led = LED(pos=(x, y))
				leds.append(led)
			#leds = animation[frame_number]
			for saved_led in animation[playframe]:
				if saved_led.lit:
					for led in leds:
						if led.pos == saved_led.pos:
							led.color = saved_led.color
							led.lit = True
		grid, png_grid = buildGrid()
		
		FILE.write(str(grid))
		FILE.write(',\n')
	FILE.write(']\n')
	FILE.write('for x in FRAMES:\n')
	FILE.write('\t ap.set_pixels(x)\n')
	FILE.write('\t time.sleep('+ str(1.0/fps) + ')\n')
	FILE.close()



exportAniButton = Button('py', action=exportAni, size=(45,25), pos=(10, 460), color=(153,0,0))
buttons.append(exportAniButton)
exportPngButton = Button('png', action=exportGrid, size=(45,25), pos=(62, 460), color=(153,0,0))
buttons.append(exportPngButton)
clearButton = Button('Clear', action=clearGrid, size=(50,25), pos=(330, 450), color=(204,255,255))
buttons.append(clearButton)
LoadButton = Button('Load to LEDs', action=piLoad, pos=(115, 450), color=(153,0,0))
buttons.append(LoadButton)
exportConsButton = Button('Export to console', action=exportCons, pos=(220, 450), color=(153,0,0))
buttons.append(exportConsButton)

PlayButton = Button('Play', action=play, size=(50,25), pos=(445, 430), color=(184,138,0))
buttons.append(PlayButton)

PrevFrameButton = Button('<-', action=prevFrame, size=(24,25), pos=(445, 350), color=(184,138,0))
buttons.append(PrevFrameButton)
NextFrameButton = Button('->', action=nextFrame, size=(24,25), pos=(472, 350), color=(184,138,0))
buttons.append(NextFrameButton)

FasterButton = Button('+', action=faster, size=(24,25), pos=(445, 395), color=(184,138,0))
buttons.append(FasterButton)
SlowerButton = Button('-', action=slower, size=(24,25), pos=(472, 395), color=(184,138,0))
buttons.append(SlowerButton)

RotateButton = Button('Rotate', action=rotate, size=(50,25), pos=(385, 450), color=(205,255,255))
buttons.append(RotateButton)

RedButton = Button('Red', action=setColourRed, size=(50,30), pos=(445, 10),hilight=(0, 200, 200),color=(255,0,0))
buttons.append(RedButton)
BlueButton = Button('Blue', action=setColourBlue, size=(50,30), pos=(445, 45),hilight=(0, 200, 200),color=(0,0,255))
buttons.append(BlueButton)
GreenButton = Button('Green', action=setColourGreen, size=(50,30), pos=(445, 80),hilight=(0, 200, 200),color=(0,255,0))
buttons.append(GreenButton)
PurpleButton = Button('Purple', action=setColourPurple, size=(50,30), pos=(445, 115),hilight=(0, 200, 200),color=(102,0,204))
buttons.append(PurpleButton)
PinkButton = Button('Pink', action=setColourPink, size=(50,30), pos=(445, 150),hilight=(0, 200, 200),color=(255,0,255))
buttons.append(PinkButton)
OrangeButton = Button('Orange', action=setColourOrange, size=(50,30), pos=(445, 185),hilight=(0, 200, 200),color=(255,128,0))
buttons.append(OrangeButton)
YellowButton = Button('yellow', action=setColourYellow, size=(50,30), pos=(445, 220),hilight=(0, 200, 200),color=(255,255,0))
buttons.append(YellowButton)
WhiteButton = Button('white', action=setColourWhite, size=(50,30), pos=(445, 255),hilight=(0, 200, 200),color=(255,255,255))
buttons.append(WhiteButton)



# Main prog loop


while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			clearGrid()
			pygame.quit()
			sys.exit()
		
		if event.type == MOUSEBUTTONDOWN:
			handleClick()

	#update the display
	drawEverything()


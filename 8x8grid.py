# bookmarks http://www.one-tab.com/page/Ds6dSsBoSX24cD8OSxqKcA
import pygame
import sys
import math
from pygame.locals import *
from led import LED
from buttons import Button
import png # pypng
from astro_pi import AstroPi


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


def clearGrid():
    
    # Clears the pygame  grid and sets all the leds.lit back to False
    
    for led in leds:
        led.lit = False

def drawEverything():
    
    screen.blit(background, (0, 0))
    #draw the leds
    for led in leds:
        led.draw()
    for button in buttons:
        button.draw(screen)

    pygame.draw.circle(screen,colour,(470,460),20,0)
    #flip the screen
    pygame.display.flip()

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

exportFileButton = Button('Export to file', action=exportGrid, pos=(10, 450), color=(153,0,0))
buttons.append(exportFileButton)
clearButton = Button('Clear grid', action=clearGrid, pos=(325, 450), color=(153,0,0))
buttons.append(clearButton)
LoadButton = Button('Load to LEDs', action=piLoad, pos=(115, 450), color=(153,0,0))
buttons.append(LoadButton)
exportConsButton = Button('Export to console', action=exportCons, pos=(220, 450), color=(153,0,0))
buttons.append(exportConsButton)

RotateButton = Button('Rotate', action=rotate, size=(50,25), pos=(445, 355), color=(153,0,0))
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


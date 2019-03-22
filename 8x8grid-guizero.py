# Write your code here :-)
from guizero import App, PushButton, Slider, Waffle, Box,Text, Combo,CheckBox, yesno, info, error, MenuBar, warn
import os
from time import sleep
import ast
from tkinter import filedialog
from pathlib import Path

HOME = str(Path.home())

import os, sys

NOHAT = False
ONEMU = False

def no_hat_check():
    global NOHAT
    global ONEMU
    NOHAT = yesno("No SenseHAT detected", "No SenseHat detected - Do you want to carry on anyway?")
    if NOHAT:
        if "arm" in  os.uname().machine: 
            ONEMU = yesno("Looks like a Pi","Do you want to try to run in the SenseHat emulator?")      
                
    else:
        sys.exit()

col = (255,255,255)
blank_frame = [(0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0),
                (0,0,0), (0,0,0), (0,0,0), (0,0,0),(0,0,0), (0,0,0),(0,0,0), (0,0,0)]
                
frames = {1:blank_frame.copy()}
current_frame_number =1
framerate =  1 # frames per second
looping = False

def illum_pixel(x,y):
    global col
    global NOHAT
    matrix.set_pixel(x,y,col)
    if not NOHAT:
        sh.set_pixel(x,y,col)
    
    
def col_select(x,y):
    global col
    if y == 0:
        col = (255,0,0)
        button_clear.text_color = "black"
    elif y == 1:
        col = (0,255,0)
        button_clear.text_color = "black"
    elif y == 2:
        col = (0,0,255)
        button_clear.text_color = "white"
    elif y == 3:
        col = (255,255,0)
        button_clear.text_color = "black"
    elif y == 4:
        col = (80,80,80)
        button_clear.text_color = "white"
    elif y == 5:
        col = (255,255,255)
        button_clear.text_color = "black"
    elif y == 6:
        col = (255,0,255)
        button_clear.text_color = "black"
    elif y == 7:
        col = (255,150,0)
        button_clear.text_color = "black"
        button_clear.text_color = "black"
    elif y == 8:
        col = (0,0,0)
        button_clear.text_color = "white"
    elif y == 9:
        col = (66,220,240)
        button_clear.text_color = "black"
    box.bg =col
    button_clear.bg = col

def hex_to_rgb(hex):
    return(tuple(int(hex[i:i+2],16) for i in (0,2,4)))

def p_clicked(x,y):
    if (x <= 7) and (y <= 7):
        
        if matrix.get_pixel(x,y) == "black":
            illum_pixel(x,y)
            frames[current_frame_number][(y*8)+x] = col
        elif hex_to_rgb(str(matrix.get_pixel(x,y).strip('#'))) == col:
            matrix.set_pixel(x,y,"black")
            sh.set_pixel(x,y,(0,0,0))
            frames[current_frame_number][(y*8)+x] = (0,0,0)        
        else:
            illum_pixel(x,y)
            frames[current_frame_number][(y*8)+x] = col 

    
def clear_matrix():
    global NOHAT
    if not NOHAT:
        sh.clear(col)
    for x in range(8):
        for y in range(8):
            matrix.set_pixel(x,y,col)
            frames[current_frame_number][(y*8)+x] = col
           

def new_frame():
    global current_frame_number
    global frames
    global blank_frame
    if current_frame_number != len(frames): # not last frame
        for f in range(len(frames), current_frame_number, -1):
            frames[f+1] = frames[f].copy()
    frames[current_frame_number+1] = blank_frame.copy()
    current_frame_number +=1  

    load_frame()

def copy_frame():
    global current_frame_number
    global frames
    if current_frame_number != len(frames): # not last frame
        for f in range(len(frames), current_frame_number, -1):
            frames[f+1] = frames[f].copy()
    frames[current_frame_number+1] = frames[current_frame_number].copy()
    current_frame_number +=1  

    load_frame()
    
def delete_frame():
    global current_frame_number
    global frames
    global blank_frame
    if current_frame_number != 1:
        if current_frame_number != len(frames): # not last frame
            for f in range(current_frame_number, len(frames)):
                frames[f] = frames[f+1].copy()
        current_frame_number-=1
        del frames[len(frames)]
     
        load_frame()
    else:
        warn("Heads up", "Only one frame exits - you can't delete it")
        
    
def load_frame():
    global NOHAT
    frame_status_text.value=("Frame " + str(current_frame_number).zfill(3) + " of " + str(len(frames)).zfill(3))
    if not NOHAT:
        sh.set_pixels(frames[current_frame_number])
    for x in range(8):
        for y in range(8):
            matrix.set_pixel(x,y,frames[current_frame_number][(y*8)+x])
    load_other_frames()
            
def load_other_frames():
    prev_matrix.color="black"
    next_matrix.color="black"
    if len(frames) == 2:
        if current_frame_number == 1:
            for x in range(8):
                for y in range(8):
                    next_matrix.set_pixel(x,y,frames[current_frame_number+1][(y*8)+x])
            for x in range(8):
                for y in range(8):
                    prev_matrix.set_pixel(x,y,"grey")                  
        else:
            for x in range(8):
                for y in range(8):
                    prev_matrix.set_pixel(x,y,frames[current_frame_number-1][(y*8)+x])
            for x in range(8):
                for y in range(8):
                    next_matrix.set_pixel(x,y,"grey")   
                
    if len(frames) >= 3:
        if current_frame_number == 1:
            for x in range(8):
                for y in range(8):
                    next_matrix.set_pixel(x,y,frames[current_frame_number+1][(y*8)+x])
            for x in range(8):
                for y in range(8):
                    prev_matrix.set_pixel(x,y,"grey")                  
        elif current_frame_number == len(frames):
            for x in range(8):
                for y in range(8):
                    prev_matrix.set_pixel(x,y,frames[current_frame_number-1][(y*8)+x])
            for x in range(8):
                for y in range(8):
                    next_matrix.set_pixel(x,y,"grey")
        else:
            for x in range(8):
                for y in range(8):
                    next_matrix.set_pixel(x,y,frames[current_frame_number+1][(y*8)+x])
            for x in range(8):
                for y in range(8):
                    prev_matrix.set_pixel(x,y,frames[current_frame_number-1][(y*8)+x])                 


        
def left():
    global current_frame_number
    if current_frame_number > 1:
        current_frame_number -=1
        load_frame()
    
def right():
    global current_frame_number
    if current_frame_number < len(frames):
        current_frame_number +=1
        load_frame()

def right_play():
    global current_frame_number
    global stopped
    global looping
    if (current_frame_number < len(frames)) and not stopped:
        current_frame_number +=1
        load_frame()
    if (current_frame_number == len(frames)) and not stopped:

        button_play.enable()
        button_stop.disable()
        slider_framerate.enable()
        button_go_end.enable()
        button_go_start.enable()
        button_left.enable()
        button_right.enable()
        if checkbox_repeat.value == 1:
            looping = True
            current_frame_number = 0
            play()
        else:
            stopped = True
            
        
def go_end():
    global current_frame_number
    global frames
    current_frame_number = len(frames)
    load_frame()
    
def go_start():
    global current_frame_number
    current_frame_number =1
    load_frame()
    

def play():
    global stopped
    global current_frame_number
    global looping
    if len(frames) > 1:
        button_play.disable()
        button_stop.enable()
        button_go_end.disable()
        button_go_start.disable()
        button_go_end.disable()
        button_left.disable()
        button_right.disable()
        slider_framerate.disable()
        stopped = False
        t =  int(1000/framerate)
        if looping:
            for i in range(1,len(frames)+1): # because we set current_frame_number = 0 when looping we need an extra iteration
                    frame_status_text.after(t*i,right_play)
        else:  
            for i in range(1,len(frames)):
                    frame_status_text.after(t*i,right_play)

        
def stop():
    global stopped
    stopped = True
    button_play.enable()
    button_stop.disable()
    slider_framerate.enable()
    button_go_end.enable()
    button_go_start.enable()
    button_left.enable()
    button_right.enable()


def export_as_python():
    global framerate
    filename = filedialog.asksaveasfilename(initialdir = HOME, 
                                        title = "Export file", 
                                        filetypes = (("python files","*.py"),("all files","*.*")))
    if len(filename) != 0:
        with open(filename,"w") as export_file:
            export_file.write("# 8x8Grid Editor output file \n")
            export_file.write("from sense_hat import SenseHat\n")
            export_file.write("from time import sleep\n")
            export_file.write("sh = SenseHat()\n")
            export_file.write("sh.clear(0,0,0)\n")
            for e in range(1,len(frames)+1):
                export_file.write("sh.set_pixels(" +str(frames[e]) + ")\n")
                export_file.write("sleep(1/"+str(framerate) +")\n")
            

            
def import_python():
    global framerate
    global current_frame_number
    current_frame_number = 1
    filename = filedialog.askopenfilename(initialdir = HOME, 
                                        title = "Select file", 
                                        filetypes = (("python files","*.py"),("all files","*.*")))                                    
    if len(filename) != 0:
        with open(filename,"r") as import_file:
            line1 = import_file.readline()
            if line1 == "# 8x8Grid Editor output file \n":
                #print("This looks like an 8x8 Grid Editor file")
                try:
                    for line in import_file:
                        if line.startswith("sh.set_pixels"):
                            grid = line[14:-2]
                            frames[current_frame_number] = ast.literal_eval(grid)
                            current_frame_number+=1
                    current_frame_number-=1
                    load_frame()
                except:
                    error("Import failed", "Sorry, that file could not be imported")
            else:
                not_our_file = yesno("Uh-oh","This doesn't look like an 8x8 Grid Editor file. Carry on trying to import it?")
                if not_our_file == True:
                    try:
                        for line in import_file:
                            if line.startswith("sh.set_pixels"):
                                grid = line[14:-2]
                                frames[current_frame_number] = ast.literal_eval(grid)
                                current_frame_number+=1
                        current_frame_number-=1
                        load_frame()
                    except:
                        error("Import failed", "Sorry, that file could not be imported")
                    
            
def set_framerate():
    global framerate
    framerate = slider_framerate.value
    
def sh_rotation():
    sh.set_rotation(int(combo_rotation.value))

app = App(title="8x8 Grid Editor",layout="grid",height=540, width=500)
box_top = Box(app, layout="grid", grid=[0,0,5,1])
button_go_start = PushButton(box_top, command=go_start,grid=[0,0,2,1], text = "<<", image=HOME+"/RPi_8x8GridDraw/images/endl.png")
button_left = PushButton(box_top, command=left,grid=[2,0,2,1], text = "<",image=HOME+"/RPi_8x8GridDraw/images/left.png")
button_play = PushButton(box_top, command=play,grid=[4,0,2,1], text = "PLAY", image=HOME+"/RPi_8x8GridDraw/images/play.png")
button_stop = PushButton(box_top, command=stop,grid=[6,0,2,1], text = "STOP",enabled=False, image=HOME+"/RPi_8x8GridDraw/images/stop.png")
button_right = PushButton(box_top, command=right,grid=[8,0,2,1], text = ">",image=HOME+"/RPi_8x8GridDraw/images/right.png")
button_go_end = PushButton(box_top, command=go_end,grid=[10,0,2,1], text = ">>",image=HOME+"/RPi_8x8GridDraw/images/endr.png")
checkbox_repeat = CheckBox(app, text=" Repeat",grid=[6,0,1,1])
box_framerate = Box(app, layout="grid", grid=[7,0,2,1])
box_framerate.set_border(0,"#ff0000")
slider_framerate = Slider(box_framerate, command=set_framerate, grid=[0,0],start=1, end=25)
text_slider = Text(box_framerate, text="Framerate (fps)", grid = [0,1], size=10)


matrix = Waffle(app,height=8,width=8,dim=30,command=p_clicked,color="black",grid=[0,1,7,7])
palette = Waffle(app,height=10, width=1, dim =20, command = col_select,grid=[7,1,1,7])
palette.set_pixel(0, 0, "red")
palette.set_pixel(0,1, (0,255,0))
palette.set_pixel(0,2, "blue")
palette.set_pixel(0,3, "yellow")
palette.set_pixel(0,4, (100,100,100))
palette.set_pixel(0,5, "white")
palette.set_pixel(0,6, (255,0,255))
palette.set_pixel(0,7, "orange")
palette.set_pixel(0,8, "black")
palette.set_pixel(0,9, (66,220,240))
box = Box(app, width=30,height=30,grid=[2,10,2,1])
box.bg =col
text_current_col = Text(app, text="Selected Colour:", grid=[0,10,3,1])
text_rotation = Text(app, text="LED Rotation:", grid=[5,10,3,1])
combo_rotation = Combo(app, options=["0", "90", "180", "270"],grid=[8,10,2,1],command=sh_rotation)


button_clear = PushButton(app, command=clear_matrix,grid=[8,1], text = "Clear")
button_clear.bg = col


frame_status_text = Text(app, text="Frame " + str(current_frame_number).zfill(3) + " of " + str(len(frames)).zfill(3), grid=[0,11,3,1])
button_new_frame = PushButton(app, command=new_frame,grid=[3,11,2,1], text = "New",padx=28)
button_new_frame = PushButton(app, command=copy_frame,grid=[5,11,2,1], text = "Duplicate")
button_new_frame = PushButton(app, command=delete_frame,grid=[7,11,2,1], text = "Delete", padx=20)


prev_matrix = Waffle(app,height=8,width=8,dim=8,color="grey",grid=[0,13,3,3])
next_matrix = Waffle(app,height=8,width=8,dim=8,color="grey",grid=[7,13,3,3])

menubar = MenuBar(app,
                  toplevel=["File"],
                  options=[
                      [ ["Import file", import_python],
                        ["Export as", export_as_python]
                         ]
                  ])
if os.path.isfile("/proc/device-tree/hat/product"):
    file = open("/proc/device-tree/hat/product","r")
    hat = file.readline()
    if  hat == "Sense HAT\x00":
        #print('Sense HAT detected')
        file.close()
    else:
        #print("No SenseHAT detected")
        no_hat_check()
else:
    #print("No SenseHAT detected")
    no_hat_check()


if not NOHAT: # SenseHat detected to run normally
    from sense_hat import SenseHat       
    sh = SenseHat()
    sh.clear(0,0,0)
else:
    if ONEMU: # No SenseHat - and we're on a Pi so try the emulator
        from sense_emu import SenseHat
        sh = SenseHat()
        sh.clear(0,0,0)
        NOHAT = False
    else: #Disable SenseHat functions
        text_rotation.disable()
        combo_rotation.disable()

app.display()



# Write your code here :-)
from guizero import App, PushButton, Slider, Waffle, Box,Text
from sense_hat import SenseHat
from time import sleep

sh = SenseHat()

sh.clear(0,0,0)

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
        col = (0,0,0)
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
    #print(col)
    box.bg =col
    button_clear.bg = col


def p_clicked(x,y):
    print(x,y)
    matrix.set_pixel(x,y,col)
    sh.set_pixel(x,y,col)
    frames[current_frame_number][(y*8)+x] = col 
    #print(frames)
    
def clear_matrix():
    sh.clear(col)
    for x in range(8):
        for y in range(8):
            matrix.set_pixel(x,y,col)

def new_frame():
    global current_frame_number
    global frames
    global blank_frame
    if current_frame_number != len(frames): # not last frame
        for f in range(len(frames), current_frame_number, -1):
            frames[f+1] = frames[f].copy()
            #print("shuffling " + str(f) + " to " + str(f+1))
    frames[current_frame_number+1] = blank_frame.copy()

    #print(current_frame_number, len(frames))
    current_frame_number +=1  

    load_frame()

def copy_frame():
    global current_frame_number
    global frames
    if current_frame_number != len(frames): # not last frame
        for f in range(len(frames), current_frame_number, -1):
            frames[f+1] = frames[f].copy()
    frames[current_frame_number+1] = frames[current_frame_number].copy()

    #print(current_frame_number, len(frames))
    current_frame_number +=1  

    load_frame()
    
def delete_frame():
    global current_frame_number
    global frames
    global blank_frame
    if current_frame_number != len(frames): # not last frame
        for f in range(current_frame_number, len(frames)):
            frames[f] = frames[f+1].copy()
    #print(current_frame_number, len(frames))
    del frames[len(frames)]
    load_frame()
    
def load_frame():
    #print(frames[current_frame_number])
    #print(current_frame_number)
    #print(frames)
    frame_status_text.value=("Frame " + str(current_frame_number).zfill(3) + " of " + str(len(frames)).zfill(3))
    #print(blank_frame)
    sh.set_pixels(frames[current_frame_number])
    for x in range(8):
        for y in range(8):
            matrix.set_pixel(x,y,frames[current_frame_number][(y*8)+x])
        
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
    global current_frame_number
    print(current_frame_number)
    t =  int(1000/framerate)
    for i in range(len(frames)):
        frame_status_text.after(t*i,right)

def export_python():
    global framerate
    with open("/home/pi/animation.py","w") as export_file:
        export_file.write("from sense_hat import SenseHat\n")
        export_file.write("from time import sleep\n")
        export_file.write("sh = SenseHat()\n")
        export_file.write("sh.clear(0,0,0)\n")
        for e in range(1,len(frames)):
            export_file.write("sh.set_pixels(" +str(frames[e]) + ")\n")
            export_file.write("sleep(1/"+str(framerate) +")\n")
            
def set_framerate():
    global framerate
    framerate = slider_framerate.value

app = App(layout="grid")
matrix = Waffle(app,height=8,width=8,dim=30,command=p_clicked,color="black",grid=[0,0,7,7])
palette = Waffle(app,height=8, width=1, dim =25, command = col_select,grid=[8,0,1,7])
palette.set_pixel(0, 0, "red")
palette.set_pixel(0,1, "green")
palette.set_pixel(0,2, "blue")
palette.set_pixel(0,3, "yellow")
palette.set_pixel(0,4, "black")
palette.set_pixel(0,5, "white")
palette.set_pixel(0,6, "pink")
palette.set_pixel(0,7, "orange")
box = Box(app, width=30,height=30,grid=[3,9,2,1])
box.bg =col
text_current_col = Text(app, text="Selected Colour:", grid=[0,9,3,1])
button_clear = PushButton(app, command=clear_matrix,grid=[9,0], text = "Clear")
button_clear.bg = col

frame_status_text = Text(app, text="Frame " + str(current_frame_number).zfill(3) + " of " + str(len(frames)).zfill(3), grid=[0,10,3,1])
button_new_frame = PushButton(app, command=new_frame,grid=[3,10,3,1], text = "New Frame")
button_new_frame = PushButton(app, command=copy_frame,grid=[6,10,3,1], text = "Copy Frame")
button_new_frame = PushButton(app, command=delete_frame,grid=[9,10,3,1], text = "Delete Frame")
button_go_start = PushButton(app, command=go_start,grid=[0,11,2,1], text = "<<")
button_left = PushButton(app, command=left,grid=[1,11,2,1], text = "<")
button_play = PushButton(app, command=play,grid=[2,11,2,1], text = "PLAY")
button_right = PushButton(app, command=right,grid=[3,11,2,1], text = ">")
button_go_end = PushButton(app, command=go_end,grid=[4,11,2,1], text = ">>")

slider_framerate = Slider(app, command=set_framerate, grid=[6,11,5,1],start=1, end=25)

button_export_python = PushButton(app, command=export_python,grid=[0,12,4,1], text = "Export Python")
app.display()



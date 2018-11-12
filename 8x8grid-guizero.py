# Write your code here :-)
from guizero import App, PushButton, Slider, Waffle, Box,Text
from sense_hat import SenseHat

sh = SenseHat()

sh.clear(0,0,0)

col = (255,255,255)
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
    print(col)
    box.bg =col
    button_clear.bg = col


def p_clicked(x,y):
    print(x,y)
    matrix.set_pixel(x,y,col)
    sh.set_pixel(x,y,col)
    
def clear_matrix():
    sh.clear(col)
    for x in range(8):
        for y in range(8):
            matrix.set_pixel(x,y,col)
            
app = App(layout="grid")
matrix = Waffle(app,height=8,width=8,dim=30,command=p_clicked,color="black",grid=[0,0,7,1])
palette = Waffle(app,height=8, width=1, dim =25, command = col_select,grid=[8,0])
palette.set_pixel(0, 0, "red")
palette.set_pixel(0,1, "green")
palette.set_pixel(0,2, "blue")
palette.set_pixel(0,3, "yellow")
palette.set_pixel(0,4, "black")
palette.set_pixel(0,5, "white")
palette.set_pixel(0,6, "pink")
palette.set_pixel(0,7, "orange")
box = Box(app, width=30,height=30,grid=[2,1,2,1])
box.bg =col
text_current_col = Text(app, text="Current Colour:", grid=[0,1,3,1])
button_clear = PushButton(app, command=clear_matrix,grid=[0,3], text = "Clear")
button_clear.bg = col
app.display()


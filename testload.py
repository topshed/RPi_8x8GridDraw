from astro_pi import AstroPi
import time

e = [0,0,0]
r = [255,0,0]

grid1 = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
    ]

grid2 = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,r,r,r,r,e,e,
    e,e,r,r,r,r,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
    ]

ani = [grid1,grid2]

ap=AstroPi()

for frame in ani:

	ap.set_pixels(frame)
	time.sleep(1)

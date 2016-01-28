#!/usr/bin/python
# 
# draw spirographs in vp3 embroidery format
# vp3rw class usage demo
#
# may need sudo apt-get install python-tk
#

import math
import vp3rw
import time
from Tkinter import *

# from pprint import pprint
# import inspect
master=Tk()


c_width=600
c_height=600
canvas_scale=0.6

canvas=Canvas(master,width=c_width, height=c_height)
canvas.pack(expand = YES, fill = BOTH)

def sin_div (a):
	return math.sin ( a*argmul )*sinmul+a*smul;


# pprint(inspect.getmembers(canvas))

cx=int(c_width/2)
cy=int(c_height/2)
divv1=6.0
divv2=10.0
limit=500
scale=6
cdivv1=2
cdivv2=3
argmul=3
sinmul=5
smul=0
rmul1=0
radmul=0
first=1
divv=15.0
stx=0
sty=0
vcount=0
current_color="#112233"
do_save=0


def transform_coord(x,y): # for canvas
	return int(x*canvas_scale)+cx,int(y*canvas_scale)+cy


def canvasline(x1,y1,x2,y2):
	xx1,yy1=transform_coord(x1,y1)
	xx2,yy2=transform_coord(x2,y2)
	canvas.create_line(xx1,yy1,xx2,yy2,width=1,fill=current_color)



def lineto (x,y):
	global lastx,lasty
	canvasline(lastx,lasty,x,y)
	lastx=x
	lasty=y
	if do_save: draw.lineto(int(x),int(y))

def moveto (x,y):
	global lastx,lasty, draw
	lastx=x
        lasty=y

        # DEBUG !!!
	# if do_save: draw.moveto(int(x),int(y))

 
def point ( x,y ):
# var xx, yy: integer;
	global stx, sty, divv, first, vcount
	xx= round ( x * divv ) + stx
	yy= round ( y * divv ) + sty
	#first=0
	if first:
		moveto ( xx, yy )
		first=0
	lineto ( xx,yy )
	vcount+=1

 
# procedure polar ( rad,ang: real ; var x,y: real );
def polar ( rad,ang ):
	x= rad * math.cos (ang)
	y= rad * math.sin (ang)
	return x,y

def nyhi3 ( f, div1, div2, scale):
	global limit, cdivv1, cdivv2, first, nurk_nihe
	divv= scale
	min_radius=1
	if div1==0: div1=1
	first=1

	for a in xrange (0, limit):
		r= f ( a / div1 )
		x,y=polar ( r + a *rmul1, a/div2 + r * radmul+nurk_nihe)
		if r > min_radius: point ( x*scale, y*scale )


def set_color(s):
	global current_color
	if do_save: draw.setcolor(s) # draw to vp3
	current_color=s # draw to tkinter canvas

rep_count=3


def redraw1():
	global nurk_nihe,divv1
	#time.sleep(1)
	canvas.delete("all") # clear screen
	nurk_nihe=0
	#ep_count=int(e.get())
	#divv1=float(e.get())
	if not do_save: divv1+=0.01
	#time.sleep(0.2)
	
	for i in xrange(rep_count):
		current_color="#ff0000"
		set_color(colors[i])
		nurk_nihe+=0.1
		nyhi3 ( sin_div, divv1, divv2, scale )


def redraw2():
	# while(divv1<10):
	redraw1()
		


def save():
	global do_save,draw
	draw= vp3rw.vp3(producer,settings)
	do_save=1
	redraw1()
	fname_nr=int(divv1 * 100)
	fname="spiro1-%d.vp3" % fname_nr
	draw.flush(fname)
	print "saved: ",fname
	do_save=0




producer="spirograaf"
settings="sinine #ff0000, punane #ff0000, roheline #00ff00"
# draw= vp3rw.vp3(producer,settings)


colors=["#0000ff","#ff0000","#00ff00","#11ddff","#1100ff","#01d0f0","#01ddff","#01d08f","#91ddff","#119dff","#d1ddff"]


red = Button(master, text="redraw", width=10, command=redraw2)
red.pack()
sav = Button(master, text="save", width=10, command=save)
sav.pack()

mainloop()

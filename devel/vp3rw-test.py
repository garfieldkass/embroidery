
#!/usr/bin/python

import sys
sys.path.append("/usr/share/inkscape/extensions")

import vp3rw

# todo rotating square. multi-colored 


class squares:
	def __init__(self,draw_fn):
		self.draw=draw_fn

	def square1(self, cx,cy, r,i):
		if i: 
			self.jj.lineto(cx+r,cy+r)
		else: 
			self.jj.moveto(cx+r,cy+r) # only first square does "moveto"
		self.jj.lineto(cx+r,cy-r)
		self.jj.lineto(cx-r,cy-r)
		self.jj.lineto(cx-r,cy+r)
		self.jj.lineto(cx+r,cy+r)

	def draw(self,cx,cy,r,d,cnt):
		for i in xrange(cnt): self.square1(cx,cy,5+i*d,i)


class flower:
	def __init__(self, draw_fn):
		self.drawfn=draw_fn
	def draw(self,cx,cy):
		self.drawfn.moveto(cx+4,cy+5)
		self.drawfn.lineto(cx+2,cy+3)
		self.drawfn.lineto(cx+5,cy+6)
		self.drawfn.lineto(cx-5,cy+6)
		self.drawfn.lineto(cx-5,cy-6)


# vp3 format requires some strings
producer="testing"
settings="settings"

testdraw= vp3rw.vp3(producer,settings)

rose=flower(testdraw)
shape=squares(testdraw)

color="#ffff00"
testdraw.setcolor(color)
shape.draw(10,10,20,3,7)
shape.draw(80,30,15,2,9)
shape.draw(0,70,7,2,5)
shape.draw(50,80,7,3,6)

color="#0000ff"
testdraw.setcolor(color)
shape.draw(200,190,7,2,5)
shape.draw(250,190,7,3,6)



color="#ff0000"
testdraw.setcolor(color)
shape.draw(200,0,7,2,5)
shape.draw(250,0,7,3,6)

rose.draw(20,20)
rose.draw(30,20)


color="#12ff56"
testdraw.setcolor(color)
shape.draw(133,33,4,1,9)
shape.draw(135,133,8,2,9)

#color="#567890"
#testdraw.setcolor(color)
shape.draw(87,88,4,2,5)
shape.draw(120,90,8,2,5)


testdraw.flush("squares.vp3")

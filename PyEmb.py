#!python
#!/usr/bin/python
# http://www.achatina.de/sewing/main/TECHNICL.HTM

import math
import sys
import vp3rw

dbg = sys.stderr

def abs(x):
	if (x<0): return -x
	return x



class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Point(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Point(self.x-other.x, self.y-other.y)

	def mul(self, scalar):
		return Point(self.x*scalar, self.y*scalar)
	
	def __repr__(self):
		return "Pt(%s,%s)" % (self.x,self.y)

	def length(self):
		return math.sqrt(math.pow(self.x,2.0)+math.pow(self.y,2.0))

	def unit(self):
		return self.mul(1.0/self.length())

	def rotate_left(self):
		return Point(-self.y, self.x)

	def as_int(self):
		return Point(int(round(self.x)), int(round(self.y)))

	def as_tuple(self):
		return (self.x,self.y)

	def __cmp__(self, other):
		return cmp(self.as_tuple(), other.as_tuple())


embroidery_len = 19100 # debug


class Embroidery:
	def __init__(self):
		self.coords = []

	def addStitch(self, coord):
		self.coords.append(coord)

	def translate_to_origin(self):
		if (len(self.coords)==0):
			return
		(maxx,maxy) = (self.coords[0].x,self.coords[0].y)
		(minx,miny) = (self.coords[0].x,self.coords[0].y)
		for p in self.coords:
			minx = min(minx,p.x)
			miny = min(miny,p.y)
			maxx = max(maxx,p.x)
			maxy = max(maxy,p.y)
		sx = maxx-minx
		sy = maxy-miny
		for p in self.coords:
			p.x -= minx
			p.y -= miny
		dbg.write("Field size %s x %s\n" % (sx,sy))

	def scale(self, sc):
		for p in self.coords:
			p.x *= sc
			p.y *= sc
			
	def export_ksm(self, dbg):
		str = ""
		self.pos = Point(0,0)
		lastColor = None
		for stitch in self.coords:
			if (lastColor!=None and stitch.color!=lastColor):
				mode_byte = 0x99
				#dbg.write("Color change!\n")
			else:
				mode_byte = 0x80
				#dbg.write("color still %s\n" % stitch.color)
			lastColor = stitch.color
			new_int = stitch.as_int()
			old_int = self.pos.as_int()
			delta = new_int - old_int
			assert(abs(delta.x)<=127)
			assert(abs(delta.y)<=127)
			str+=chr(abs(delta.y))
			str+=chr(abs(delta.x))
			if (delta.y<0):
				mode_byte |= 0x20
			if (delta.x<0):
				mode_byte |= 0x40
			str+=chr(mode_byte)
			self.pos = stitch
		return str

	def export_melco(self, dbg):
		self.str = ""
		self.pos = self.coords[0]
		dbg.write("stitch count: %d\n" % len(self.coords))
		lastColor = None
		numColors = 0x0
		for stitch in self.coords[1:]:
			if (lastColor!=None and stitch.color!=lastColor):
				numColors += 1
				# color change
				self.str += chr(0x80)
				self.str += chr(0x01)
#				self.str += chr(numColors)
#				self.str += chr(((numColors+0x80)>>8)&0xff)
#				self.str += chr(((numColors+0x80)>>0)&0xff)
			lastColor = stitch.color
			new_int = stitch.as_int()
			old_int = self.pos.as_int()
			delta = new_int - old_int

			def move(x,y):
				if (x<0): x = x + 256
				self.str+=chr(x)
				if (y<0): y = y + 256
				self.str+=chr(y)
				
			while (delta.x!=0 or delta.y!=0):
				def clamp(v):
					if (v>127):
						v = 127
					if (v<-127):
						v = -127
					return v
				dx = clamp(delta.x)
				dy = clamp(delta.y)
				move(dx,dy)
				delta.x -= dx
				delta.y -= dy
				
			#dbg.write("Stitch: %s delta %s\n" % (stitch, delta))
			self.pos = stitch
		return self.str   # melco
		
		
		

        
        
         
	def export_vp3(self, dbg):
		vp3o=vp3rw.vp3("inkscape plugin","settings")
		lastColor=""
		# for stitch in self.coords[1:]:
		for stitch in self.coords:
			if stitch.color!=lastColor:
				vp3o.setcolor(stitch.color)
				lastColor=stitch.color
			p = stitch.as_int()
			if stitch.cmd=="m":
				vp3o.lineto(p.x,p.y,1) # long
			else:
				vp3o.lineto(p.x,p.y)
		return vp3o.flush_str()

# vp3 ended *******************************************************


class Test:
	def __init__(self):
		emb = Embroidery()
		for x in range(0,301,30):
			emb.addStitch(Point(x, 0));
			emb.addStitch(Point(x, 15));
			emb.addStitch(Point(x, 0));

		for x in range(300,-1,-30):
			emb.addStitch(Point(x, -12));
			emb.addStitch(Point(x, -27));
			emb.addStitch(Point(x, -12));

		fp = open("test.exp", "wb")
		fp.write(emb.export_melco())
		fp.close()

class Turtle:
	def __init__(self):
		self.emb = Embroidery()
		self.pos = Point(0.0,0.0)
		self.dir = Point(1.0,0.0)
		self.emb.addStitch(self.pos)

	def forward(self, dist):
		self.pos = self.pos+self.dir.mul(dist)
		self.emb.addStitch(self.pos)

	def turn(self, degreesccw):
		radcw =  -degreesccw/180.0*3.141592653589
		self.dir = Point(
			math.cos(radcw)*self.dir.x-math.sin(radcw)*self.dir.y,
			math.sin(radcw)*self.dir.x+math.cos(radcw)*self.dir.y)

	def right(self, degreesccw):
		self.turn(degreesccw)

	def left(self, degreesccw):
		self.turn(-degreesccw)
	
class Koch(Turtle):
	def __init__(self, depth):
		Turtle.__init__(self)

		edgelen = 750.0
		for i in range(3):
			self.edge(depth, edgelen)
			self.turn(120.0)

		fp = open("koch%d.exp" % depth, "wb")
		fp.write(self.emb.export_melco())
		fp.close()
	
	def edge(self, depth, dist):
		if (depth==0):
			self.forward(dist)
		else:
			self.edge(depth-1, dist/3.0)
			self.turn(-60.0)
			self.edge(depth-1, dist/3.0)
			self.turn(120.0)
			self.edge(depth-1, dist/3.0)
			self.turn(-60.0)
			self.edge(depth-1, dist/3.0)

class Hilbert(Turtle):
	def __init__(self, level):
		Turtle.__init__(self)

		self.size = 10.0
		self.hilbert(level, 90.0)

		fp = open("hilbert%d.exp" % level, "wb")
		fp.write(self.emb.export_melco())
		fp.close()

	# http://en.wikipedia.org/wiki/Hilbert_curve#Python
	def hilbert(self, level, angle):
		if (level==0):
			return
		self.right(angle)
		self.hilbert(level-1, -angle)
		self.forward(self.size)
		self.left(angle)
		self.hilbert(level-1, angle)
		self.forward(self.size)
		self.hilbert(level-1, angle)
		self.left(angle)
		self.forward(self.size)
		self.hilbert(level-1, -angle)
		self.right(angle)

if (__name__=='__main__'):
	#Koch(4)
	Hilbert(6)

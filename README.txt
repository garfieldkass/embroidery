embroidery

inkscape embroidery vp3 output plugin based on 
  vp3 file format:
    https://community.kde.org/Projects/Liberty/File_Formats/Viking_Pfaff
    http://www.jasonweiler.com/VP3FileFormatInfo.html
  inkscape embroidery plugin:
    Jon Howell,2010 http://www.jonh.net/~jonh/inkscape-embroidery/


standalone vp3 rw class to easily create vp3 embroider files
simplest usage example of vp3rw class: 
draw=vp3rw.vp3()
draw.setcolor("#000000")
draw.moveto(10,10)
draw.lineto(100,100)
draw.lineto(100,0)
draw.lineto(0,0)
draw.flush("fname.vp3")


to install inkscape plugin:

linux:
  copy files: 
    PyEmb.py 	
    embroider.inx 	
    embroider.py 	
    vp3rw.py
  into inkscape plugin directory: ~/.config/inkscape/extensions

todo: installation instructions in windows, osx	
	

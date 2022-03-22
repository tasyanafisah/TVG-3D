"""
 Wireframe 3D cube simulation.
 graphics.py version by James Futhey <james@jamesfuthey.com>
 Original by Leonel Machava <leonelmachava@gmail.com>
"""
import sys, math
from graphics import *
import numpy as np
from time import sleep

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
        self.koordHomogen = np.array([x,y,z,1])
        
    def translasi (self, tx, ty, tz):
        MatrixTranslasi = np.array([[1,0,0,tx],
                                    [0,1,0,ty],
                                    [0,0,1,tz],
                                    [0,0,0,1]])
        xNew, yNew, zNew, homogen = (MatrixTranslasi @ self.koordHomogen)
        return Point3D(xNew, yNew, zNew)

 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, -1)

class Simulation:
    def __init__(self, win_width = 640, win_height = 480):

        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
        self.tx, self.ty, self.tz = 0,0,0

        
    def run(self):
        """ Main Loop """
        w=GraphWin("3D Wireframe cube Simulation", 800, 700)
        zzyzx=0
        l1 = [[],[],[],[],[],[]]
        l2 = [[],[],[],[],[],[]]
        l3 = [[],[],[],[],[],[]]
        l4 = [[],[],[],[],[],[]]   
        
        # Menulis judul
        title = Text(Point(400,50), 'Translasi Balok sebesar searah x, y, z')
        title.draw(w)

        # Meminta input besar sudut yang akan dirotasi
        entriX = Entry(Point(300,650), 5)
        entriY = Entry(Point(400,650), 5)
        entriZ = Entry(Point(500,650), 5)
        teks = Text(Point(400, 600), 'Masukkan satuan translasi, lalu klik di manapun pada window')
        teksX = Text(Point(300, 625), 'X')
        teksY = Text(Point(400, 625), 'Y')
        teksZ = Text(Point(500, 625), 'Z')
        entriX.setFill('white')
        entriY.setFill('white')
        entriZ.setFill('white')
        entriX.draw(w)
        entriY.draw(w)
        entriZ.draw(w)
        teks.draw(w)
        teksX.draw(w)
        teksY.draw(w)
        teksZ.draw(w)
        
        # Menerima input sudut rotasi
        w.getMouse()  # Program perlu suatu trigger agar program mengambil input dari kolom entri, getMouse berperan sbg trigger
        self.tx = int(entriX.getText())
        self.ty = int(entriY.getText())
        self.tz = int(entriZ.getText())
        entriX.undraw()
        entriY.undraw()
        entriZ.undraw()
        teks.undraw()
        teksX.undraw()
        teksY.undraw()
        teksZ.undraw()
        
        # Menuliskan subtitle 'Sudut putar: '
        subtitle = Text(Point(400,650), f'Tranlasi : [{self.tx} , {self.ty} , {self.tz}]')
        iterTranslasi = max(self.tx, self.ty, self.tz)*10
        subtitle.draw(w)
        
        for iterr in range(iterTranslasi):
            sleep(0.5)

            # Will hold transformed vertices.
            t = []
            gx = 0
            
            for i, v in enumerate(self.vertices):
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                self.vertices[i] = v.translasi(self.tx/iterTranslasi, self.ty/iterTranslasi, self.tz/iterTranslasi)
                # Transform the point from 3D to 2D
                p = self.vertices[i].project(800, 600, 300, 4)
                # Put the point in the list of transformed vertices
                t.append(p)

            if(zzyzx == 1):
                for i in range(6):
                    l1[i].undraw()
                    l2[i].undraw()
                    l3[i].undraw()
                    l4[i].undraw()
            else:
                zzyzx = 1
                      
            for langkah, f in enumerate(self.faces):
                l1[gx]=Line(Point(t[f[0]].x, t[f[0]].y), Point(t[f[1]].x, t[f[1]].y))
                l2[gx]=Line(Point(t[f[1]].x, t[f[1]].y), Point(t[f[2]].x, t[f[2]].y))
                l3[gx]=Line(Point(t[f[2]].x, t[f[2]].y), Point(t[f[3]].x, t[f[3]].y))
                l4[gx]=Line(Point(t[f[3]].x, t[f[3]].y), Point(t[f[0]].x, t[f[0]].y))
                
                l1[gx].setFill('gray')
                l2[gx].setFill('gray')
                l3[gx].setFill('gray')
                l4[gx].setFill('gray')
                
                if langkah in [1,4]:
                    l4[gx].setFill('red')
                elif langkah == 3:
                    l2[gx].setFill('red')
                elif langkah == 5:
                    l1[gx].setFill('red')
                
                l1[gx].draw(w)
                l2[gx].draw(w)
                l3[gx].draw(w)
                l4[gx].draw(w)
                gx+=1
                
        w.getMouse()
        w.close()

if __name__ == "__main__":
    Simulation().run()
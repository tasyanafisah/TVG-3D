from graphics import *
import numpy as np
from math import *
import sys
 
class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
        self.koordHomogen = np.array([x,y,z,1])
    #Shear
    def shear(self, shx,shy,shz):
        sh = [[0]*4]*4
        if shz == 0:
            sh = np.array([
                [1, 0, shx, 0], 
                [0, 1, shy, 0],
                [0, 0,  1,  0],
                [0, 0,  0,  1]
                ])
        elif shx == 0:
            sh = np.array([
                [1,  0,  0, 0],
                [0, shy, 0, 0],
                [0, shz, 1, 0],
                [0,  0,  0, 1]
            ])
        elif shy == 0:
            sh = np.array([
                [shx, 0, 0, 0],
                [0,   1, 0, 0],
                [shz, 0, 1, 0],
                [0,   0, 0, 1]
                ])
        
        result = np.dot(sh, [self.x, self.y, self.z, 1])
        
        return Point3D(result[0], result[1], result[2])
        
    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)
 
def run():
    values = []
    operation = int(input(
        """Apakah jenis shear yang ingin kamu lakukan?
        1. xy
        2. yz
        3. xz
        4. Tidak ada
        Jawablah hanya dengan mengetikkan angka 1 sampai 4!
        Masukkan pilihan: """))
    #Program dijalankan
    if operation > 4 or operation < 1:
        print("PILIHAN TIDAK TERSEDIA")
        sys.exit()
    elif operation == 1:
        xShear = float(input("Berapa banyak shear x? HANYA masukkan angka!\nInput: "))
        yShear = float(input("Berapa banyak shear y? HANYA masukkan angka!\nInput: "))
        values = [xShear, yShear, 0]
    elif operation == 2:
        yShear = float(input("Berapa banyak shear y? HANYA masukkan angka!\nInput: "))
        zShear = float(input("Berapa banyak shear z? HANYA masukkan angka!\nInput: "))
        values = [0, yShear, zShear]
    elif operation == 3:
        xShear = float(input("Berapa banyak shear x? HANYA masukkan angka!\nInput: "))
        zShear = float(input("Berapa banyak shear z? HANYA masukkan angka!\nInput: "))
        values = [xShear, 0, zShear]
    elif operation == 4:
        values = [0]
    return operation, values
 
 
#Fungsi utama program 
def main(operation, values, points):
    p = 0
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]
    width, height = 1280, 720
    lines = []
    operatedPoints = []
    transformedPoints = []
 
    #Shearing
    if operation == 1:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].shear(xShear, yShear, zShear))
    elif operation == 2:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].shear(xShear, yShear, zShear))
    elif operation == 3:
        xShear, yShear, zShear = values[0], values[1], values[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].shear(xShear, yShear, zShear))
    elif operation == 4:
        for i in range(len(points)):
            operatedPoints.append(points[i])
    
    #Melakukan proyeksi koordinat yang telah di transformasi pada bidang 2 dimensi
    for i in range(len(operatedPoints)):
        transformedPoints.append(operatedPoints[i].project(width, height, 600, 5))
 
    win = GraphWin('3D Transformation', width, height)
    win.setBackground('white')
 
    #Menentukan nilai garis pembentuk balok
    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
    #Menggambar garis pembentuk balok
    for i in lines:
        i.draw(win)
 
    #Menampilkan titik koordinat di x y z
    for i in range(len(transformedPoints)):
        p = Text(Point(transformedPoints[i].x, transformedPoints[i].y), "{:.2f}, {:.2f}, {:.2f}".format(operatedPoints[i].x, operatedPoints[i].y, operatedPoints[i].z))
        p.setSize(8)
        p.setTextColor('Red')
        p.draw(win) 
 
    ask = int(input("Apakah anda ingin melanjutkan operasi lainnya?\nMasukkan 1 jika iya, lainnya untuk keluar (hanya angka).\nInput: "))
    if ask==1:
        op, val = run()
        win.close()
        main(op,val, operatedPoints)
    else:
        sys.exit()  
    win.getMouse()
    win.close()
 
#Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
points =   [Point3D(-2,1,-1),
            Point3D(2,1,-1),
            Point3D(2,-1,-1),
            Point3D(-2,-1,-1),
            Point3D(-2,1,1),
            Point3D(2,1,1),
            Point3D(2,-1,1),
            Point3D(-2,-1,1)]
 
op, val = run()
main(op, val, points)

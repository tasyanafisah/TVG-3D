from cgitb import text
from graphics import *
import numpy as np

def main(list_point):
    # Setup window
    win = GraphWin('Rotasi terhadap sumbu x, y, atau z', 600,600)
    win.setCoords(-6,-6,6,6)
    
    # Menulis judul
    title = Text(Point(0, 5.2), 'Memutar balok terhadap sumbu x, y, atau z')
    title.draw(win)
    
    # Menggambar posisi awal balok
    corners, skeletons = draw(win, list_point, keep=True)
    
    # Menggambar sumbu putar
    sumbuZ = Line(Point(-5,0),Point(5,0))
    sumbuZ.setFill('purple')
    sumbuZ.draw(win)
    
    sumbuY = Line(Point(0,-3.4),Point(0,4.5))
    sumbuY.setFill('blue')
    sumbuY.draw(win)
    
    titikX = Point(0,0)
    sumbuX = Circle(titikX, 0.2)
    sumbuX.setOutline('green')
    sumbuX.setWidth(2)
    sumbuX.draw(win)

    teksSbZ = Text(Point(0,4.8), 'z')
    teksSbY = Text(Point(5.2,0), 'y')
    teksSbX = Text(Point(0.3,0.3), 'x')
    teksSbZ.draw(win)
    teksSbY.draw(win)
    teksSbX.draw(win)
    
    # Meminta input sumbu yang akan dirotasi
    entriSumbu = Entry(Point(0,-4.3), 5)
    teksSumbu = Text(Point(0,-3.9), 'Masukkan sumbu rotasi, lalu klik di manapun pada window')
    entriSumbu.setFill('white')
    entriSumbu.draw(win)
    teksSumbu.draw(win)

    # Meminta input besar sudut yang akan dirotasi
    entriSudut = Entry(Point(0,-5.2), 5)
    teks = Text(Point(0, -4.8), 'Masukkan sudut putar, lalu klik di manapun pada window')
    entriSudut.setFill('white')
    entriSudut.draw(win)
    teks.draw(win)
    
    # Menerima input sudut rotasi
    win.getMouse()  # Program perlu suatu trigger agar program mengambil input dari kolom entri, getMouse berperan sbg trigger
    sudut = int(entriSudut.getText())
    sumbu = (entriSumbu.getText())
    if(sumbu == 'x'):
        sumbu = 'x'
    elif(sumbu == 'y'):
        sumbu = 'y'
    elif(sumbu == 'z'):
        sumbu = 'z'
    else:
        win.close()
    entriSudut.undraw()
    entriSumbu.undraw()
    teksSumbu.undraw()
    teks.undraw()
    
    # Menuliskan subtitle 'Sudut putar: '
    subtitle = Text(Point(0,-5.2), f'Sudut putar : {sudut}°\nSumbu rotasi : {sumbu}')
    subtitle.draw(win)
    
    # Menghapus posisi awal balok
    for corner in corners: corner.undraw()
    for skeleton in skeletons: skeleton.undraw()
        
    # Merotasi balok
    for iterr in range(sudut):
        isFinished = True if (iterr==sudut-1) else False        
        draw(win, list_point, isFinished)
        list_point = rotatexyz(list_point,sumbu)
    
    # Program selesai
    win.getMouse()
    win.close()

def draw(window, list_point, keep=False):
    """
    Fungsi untuk Menggambar titik sudut dan garis kerangka balok
    
    Args: 
        windows (graphics.GraphWin): window dimana objek akan digambar
        list_point (list) : list titik sudut yang akan digambar
        keep (bool) : flag penentu apakah bangun yang telah digambar ingin disimpan atau tidak
        
    Returns:
        points (list of Point) : list dari Point yang telah digambar
        lines (list of Line) : list dari Line yang telah digambar
    """
    
    points = []  # list penampung semua objek Point
    lines = []  # list penampung semua objek Line
    
    # Menggambar titik sudut balok
    for i, koor_point in enumerate(list_point):
        point_temp = Point(koor_point[1],koor_point[2])  
        # Hanya mengambil koordinat y dan z dari koor_point
        # Hal ini karena layar desktop dispan oleh sumbu y dan z, sedangkan sumbu x ⟂ layar
        points.append(point_temp)
        points[i].draw(window)
    
    # Menggambar garis kerangka balok untuk sisi atas (A-B-C-D) dan bawah (E-F-G-H)
    bidangAtasLaluBawah = [0,4]
    for j in bidangAtasLaluBawah:
        for k in range(j, 4+j):
            line_temp = None
            if (k+1) != 4+j:
            # Garis (AB, BC, CD, dan EF, FG, GH)
                line_temp = Line(points[k], points[k+1])
                # print(f'point {k}:', k,',', k+1) --> troubleshooting, uncomment untuk melihat indeks line
            else:
            # Garis (DA dan HE)
                line_temp = Line(points[k], points[k-3])
                # print(f'point {k}:', k, ',', k-3) --> troubleshooting, uncomment untuk melihat indeks line
            lines.append(line_temp)
            
            lines[k].draw(window)
            
    # Menggambar garis kerangka balok untuk sisi samping: (A-E), (B-F), (C-G), (D-H)
    for l in range(4):
        # print(f'point {8+l}:', l,',',l+4) --> troubleshooting, uncomment untuk melihat indeks line
        line_temp = Line(points[l],points[l+4])
        lines.append(line_temp)
        lines[8+l].draw(window)
    
    # Jeda
    time.sleep(.03)
    
    # Untuk iterasi terakhir, gambar dibiarkan tetap di window
    # Jika bukan iter terakhir, gambar segera di-undraw
    if not keep:
        for point in points:
            point.undraw()
        for line in lines:
            line.undraw()
            
    return points, lines

def rotatexyz(list_point, sumbu):
    """
    Fungsi untuk merotasi titik sebesar sudut tertentu thd sumbu x, y, atau z
    
    Rumus matriks:
        Rx : [1,      0,       0, 0]
             [0, cos(x), -sin(x), 0]
             [0, sin(x),  cos(x), 0]
             [0,      0,       0, 0]

        Ry : [ cos(x), 0, sin(x), 0]
             [      0, 1,      0, 0]
             [-sin(x), 0, cos(x), 0]
             [      0, 0,      0, 0]

        Rz : [cos(x), -sin(x), 0, 0]
             [sin(x),  cos(x), 0, 0]
             [     0,       0, 1, 0]
             [     0,       0, 0, 0]
    Args:
        list_point (list) : list titik yang akan dirotasi
    
    Returns:
        List titik setelah dirotasi
    """
    list_point_transpos = np.array(list_point).T
    
    # cos dan sin sudut
    sudut_rad = np.radians(1)
    cos_sudut = np.cos(sudut_rad)
    sin_sudut = np.sin(sudut_rad)

    # Rumus rotasi sumbu x
    if(sumbu == 'x'):
        putar = np.array([[1,0,0,0],
                     [0,cos_sudut, -sin_sudut, 0],
                     [0,sin_sudut, cos_sudut, 0],
                     [0,0,0,1]])
    # Rumus rotasi sumbu y
    elif(sumbu == 'y'):
        putar = np.array([[cos_sudut, 0, sin_sudut, 0],
                  [0,      1, 0,      0],
                  [-sin_sudut,0, cos_sudut, 0],
                  [0,      0, 0,      1]])
    # Rumus rotasi sumbu z
    elif(sumbu == 'z'):
        putar = np.array([[cos_sudut, -sin_sudut,0,0],
                       [sin_sudut, cos_sudut, 0,0],
                       [0,         0,                     1,0],
                       [0,                     0,                     0,1]])

    # Matriks rotasi
    M = putar
    
    return (M @ list_point_transpos).T

# Setup koordinat balok
A = np.array([1,-2,1,1])
B = np.array([1,2,1,1])
C = np.array([-1,2,1,1])
D = np.array([-1,-2,1,1])
E = np.array([1,-2,-1,1])
F = np.array([1,2,-1,1])
G = np.array([-1,2,-1,1])
H = np.array([-1,-2,-1,1])

# Matriks seluruh koordinat balok
points_awal = [A,B,C,D,E,F,G,H]

# Run program
main(points_awal)
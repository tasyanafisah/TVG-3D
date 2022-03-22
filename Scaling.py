#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from graphics import *
import numpy as np


# In[ ]:


def main(list_point):
    
    """
    PROGRAM UTAMA
    Fungsi untuk menampilkan scaling balok
    
    Args: 
        list_point (list atau np.array) : List titik sudut dari bangun ruang balok yang akan di scale
    Returns:
        None
    """
    
    # Setup window
    win = GraphWin('Scaling', 800,600)
    win.setCoords(-6,-6,6,6)
    
    # Menulis judul
    title = Text(Point(0, 5.2), 'Melakukan scaling terhadap balok')
    title.draw(win)
    
    # Menggambar posisi awal balok
    corners, skeletons = draw(win, list_point, keep=True)
    
    # Meminta input besar skala scaling terhadap sumbu x
    entriScaleX = Entry(Point(0,-5.2), 5)
    teks = Text(Point(0, -4.8), 'Masukkan skala scaling terhadap sumbu x, lalu klik di manapun pada window')
    entriScaleX.setFill('white')
    entriScaleX.draw(win)
    teks.draw(win)
    
    # Menerima input skala scaling terhadap sumbu x
    win.getMouse()  # Program perlu suatu trigger agar program mengambil input dari kolom entri, getMouse berperan sbg trigger
    scaleX = int(entriScaleX.getText())
    entriScaleX.undraw()
    teks.undraw()
    
    # Meminta input besar skala scaling terhadap sumbu y
    entriScaleY = Entry(Point(0,-5.2), 5)
    teks = Text(Point(0, -4.8), 'Masukkan skala scaling terhadap sumbu y, lalu klik di manapun pada window')
    entriScaleY.setFill('white')
    entriScaleY.draw(win)
    teks.draw(win)
    
    # Menerima input skala scaling terhadap sumbu x
    win.getMouse()  # Program perlu suatu trigger agar program mengambil input dari kolom entri, getMouse berperan sbg trigger
    scaleY = int(entriScaleY.getText())
    entriScaleY.undraw()
    teks.undraw()
    
    # Meminta input besar skala scaling terhadap sumbu z
    entriScaleZ = Entry(Point(0,-5.2), 5)
    teks = Text(Point(0, -4.8), 'Masukkan skala scaling terhadap sumbu z, lalu klik di manapun pada window')
    entriScaleZ.setFill('white')
    entriScaleZ.draw(win)
    teks.draw(win)
    
    # Menerima input skala scaling terhadap sumbu z
    win.getMouse()  # Program perlu suatu trigger agar program mengambil input dari kolom entri, getMouse berperan sbg trigger
    scaleZ = int(entriScaleZ.getText())
    entriScaleZ.undraw()
    teks.undraw()
    
    # Menuliskan subtitle Skala scaling untuk masing masing sumbu x, y, dan z
    subtitle = Text(Point(0,-5.2), f'Skala scaling sumbu x : {scaleX} \nSkala scaling sumbu y : {scaleY} \nSkala scaling sumbu z : {scaleZ}')
    subtitle.draw(win)
    
    # Menghapus posisi awal balok
    for corner in corners: corner.undraw()
    for skeleton in skeletons: skeleton.undraw()
        
    # Merotasi balok
    list_point = rotate(list_point, scaleX, scaleY, scaleZ)
    draw(win, list_point, False)
    
    # Program selesai
    win.getMouse()
    win.close()


# In[ ]:


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
    
            
    return points, lines


# In[ ]:


def rotate(list_point, scaleX, scaleY, scaleZ):
    
    """
    Fungsi untuk melakukan scaling pada balok sesuai dengan skala scaling yang di-input user
    
    Rumus:
        Matriks scaling x Matriks dari titik posisi awal balok
    Args:
        list_point (list) : list titik yang akan dilakukan scaling
    Returns:
        List titik setelah dilakukan scaling
    """
    
    list_point_transpos = np.array(list_point).T
    
    # Matriks scaling
    S = np.array([[scaleX,0,0,0],
                  [0,scaleY,0,0],
                  [0,0,scaleZ,0],
                  [0,0,0,1]])
    
    return (S @ list_point_transpos).T


# In[ ]:


# Inisiasi koordinat balok
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


# In[ ]:


# Run program
main(points_awal)


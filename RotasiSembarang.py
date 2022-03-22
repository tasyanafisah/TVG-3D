from graphics import *
import numpy as np

def main(list_point):
    """
    PROGRAM UTAMA
    Fungsi untuk menampilkan rotasi balok
    
    Args: 
        list_point (list atau np.array) : List titik sudut dari bangun ruang
        
    Returns:
        None
    """
    
    # Setup window
    win = GraphWin('Rotasi terhadap sembarang sumbu', 600,600)
    win.setCoords(-6,-6,6,6)
    
    # Menulis judul
    title = Text(Point(0, 5.2), 'Memutar balok terhadap garis 3,3,3 - 5,5,5')
    title.draw(win)
    
    # Menggambar posisi awal balok
    corners, skeletons = draw(win, list_point, keep=True)
    
    # Menggambar sumbu putar
    sumbu = Line(Point(3,3),Point(5,5))
    sumbu.setFill('red')
    sumbu.draw(win)
    
    sumbuExtend = Line(Point(-4.5,-4.5),Point(3,3))
    sumbuExtend.setFill('pink')
    sumbuExtend.draw(win)
    
    teksPangkal = Text(Point(3.2,2.7), '3,3,3')
    teksUjung = Text(Point(5.2,5.2), '5,5,5')
    teksPangkal.draw(win)
    teksUjung.draw(win)
    
    # Meminta input besar sudut yang akan dirotasi
    entriSudut = Entry(Point(0,-5.2), 5)
    teks = Text(Point(0, -4.8), 'Masukkan sudut putar, lalu klik di manapun pada window')
    entriSudut.setFill('white')
    entriSudut.draw(win)
    teks.draw(win)
    
    # Menerima input sudut rotasi
    win.getMouse()  # Program perlu suatu trigger agar program mengambil input dari kolom entri, getMouse berperan sbg trigger
    sudut = int(entriSudut.getText())
    entriSudut.undraw()
    teks.undraw()
    
    # Menuliskan subtitle 'Sudut putar: '
    subtitle = Text(Point(0,-5.2), f'Sudut putar : {sudut}°')
    subtitle.draw(win)
    
    # Menghapus posisi awal balok
    for corner in corners: corner.undraw()
    for skeleton in skeletons: skeleton.undraw()
        
    # Merotasi balok
    for iterr in range(sudut):
        isFinished = True if (iterr==sudut-1) else False        
        draw(win, list_point, isFinished)
        list_point = rotate(list_point)
    
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

def rotate(list_point):
    """
    Fungsi untuk merotasi titik sebesar sudut tertentu thd sumbu 3,3,3 - 5,5,5 (mirip PR kemarin)
    
    Rumus:
        Invers T x R(β) x R(-μ) x Rotasi x R(μ) x R(-β) x T
    Args:
        list_point (list) : list titik yang akan dirotasi
    
    Returns:
        List titik setelah dirotasi
    """
    list_point_transpos = np.array(list_point).T
    
    # cos dan sin (-45)
    cos_45 = np.cos(np.radians(-45))
    sin_45 = np.sin(np.radians(-45))

    # miu (sbg argumen matriks R(μ)), 
    miu_rad = np.arctan(1/np.sqrt(2))
    miu = np.degrees(miu_rad)
    
    # cos dan sin (45)
    cos45 = np.cos(np.radians(45))
    sin45 = np.sin(np.radians(45))

    # Matriks translasi 3,3,3-5,5,5 ke origin
    # T
    T = np.array([[1,0,0,-3],
                  [0,1,0,-3],
                  [0,0,1,-3],
                  [0,0,0,1]])

    # matriks untuk merotasi sumbu putar (3,3,3-5,5,5) sebesar -45 derajat ke bidang yz
    # R(-β)
    R_45 = np.array([[cos_45, 0, sin_45, 0],
                  [0,      1, 0,      0],
                  [-sin_45,0, cos_45, 0],
                  [0,      0, 0,      1]])
    
    # Matriks utk merotasi sumbu putar ke sumbu z
    # R(μ)
    Rmiu = np.array([[1,0,0,0],
                     [0,np.cos(miu_rad), -np.sin(miu_rad), 0],
                     [0,np.sin(miu_rad), np.cos(miu_rad), 0],
                     [0,0,0,1]])
    
    # Rotasi sebesar sudut yg diinginkan
    Rotasi = np.array([[np.cos(np.radians(1)), -np.sin(np.radians(1)),0,0],
                       [np.sin(np.radians(1)), np.cos(np.radians(1)), 0,0],
                       [0,                     0,                     1,0],
                       [0,                     0,                     0,1]])
    
    # Inverse Rmiu
    # R(-μ)
    R_miu = np.array([[1,0,0,0],
                     [0,np.cos(-miu_rad), -np.sin(-miu_rad), 0],
                     [0,np.sin(-miu_rad), np.cos(-miu_rad), 0],
                     [0,0,0,1]])
    
    # Inverse R_45
    # R(β)
    R45 = np.array([[cos45, 0, sin45, 0],
                  [0,      1, 0,      0],
                  [-sin45,0, cos45, 0],
                  [0,      0, 0,      1]])
    
    # Inverse T
    T_1 = np.linalg.inv(T)

    # Matriks rotasi keseluruhan
    # Rumus: Invers T x R(β) x R(-μ) x Rotasi x R(μ) x R(-β) x T
    M = T_1 @ R45 @R_miu @ Rotasi @Rmiu @ R_45 @ T
    
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

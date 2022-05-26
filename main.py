import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import hsv_to_rgb

def drukuj(obraz):
    # pokazanie obrazu
    cv2.imshow("1", obraz)
    cv2.waitKey()
    cv2.destroyAllWindows()

def wykresHSV(obraz):
# https://realpython.com/python-opencv-color-spaces/#picking-out-a-range

    #podzielenie obrazu
    h, s, v = cv2.split(obraz)

    #stworzenie wykresu
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")

    #splaszczenie do listy i normalizacji pixeli
    pixel_colors = obraz.reshape((np.shape(obraz)[0] * np.shape(obraz)[1], 3))
    norm = colors.Normalize(vmin=-1., vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()

    #dalsze tworzenie wykresu
    axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show()

#ścieżka obrazu
sciezka=r'D:\semestr6\wm_proj\mix2.jpg'

#wczytanie obrazu
obraz = cv2.imread(sciezka)

#zmniejszenie
obraz = cv2.pyrDown(obraz)

#konwersja na skale szarosci
gray=cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)

#pozbycie sie szumow
blur=cv2.GaussianBlur(gray, (7, 7), 0)

#znalezienie wszystkich nominalow
circles=cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=20,maxRadius=45)

# Tworzenie maski
mask = np.zeros(obraz.shape[:2], np.uint8)
circles = np.uint16(np.around(circles))#potrzebne bo kod nie dziala
#rysowanie kołek na masce
for i in circles[0,:]:
    mask = cv2.circle(mask, (i[0],i[1]), i[2], 255, -1)
    print(i[2])

#przemaskowanie
img_copy = obraz.copy()
img_copy[mask!=255] = 0



#wartosci do maski dla zlotcyh monet odczytane mniejwiecej w wykresu i dobrane eksperymentalnie
zloty=(0,70,70)
zloty2=(250,250,250)

srebny=(0,0,0)
srebny2=(250,250,250)

#przejscie na HSV
obraz_HSV=cv2.cvtColor(img_copy,cv2.COLOR_RGB2HSV)

#stworzenie maski dla zlotcyh monet
maska_zlota=cv2.inRange(obraz_HSV, zloty, zloty2)

#stworzenie maski dla srebnych monet
maska_srebna=cv2.inRange(obraz_HSV, srebny, srebny2)



#obraz z samymi zlotymi monetami
obraz_zloty = cv2.bitwise_and(img_copy, img_copy, mask=maska_zlota)



#obraz z samymi srebnymi monetami
#obraz_srebny = cv2.bitwise_and(img_copy, img_copy, mask=maska_srebna)

obraz_srebny=img_copy.copy()
obraz_srebny[maska_zlota==255] = 0



drukuj(obraz_srebny)








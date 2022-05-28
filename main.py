import cv2
import numpy as np
import urllib.request

#funckja zwraca obraz mozliwy do przetwarzania przez opencv, ktory zostal pobrany z githuba
def zwrocObrazGithub(i):
    # url zdjec z githuba
    url = ["https://github.com/sarna320/WMA/blob/master/mix.jpg?raw=true",
           "https://github.com/sarna320/WMA/blob/master/mix2.jpg?raw=true",
           "https://github.com/sarna320/WMA/blob/master/srebne.jpg?raw=true"]

    # wgranie zdjeciaa
    url_response = urllib.request.urlopen(url[i])

    # przekonwertowanie zdjecia do formatu odowiedniego dla opencv
    obraz = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)

    # zmniejszenie
    obraz = cv2.pyrDown(obraz)

    return obraz

#funckja do drukowania obrazu
def drukujObraz(obraz):
    # pokazanie obrazu
    cv2.imshow("1", obraz)
    cv2.waitKey()
    cv2.destroyAllWindows()

#funckja zwraca obraz z wszystkimi wykrytymi nominalami na zdjecie, gdzi tlo zamieniane jest na czarny kolor
def wszyskieNominaly(obraz):
    # konwersja na skale szarosci
    gray = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)

    # pozbycie sie szumow
    blur = cv2.GaussianBlur(gray, (17, 17), 0)

    # znalezienie wszystkich nominalow param2=odleglosc
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=25, maxRadius=45)
    circles = np.uint16(np.around(circles))  # potrzebne bo kod nie dziala

    # Tworzenie maski
    mask = np.zeros(obraz.shape[:2], np.uint8)

    temp = obraz.copy()

    # rysowanie kołek na masce
    for i in circles[0, :]:
        mask = cv2.circle(mask, (i[0], i[1]), i[2], 255, -1)
        cv2.circle(temp, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # print(i[2])

    # przemaskowanie
    img_copy = obraz.copy()
    img_copy[mask!=255]=0
    return img_copy


obraz=zwrocObrazGithub(0)

wszystkie=wszyskieNominaly(obraz)

#wartosci do maski dla zlotcyh monet odczytane mniejwiecej w wykresu i dobrane eksperymentalnie
zloty=(0,70,0)
zloty2=(250,250,250)

#przejscie na HSV
obraz_HSV=cv2.cvtColor(wszystkie,cv2.COLOR_RGB2HSV)

#stworzenie maski dla zlotcyh monet
maska_zlota=cv2.inRange(obraz_HSV, zloty, zloty2)

#obraz z samymi zlotymi monetami
obraz_zloty = cv2.bitwise_and(wszystkie, wszystkie, mask=maska_zlota)

#konwersja na skale szarosci
gray_zloty=cv2.cvtColor(obraz_zloty, cv2.COLOR_BGR2GRAY)

#pozbycie sie szumow
blur_zloty=cv2.GaussianBlur(gray_zloty, (7, 7), 0)

#znalezienie zlotych nominalow
circles_zloty=cv2.HoughCircles(blur_zloty,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=20,maxRadius=45)
circles_zloty = np.uint16(np.around(circles_zloty))#potrzebne bo kod nie dziala

for i in circles_zloty[0,:]:
    print(i[2],"zl")
    cv2.circle(obraz, (i[0], i[1]), i[2], (0, 255, 0), 2)

obraz_srebny = wszystkie.copy()
obraz_srebny[maska_zlota==255] = 0

drukujObraz(wszystkie)








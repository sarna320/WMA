import cv2
import numpy as np
import urllib.request

#funckja zwraca obraz mozliwy do przetwarzania przez opencv, ktory zostal pobrany z githuba
#argumentem wejsciowym jest numer linku
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
#argumentem wejsciowym jest obraz do pokazania
def drukujObraz(obraz):
    # pokazanie obrazu
    cv2.imshow("1", obraz)
    cv2.waitKey()
    cv2.destroyAllWindows()

#funckja zwraca obraz z wszystkimi wykrytymi nominalami na zdjecie, gdzie tlo zamieniane jest na czarny kolor
#argumentem wejsciowym jest obraz z monetami
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

    # przemaskowanie
    img_copy = obraz.copy()
    img_copy[mask!=255]=0
    return img_copy

#funkcja zwraca 2 obrazy: 1-zlote monety, 2-srebne monety. Oba na czarnym tle
#argumentem wejsciowym jest obraz z monetami gdzie tlo czarne
def rodzielZloty(obraz):
    # wartosci do maski dla zlotcyh monet odczytane mniejwiecej w wykresu i dobrane eksperymentalnie
    zloty = (0, 70, 0)
    zloty2 = (250, 250, 250)

    # przejscie na HSV
    obraz_HSV = cv2.cvtColor(obraz.copy(), cv2.COLOR_RGB2HSV)

    # stworzenie maski dla zlotcyh monet
    maska_zlota = cv2.inRange(obraz_HSV, zloty, zloty2)

    # obraz z samymi zlotymi monetami
    obraz_zloty = cv2.bitwise_and(wszystkie, wszystkie, mask=maska_zlota)

    return obraz_zloty

# def rodzielSrebne(obraz,gray_zloty):
#     # znalezienie wszystkich nominalow o kolorze zlotym param2=odleglosc
#     circles = cv2.HoughCircles(gray_zloty, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=20, maxRadius=45)
#     circles= np.uint16(np.around(circles))  # potrzebne bo kod nie dziala
#     # jesli tak to nastapi rysowanie kołek czarnych kolek w miejscje znalezionych zlotych monet
#     for i in circles:
#         obraz_srebny = cv2.circle(obraz, (i[0], i[1]), 46, 0, -1)
#
#     return obraz_srebny
"---------------------------------------------------------------------------------------------------------------------"

obraz=zwrocObrazGithub(2)

wszystkie=wszyskieNominaly(obraz)

obraz_zloty=rodzielZloty(wszystkie)

# #konwersja na skale szarosci
# gray_zloty=cv2.cvtColor(obraz_zloty, cv2.COLOR_BGR2GRAY)
#
# obraz_srebne=wszystkie.copy()
# # sprawdzenie czy znalazlo jakiekolwiek monety
# if cv2.countNonZero(gray_zloty) != 0:
#     obraz_srebne=rodzielSrebne(obraz_srebne,gray_zloty)

drukujObraz(obraz_zloty)









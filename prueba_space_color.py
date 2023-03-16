import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import time

GENERAL_PATH = os.getcwd()
n = 25
test_times = []
num_photos = []
contador = 0
total_time = time.time()
# Creo diccionario con nombre de las fotos
test_dict = {}
for file in os.listdir(GENERAL_PATH+"/Dataset/cafe_buenoEI/"):
    test_dict[file]=0

for i in range(0,n):

    for file in os.listdir(GENERAL_PATH+"/Dataset/cafe_buenoEI/"):
        #print(file)
        img = cv2.imread(GENERAL_PATH+"/Dataset/cafe_buenoEI/"+file)
        img = cv2.resize(img, (640, 480)) #para hacer las fotos pequeñas
        lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        start_time = time.time()


        # Red mask
        lower_red = np.array([0, 120, 0])
        upper_red = np.array([50, 200, 150]) #Ligthness, rojo a verde, azul a amarillo
        mask = cv2.inRange(lab_img, lower_red, upper_red)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        result = cv2.bitwise_and(img, img, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in contours:
            area = cv2.contourArea(c)
            if area > 70000:
                cv2.drawContours(img, [c], -1, (0, 255, 0), 5)
                #print(area)
        #result = cv2.resize(result, (640, 480))
        #img = cv2.resize(img, (640, 480))

        total_time = time.time() - start_time
        #test_times.append(total_time)
        test_dict[file] += total_time
        if i == 0:
            num_photos.append(contador)
            contador += 1
        ##print("Tiempo de ejecucion de foto "+ str(file)+": "+ str(total_time))
        #cv2.imshow("prueba"+file, result)
        #cv2.imshow("foto con bordes" + file,img)
    print(i)
#cv2.waitKey(0)
print("dict sin prom: ", test_dict.values())
for i in test_dict.values():
    test_times.append(i/n)
print("list con prom: ", len(test_times), len(num_photos))
timepo_deseado = [0.03]*len(test_times)

final_time = time.time() - total_time
print(sum(test_times)/len(test_times), final_time%60)
plt.plot(num_photos, test_times)
plt.plot(num_photos, timepo_deseado, "r--")
plt.title("Analisis de tiempo fotos (640, 480) HSV")
plt.ylabel("tiempo estimado por foto (promedio 25 iteraciones)")
#plt.ylim(0,0.035)
plt.xlabel("Foto a analizar")
plt.legend(["Tiempo x foto (s)", "Tiempo deseado(s)"])
plt.grid()
plt.show()





"""
bgr = [40, 158, 16]
thresh = 70

"HSV"
HSV_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
minHSV = np.array([hsv[0] - thresh, hsv[1] - thresh, hsv[2] - thresh])
maxHSV = np.array([hsv[0] + thresh, hsv[1] + thresh, hsv[2] + thresh])

maskHSV = cv2.inRange(HSV_img, minHSV, maxHSV)
resultHSV = cv2.bitwise_and(HSV_img, HSV_img, mask=maskHSV)

"Lab"
LAB_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
lab = cv2.cvtColor( np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0][0]

minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

maskLAB = cv2.inRange(LAB_img, minLAB, maxLAB)
resultLAB = cv2.bitwise_and(LAB_img, LAB_img, mask=maskLAB)

"ycb"
YCB_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
#convert 1D array to 3D, then convert it to YCrCb and take the first element
ycb = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YCrCb)[0][0]
minYCB = np.array([ycb[0] - thresh, ycb[1] - thresh, ycb[2] - thresh])
maxYCB = np.array([ycb[0] + thresh, ycb[1] + thresh, ycb[2] + thresh])
maskYCB = cv2.inRange(YCB_img, minYCB, maxYCB)
resultYCB = cv2.bitwise_and(YCB_img, YCB_img, mask=maskYCB)


img = cv2.resize(img, (400, 300))
LAB_img = cv2.resize(resultLAB, (400, 300))
HSV_img = cv2.resize(resultHSV, (400, 300))
YCB_img = cv2.resize(resultYCB, (400, 300))

cv2.imshow("rgb", img)
cv2.imshow("lab", LAB_img)
cv2.imshow('YCB',YCB_img)
cv2.imshow("HSV", img)
cv2.waitKey(0)
"""
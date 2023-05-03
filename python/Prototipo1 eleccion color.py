#! /usr/bin/env python3
"""
Created on Tue Aug  11 15:00:22 2022

@author: Santiago Rodriguez Avila
"""

import serial
import cv2
import numpy as np
import time

# pines de arduino
pin_0 = 5
pin_1 = 6
pin_2 = 7
pin_3 = 8
pin_4 = 9
pin_5 = 10
encendidos = [0, 0, 0, 0, 0, 0]
serialArduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

# red mask
lower_red1 = np.array([0, 50, 45])# HSV2 -H[160-175,0-20] S[75-255] V[45,180]rojo
upper_red1 = np.array([20, 255, 180])
lower_red2 = np.array([165, 50, 45])
upper_red2 = np.array([179, 255, 180])

# green mask
lower_green = np.array([30, 145, 155])
upper_green = np.array([60, 255, 255])

# funcion que detecta los bordes segun la mascara que se le pase
def find_contours(mascara, color):
    mascara_verde = ('g' == color)
    # Find contours tiene 3 entradas, imagen, contorno y jerarquia
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contorno para objetos mayores a cierta area
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 2500 and not mascara_verde:
            M = cv2.moments(c)
            if M["m00"] == 0: M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            cv2.circle(frame, (x, y), 6, (250, 50, 50), -1)

            nuevo_contorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevo_contorno], 0, (255, 0, 0), 3)
            if x <= 320:
                if not mascara_verde:
                    #print("zona 1 hay cafe bueno")
                    encendidos[0] = 1
                    cv2.rectangle(frame, (15, 15), (300, 470), (12, 180, 12), 5)
                else: pass
            else:
                if not mascara_verde:
                    #print("zona 1 hay cafe bueno")
                    encendidos[1] = 1
                    cv2.rectangle(frame, (330, 15), (630, 470), (12, 180, 12), 5)
                else: pass



camara= 0 # 0 camara portatil, 1 webcam
video = cv2.VideoCapture(camara)

while True:
    ret, frame = video.read()
    if not ret: break
    # crear una mascara del color que se quiera tener
    start_time = time.time()
    framelab = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask1 = cv2.inRange(framelab, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(framelab, lower_red2, upper_red2)
    mascara = cv2.add(red_mask1, red_mask2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mascara_roja = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    #result = cv2.bitwise_and(frame, frame, mask=mascara)



    mascara_verde = cv2.inRange(framelab, lower_green, upper_green)
    mascara_verde = cv2.morphologyEx(mascara_verde, cv2.MORPH_OPEN, kernel)

    find_contours(mascara_verde,'g')
    find_contours(mascara_roja,'r')

    serial_msg = ''.join(str(i) for i in encendidos)
    serial_msg+="\n"
    #print(serial_msg + " ******")
    serialArduino.write(serial_msg.encode('utf-8'))
    data = serialArduino.readline()
    #print(data)

    final_time = time.time()-start_time
    #print("Tiempo x foto: ",final_time)
    #cv2.line(frame, (0, 240), (640, 240), (80, 80, 80), 3)
    #cv2.line(frame, (213, 0), (213, 480), (80, 80, 80), 3)
    cv2.line(frame, (320, 0), (320, 480), (80, 80, 80), 3)
    print(encendidos)
    cv2.imshow("mascara roja", mascara)
    cv2.imshow("mascara verde", mascara_verde)
    cv2.imshow("Stream", frame)
    encendidos = [0]*6
    # val_led = 0
    # cad = str(val_led) + "," + str(mot_led)
    # serialArduino.write(cad.encode('ascii'))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # For que encuentra el promedio especifico de un canal de color ej([i,:,0]-> H o L,[i,:,1]-> S o A)
    #print(framelab.shape)
    #for i in range(480):
        ###for j in range(640):
        ##print(framelab[i,:,1])
        #print("H val: ", sum(framelab[i, :, 0]) / 640)
        #print("S val: ", sum(framelab[i, :, 1]) / 640)
        #print("V val: ", sum(framelab[i, :, 2]) / 640)

video.release()
cv2.destroyAllWindows()

'''
TODO:

crear metodo dibujar contornos para color rojo y verde. 
Crear metodo que compare tamaño de


primero analizo si hay verde en la seccion, si hay -> Cuadro rojo, pasar a siguiente frame (no hay necesidad de analizar rojo porque ya es cafe malo)

Condicionales con 6 áreas de selección

            if y < 240:
                if x <= 213:
                    if not mascara_verde:
                        #print("zona 1 hay cafe bueno")
                        encendidos[0] = 1
                        cv2.rectangle(frame, (15, 15), (200, 230), (12, 180, 12), 5)
                    else: pass
                elif 213 < x < 426:
                    if not mascara_verde:
                        #print("zona 2 hay cafe bueno")
                        encendidos[1] = 1
                        cv2.rectangle(frame, (220, 15), (410, 230), (12, 180, 12), 5)
                    else: pass
                elif 426 < x < 639:
                    if not mascara_verde:
                        #print("zona 3 hay cafe bueno")
                        encendidos[2] = 1
                        cv2.rectangle(frame, (430, 15), (630, 230), (12, 180, 12), 5)
                    else: pass
            elif y >= 240:
                if x <= 213:
                    if not mascara_verde:
                        #print("zona 6 hay cafe bueno")
                        encendidos[5] = 1
                        cv2.rectangle(frame, (15, 255), (200, 470), (12, 180, 12), 5)
                    else: pass
                elif 213 < x < 426:
                    if not mascara_verde:
                        #print("zona 5 hay cafe bueno")
                        encendidos[4] = 1
                        cv2.rectangle(frame, (220, 255), (410, 470), (12, 180, 12), 5)
                    else: pass
                elif 426 < x < 639:
                    if not mascara_verde:
                        #print("zona 4 hay cafe bueno")
                        encendidos[3] = 1
                        cv2.rectangle(frame, (430, 255), (630, 470), (12, 180, 12), 5)
                    else: pass

'''
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
        if area > 2500:
            M = cv2.moments(c)
            if M["m00"] == 0: M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            cv2.circle(frame, (x, y), 6, (250, 50, 50), -1)

            nuevo_contorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevo_contorno], 0, (255, 0, 0), 3)

            if y < 240:
                if x <= 213:
                    #if mascara_verde: pass
                    #print("zona 1 hay cafe bueno")
                    encendidos[0] = 1
                    cv2.rectangle(frame, (15, 15), (200, 230), (12, 180, 12), 5)
                elif 213 < x < 426:
                    #if mascara_verde: pass
                    #print("zona 2 hay cafe bueno")
                    encendidos[1] = 1
                    cv2.rectangle(frame, (220, 15), (410, 230), (12, 180, 12), 5)
                elif 426 < x < 639:
                    #if mascara_verde: pass
                    #print("zona 3 hay cafe bueno")
                    encendidos[2] = 1
                    cv2.rectangle(frame, (430, 15), (630, 230), (12, 180, 12), 5)
            elif y >= 240:
                if x <= 213:
                    if mascara_verde: pass
                    #print("zona 6 hay cafe bueno")
                    encendidos[5] = 1
                    cv2.rectangle(frame, (15, 255), (200, 470), (12, 180, 12), 5)
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




#lower_red = np.array([80, 120, 110])# lab
#upper_red = np.array([110, 180, 150])
video = cv2.VideoCapture(0)
# if video.isOpened():
#   video.release()


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
    '''
    # Find contours tiene 3 entradas, imagen, contorno y jerarquia
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    # Dibujar contorno para objetos mayores a cierta area
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 2500:
            M = cv2.moments(c)
            if M["m00"] == 0: M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame, (x, y), 6, (250, 50, 50), -1)


            nuevo_contorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevo_contorno], 0, (255, 0, 0), 3)

            if y < 240:
                if x <= 213:
                    print("zona 1 hay cafe bueno")
                    cv2.rectangle(frame, (15, 15), (200, 230), (12, 180, 12), 5)
                elif 213<x<426:
                    print("zona 2 hay cafe bueno")
                    cv2.rectangle(frame, (220, 15), (410, 230), (12, 180, 12), 5)
                elif 426<x<639:
                    print("zona 3 hay cafe bueno")
                    cv2.rectangle(frame, (430, 15), (630, 230), (12, 180, 12), 5)
            elif y >= 240:
                if x <= 213:
                    print("zona 4 hay cafe bueno")
                    cv2.rectangle(frame, (15, 255), (200, 470), (12, 180, 12), 5)
                elif 213 < x < 426:
                    print("zona 5 hay cafe bueno")
                    cv2.rectangle(frame, (220, 255), (410, 470), (12, 180, 12), 5)
                elif 426 < x < 639:
                    print("zona 6 hay cafe bueno")
                    cv2.rectangle(frame, (430, 255), (630, 470), (12, 180, 12), 5)
            
        
            #print('Area: ',area)
            val_led = 1
            #serialArduino.write(bytes(str(val_led), 'utf-8'))
    '''
    serial_msg = ''.join(str(i) for i in encendidos)
    serial_msg+="\n"
    print(serial_msg + " ******")
    serialArduino.write(serial_msg.encode('utf-8'))
    data = serialArduino.readline()
    print(data)

    final_time = time.time()-start_time
    #print(encendidos)
    #print("Tiempo x foto: ",final_time)
    cv2.line(frame, (0, 240), (640, 240), (80, 80, 80), 3)
    cv2.line(frame, (213, 0), (213, 480), (80, 80, 80), 3)
    cv2.line(frame, (426, 0), (426, 480), (80, 80, 80), 3)
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
#serialArduino.write(bytes(str(2), 'utf-8'))
#data = serialArduino.readline()
#print(data, val_led)
# serialArduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

# Estructura para mandar algo a arduino:
# 1. Crear un string que tenga: val_led = str(pin que se quiera)+ ','+ str(valor que se quiera tener en arduino)
#  serialArduino.write(bytes(str(val_led), 'utf-8'))
#  data = serialArduino.readline()
#  print(data, val_led)
'''
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


while True:
    num = input("Enter a number: ")  # Taking input from user
    value = write_read(num)
    print(value)  # print
'''

'''a = 0
while a < 9:
    if val_led != 0:
        val_led = 0
        cad = str(val_led)
        serialArduino.write(bytes(str(val_led), 'utf-8'))
        time.sleep(1.0)
        data = serialArduino.readline()
        print("if", data)
    else:
        val_led = 1
        cad = str(val_led)
        serialArduino.write(bytes(str(val_led), 'utf-8'))
        time.sleep(1.0)
        data = serialArduino.readline()
        print('else', data)
    a += 1

'''





'''
TODO:

crear metodo dibujar contornos para color rojo y verde. 
Crear metodo que compare tamaño de


primero analizo si hay verde en la seccion, si hay -> Cuadro rojo, pasar a siguiente frame (no hay necesidad de analizar rojo porque ya es cafe malo)
'''
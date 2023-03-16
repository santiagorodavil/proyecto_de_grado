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
pin_cafeBueno = 5
pin_cafeMalo = 6
val_led = 2
mot_led = 0

#serialArduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

# Mascara de color rojo (Las necesarias papra el cafe)
lower_red = np.array([80, 100, 100])# HS
upper_red = np.array([180, 150, 200])
#lower_red = np.array([80, 120, 110])# lab
#upper_red = np.array([150, 180, 150])
video = cv2.VideoCapture(0)
# if video.isOpened():
#   video.release()


while True:
    ret, frame = video.read()
    if not ret: break
    # crear una mascara del color que se quiera tener
    start_time = time.time()
    framelab = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(framelab, lower_red, upper_red)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    result = cv2.bitwise_and(frame, frame, mask=mascara)

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
            print('Area: ',area)
            val_led = 1
            #serialArduino.write(bytes(str(val_led), 'utf-8'))

    #serialArduino.write(bytes(str(val_led), 'utf-8'))
    #data = serialArduino.readline()
    #print(data, val_led)
    final_time = time.time()-start_time
    #print("Tiempo x foto: ",final_time)
    cv2.line(frame, (0, 240), (640, 240), (80, 80, 80), 3)
    cv2.line(frame, (213, 0), (213, 480), (80, 80, 80), 3)
    cv2.line(frame, (426, 0), (426, 480), (80, 80, 80), 3)
    cv2.imshow("mascara", mascara)
    cv2.imshow("Stream", frame)
    val_led = 0
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

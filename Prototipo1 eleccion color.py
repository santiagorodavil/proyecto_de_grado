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
lower_red = np.array([0, 120, 0])
upper_red = np.array([100, 200, 150])
#lower_red = np.array([80, 100, 110])
#upper_red = np.array([100, 160, 200])
video = cv2.VideoCapture(0)
# if video.isOpened():
#   video.release()


while True:
    ret, frame = video.read()
    if ret:
        # crear una mascara del color que se quiera tener
        framelab = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(framelab, lower_red, upper_red)
        start_time = time.time()
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        #mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
        #result = cv2.bitwise_and(frame, frame, mask=mascara)

        # Find contours tiene 3 entradas, imagen, contorno y jerarquia
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contorno para objetos mayores a cierta area
        for c in contornos:
            area = cv2.contourArea(c)
            if area > 5000:
                cv2.drawContours(frame, [c], 0, (255, 0, 0), 3)
                #print("Entra a bueno")
                val_led = 1
                #serialArduino.write(bytes(str(val_led), 'utf-8'))

        #serialArduino.write(bytes(str(val_led), 'utf-8'))
        #data = serialArduino.readline()
        #print(data, val_led)
        final_time = time.time()-start_time
        print("Tiempo x foto: ",final_time)
        cv2.imshow("mascara", mascara)
        cv2.imshow("Stream", frame)
        val_led = 0
        # val_led = 0
        # cad = str(val_led) + "," + str(mot_led)
        # serialArduino.write(cad.encode('ascii'))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #print(framelab.shape)
        #for i in range(480):
            ##for j in range(640):
            #print(framelab[i,:,1])
            #print(sum(framelab[i,:,2])/640)

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

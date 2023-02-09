import cv2
import numpy as np
import os


'''
# Muestra bordes con la cámara 
vid = cv2.VideoCapture(0)
while True:
    ret, frame = vid.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_frame, 50, 150)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Canny Edges After Contouring', edges)
    cv2.imshow("bordes", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
'''

GENERAL_PATH = os.getcwd()
img = cv2.imread(GENERAL_PATH+"/Dataset/cafe_maloEI/DSCN0PINTON3.JPG")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def sobel_filter(img):
    # Apply the Sobel filter to get the gradient magnitude
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

    # Calculate the gradient magnitude and direction
    abs_sobelx = cv2.convertScaleAbs(sobelx)
    abs_sobely = cv2.convertScaleAbs(sobely)

    # # Calculate the gradient magnitude
    #grad_magnitude = np.sqrt(np.square(sobelx) + np.square(sobely))
    #grad_magnitude = (grad_magnitude / np.max(grad_magnitude)) * 255
    #grad_magnitude = grad_magnitude.astype(np.uint8)

    gradient_magnitude = cv2.addWeighted(np.abs(sobelx), 0.5, np.abs(sobely), 0.5, 0)

    # Threshold the gradient magnitude to get the edges
    _, thresholded = cv2.threshold(cv2.convertScaleAbs(gradient_magnitude), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresholded
# implementation canny edge
blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)
# edges = cv2.Canny(blurred, 30, 100)
threshold = sobel_filter(gray_img)
# contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#edges = cv2.resize(edges, (800, 600))
#cv2.imshow('Canny Edges After Contouring', edges)
#cv2.waitKey(0)
print("Number of Contours found = " + str(len(contours)))
for c in contours:
    area = cv2.contourArea(c)
    if area > 3500:
        cv2.drawContours(img, [c], -1, (0, 255, 0), 5)


# Draw all contours
# -1 signifies drawing all contours
#cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 3)
#cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

'''
---------------------------------------------------------
# Mascara de color rojo (Las necesarias papra el cafe)
#lim_low_color = np.array([150, 100, 20], np.uint8)
lim_low_color = np.array([0, 0, 0], np.uint8)
lim_upp_color = np.array([180, 255, 40], np.uint8)
#lim_upp_color = np.array([180, 255, 255], np.uint8)
frameHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mascara = cv2.inRange(frameHSV, lim_low_color, lim_upp_color)
contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
for c in contornos:
    area = cv2.contourArea(c)
    if area > 5000:
        cv2.drawContours(img, [c], 0, (255, 0, 0), 3)
        print("Entra a bueno")

h, w, c = img.shape
print(h,w,c)
-----------------------------------------------------------
'''
# cv2.imshow("mascara", mascara)
img = cv2.resize(img, (800, 600))
cv2.imshow("prueba", img)
cv2.waitKey(0)
cv2.destroyAllWindows()




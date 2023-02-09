import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
from skimage.feature import local_binary_pattern
from sklearn.preprocessing import normalize

import os

# Load image
GENERAL_PATH = os.getcwd()
image = io.imread(GENERAL_PATH+"/Dataset/cafe_buenoEI/DSCN0404.JPG")
#cafe_bueno_path = io.imread("Dataset/cafe_buenoEI/DSCN0400.JPG")

# Convert to grayscale
image_gray = color.rgb2gray(image)

# Apply LBP
radius = 8
n_points = 2 * radius
lbp = local_binary_pattern(image_gray, n_points, radius, method='uniform')

#border_mean= mean__(lbp,2270,2320,1180,1205)
#print("border mean: ", border_mean)
#other_mean = mean__(lbp,900,950,1750,1775)
#print("Other mean: ", other_mean)


# Create the histogram of the LBP features
#hist, _ = np.histogram(lbp, bins=59, range=(0,20))
#hist = normalize(hist.reshape(1, -1), norm='l1').flatten()
#plt.bar(range(59),hist)
#plt.title("Histograma cafe bueno")
# Plot LBP image
plt.imshow(lbp, cmap='gray')
plt.show()
'''
---
def mean__(lbp,x1,x2,y1,y2):
    mean = 0
    for i in range(x1,x2):
        #print(lbp[i,0])
        for j in range(y1,y2):
            #print(lbp[i,j])
            mean += lbp[i,j]
    return mean/((x2-x1)*(y2-y1))
---

# Load an image
image = cv2.imread(GENERAL_PATH+"/Dataset/cafe_maloEI/DSCN0VERDE3.JPG")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Calculate the LBP features
lbp = feature.local_binary_pattern(gray, 8, 2)

# Create the histogram of the LBP features
hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, lbp.max() + 1), range=(0, lbp.max()))

# Plot the histogram
plt.hist(hist, bins=np.arange(0, lbp.max() + 1))
plt.show()
cv2.imshow("frame", lbp)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


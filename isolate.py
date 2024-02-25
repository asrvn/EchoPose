import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np

BGcolor = (255, 255, 255)
ksize = (5, 5)

img = cv2.imread('input_img.jpg')

noBG = SelfiSegmentation().removeBG(img, BGcolor, 0.50)

parse = cv2.GaussianBlur(cv2.cvtColor(noBG, cv2.COLOR_BGR2GRAY), ksize, 0)

upperThresholdMask, lowThresholdMask = cv2.threshold(parse, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
lowThresholdMask = 0.5 * upperThresholdMask

# canny
canny = cv2.Canny(noBG, lowThresholdMask, upperThresholdMask)
pts = np.argwhere(canny > 0)

y1, x1 = pts.min(axis = 0)
y2, x2 = pts.max(axis = 0)

output = noBG[y1 : y2, x1 : x2]
cv2.imshow("out.jpg", output)

cv2.waitKey(0)
cv2.destroyAllWindows()
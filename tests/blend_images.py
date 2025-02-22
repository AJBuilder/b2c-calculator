from tkinter import filedialog
import os
import cv2
import numpy as np

images = []
print("Select images to blend. (Must all be of same size)")
paths = filedialog.askopenfilenames()
if not paths:
    exit()
for path in paths:
    images.append(cv2.imread(path))
    
weight = 1/len(images)
blended = np.uint8()
for i, img in zip(range(len(images)), images):
    weighted = np.uint8(img * weight)
    blended = blended + weighted
    cv2.imshow(f"weighted{i}", weighted)
    
    
cv2.imshow("Blended", blended)
cv2.waitKey(0)
filename = filedialog.asksaveasfilename() + '.png'
cv2.imwrite(filename, blended)
print("Saved to " + filename)

    

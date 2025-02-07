from cgitb import grey
import cv2
import matplotlib.pyplot as plt

# Load image
original_img = cv2.imread('captcha_image.png')
img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

# Apply different thresholding
_, global_thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
adaptive_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
otsu_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Show results
titles = ['Original Image','greyScale', 'Global Thresholding', 'Adaptive Mean', "Otsu's Thresholding"]
images = [original_img,img, global_thresh, adaptive_mean, otsu_thresh]

for i in range(len(images)):
    plt.subplot(2, 3, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.axis('off')

plt.show()

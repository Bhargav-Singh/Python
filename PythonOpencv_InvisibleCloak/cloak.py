import cv2
import numpy as np

video = cv2.VideoCapture(0)
background = 0

for i in range(30):
    ret, background = video.read()

# save a background image refrence
background = np.flip(background, axis= 1)

while True:
  # Save video feed
  ret, imgx = video.read()
  
  # Flip Image Frame If necessary
  img = cv2.flip(imgx, 1)

  # Convert the image frame into HSV from BGR
  hsv = cv2.cvtColor(imgx, cv2.COLOR_BGR2HSV)

  # Remove random noise. Here we use GaussianBlur
  blur = cv2.GaussianBlur(hsv, (35, 3), 0)
  
#  Define lower and upper hsv value for cloak color
# NOTE: Here I used red shaded cloath for cloak.
#  You can use any colored cloath. The Uppper and lower value is set accordingly
  lower = np.array([0, 111, 86 ])
  upper = np.array([3, 240, 255])
  
# create mask from the above ranges. This will detect the area where hsv lies in range
# This mask will detect the cloak area
  mask01 = cv2.inRange(hsv, lower, upper)
  mask01 = cv2.flip(mask01, 1)

# The below cade is for detect the white area maskedd by mask01
  lower_red = np.array([170, 50, 50])
  upper_red = np.array([180, 255, 255])

  mask02 = cv2.inRange(hsv, lower_red, upper_red)
  mask02 = cv2.flip(mask02, 1)

# Adding both mask to create finnal masking
  mask = mask01 + mask02

# morphologycal transformation to unit8
  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

# showing the background image pixels in the area of mask
  img[np.where(mask == 255)] = background[np.where(mask==255)]

  cv2.imshow("Display", img)
#   cv2.resizeWindow('Display', 1080,2000)
#   cv2.imshow("Background", background)
#   cv2.imshow("mask01", mask01)
#   cv2.imshow("mask02", mask02)

  k =cv2.waitKey(1)
  if k == ord('q'):
    break
video.release()
cv2.destroyAllWindows()

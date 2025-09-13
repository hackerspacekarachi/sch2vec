import cv2, os, time
import numpy as np
import mss
import numpy as np
from PIL import Image, ImageGrab
from collections import Counter
import pyautogui, platform

def remove_background(image):
    
    # If the image doesn't have an alpha channel, add one
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Get the RGB values (ignoring the alpha channel if present)
    rgb_data = image[:, :, :3]
    
    # Reshape the data to a list of pixels
    pixels = rgb_data.reshape(-1, 3)
    
    # Find the most common color
    most_common_color = Counter(map(tuple, pixels)).most_common(1)[0][0]
    
    # Create a mask for the most common color
    mask = np.all(rgb_data == most_common_color, axis=-1)
    
    # Set the alpha channel to 0 (transparent) where the mask is True
    image[mask, 3] = 0
    
    # Save the image with transparency
    cv2.imwrite("Capture.png", image)
    
    os_name = platform.system().lower()
        
    if os_name == 'windows':
        import subprocess

        subprocess.Popen('explorer "{}"'.format(os.getcwd()))
        time.sleep(2)

        pyautogui.press('c')
        # time.sleep(1)

        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('alt', 'f4')


sct = ImageGrab.grab()
img = np.array(sct) # BGR Image
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Create point matrix get coordinates of mouse click on image
point_matrix = np.zeros((2,2),np.int32)
 
counter = 0
def mousePoints(event,x,y,flags,params):
    global counter
    # Left button mouse click event opencv
    if event == cv2.EVENT_LBUTTONDOWN:
        point_matrix[counter] = x,y
        counter = counter + 1


a = 1
 
while True:
    for x in range (0,2):
        cv2.circle(img,(point_matrix[x][0],point_matrix[x][1]),3,(0,255,0),cv2.FILLED)
 
    if counter == 2:
        starting_x, ending_x = sorted((point_matrix[0][0], point_matrix[1][0]))
        starting_y, ending_y = sorted((point_matrix[0][1], point_matrix[1][1]))

        # Cropping image
        img_cropped = img[starting_y:ending_y, starting_x:ending_x]

        remove_background(img_cropped)
        
        # Reset
        a=0
        break
 
    # Return original image
    cv2.namedWindow("Sch2Vec", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Sch2Vec", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Screenshot", img)

    # Mouse click event on original image
    cv2.setMouseCallback("Screenshot", mousePoints)
    # Printing updated point matrix
    print(point_matrix)
    # Refreshing window all time
    cv2.waitKey(a)
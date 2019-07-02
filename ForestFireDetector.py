import cv2 
import numpy as np
from matplotlib import pyplot as plt
from decimal import *

def skyformulaRGB(th,fimg): #calculates every pixel and sets white which has potential to be a pixel in the sky. others sets to black. 
	for x in range(800):    #roam every pixel
		for y in range(400):
			r = fimg[y,x,2] #2:red
			g = fimg[y,x,1] #1:green
			b = fimg[y,x,0] #0:blue
			formul = 1*(int(r))+0.1*(int(g))+0.9*(int(b)) #give a value to each pixel respecting to a special formula
			#bigger th (threshold) value , generally more black pixels. bigger value=has more possibility to be a sky pixel. 
			if ( formul > th ): #sky
				fimg.itemset((y,x,2),255) #if its resulted as a sky pixel, set every channel value to 255 (white)
				fimg.itemset((y,x,1),255) #0:blue , 1:green, 2:red
				fimg.itemset((y,x,0),255)
			else:               #ground
				fimg.itemset((y,x,2),0) #if its resulted as a ground pixel, set every channel value to 0 (black)
				fimg.itemset((y,x,1),0) #0:blue , 1:green, 2:red
				fimg.itemset((y,x,0),0)
				
	return fimg	#return modified image	
#________________________________________MAIN________________________________________

calibration_img = cv2.imread('forest1.png') #a regular(non-fire) image at noon time of area for calibration
check_img = cv2.imread('forest1fire1.png')  #fire or smoke check image 

#				   cols(width),rows(height)
res_img = cv2.resize(calibration_img, (800, 400)) #resized image for plotting
img = cv2.resize(calibration_img, (800, 400))     #actual image to work on it
skyExamination = cv2.resize(check_img, (800, 400))    
groundExamination = cv2.resize(check_img, (800, 400))
#print (img.shape)

#(threshold value,input image)				
fimg = skyformulaRGB(120,img) #bigger value,more black pixels.

kernel = np.ones((5,5),np.uint8) #set kernel matrix size
#**********SKY EXAMINATION (Disable Ground)**********
eroted = cv2.erode(fimg,kernel,iterations = 15) #erote image to get rid of unwanted empty spaces
for x in range(800):   #roam every pixel
		for y in range(400):
			if(eroted[y,x,0]==0):
				skyExamination.itemset((y,x,2),255) #0:blue , 1:green, 2:red
				skyExamination.itemset((y,x,1),255)
				skyExamination.itemset((y,x,0),255)
				
hsvSky = cv2.cvtColor(skyExamination, cv2.COLOR_BGR2HSV)
lowerS = [0, 0, 2]      #lower hsv limit (hue,saturation,value)
upperS = [180, 20, 180] #upper hsv limit
lowerS = np.array(lowerS, dtype="uint8")
upperS = np.array(upperS, dtype="uint8")
smoke = cv2.inRange(hsvSky, lowerS, upperS) #set to white all smoke pixels

for x in range(800): #set to black all ground pixels
		for y in range(400):
			if(eroted[y,x,0]==0):
				smoke[y,x] = 0

#**********GROUND EXAMINATION (Disable Sky)**********
dilated = cv2.dilate(eroted,kernel,iterations = 20) 
for x in range(800):   #roam every pixel
		for y in range(400):
			if(dilated[y,x,0]==255):
				groundExamination.itemset((y,x,2),0) #0:blue , 1:green, 2:red
				groundExamination.itemset((y,x,1),0)
				groundExamination.itemset((y,x,0),0)
				
hsvGround = cv2.cvtColor(groundExamination, cv2.COLOR_BGR2HSV)
lowerG = [0, 150, 50]   #lower hsv limit (hue,saturation,value) 18
upperG = [20, 255, 255] #upper hsv limit 35
lowerG = np.array(lowerG, dtype="uint8")
upperG = np.array(upperG, dtype="uint8")
fire = cv2.inRange(hsvGround, lowerG, upperG)


#**********EXAMİNATION RESULTS**********
#*****SKY(Smoke)*****

sWhite = 0
for x in range(800):   #roam every pixel,search for white pixels (which indicates smoke)
		for y in range(400):
			if(smoke[y,x]==255):
				sWhite += 1
				
smokeRate = sWhite/320000 #400*800 = 320000
print("Smoke ratio: ",smokeRate)
if(smokeRate >0.1):
	print('(Smoke)Possible Fire Thread!')

#*****GROUND(Fire)*****
gWhite = 0
for x in range(800):   #roam every pixel,search for white pixels (which indicates fire)
		for y in range(400):
			if(fire[y,x]==255):
				gWhite += 1
				
fireRate = gWhite/320000 #400*800 = 320000
print("Fire ratio: ",fireRate)
if(fireRate >0.1):
	print('(Flame)Possible Fire Thread!')





#**********PLOT**********
titles = ['Calibration Image','Masked w/skyformula','Masked+Eroted','Sky Examination','Smoke(Sky)','Masked+Eroted+Dilated','Ground Examination','Fire(Ground)']
images = [res_img,fimg,eroted,skyExamination,smoke,dilated,groundExamination,fire]
for i in range(8):
    plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

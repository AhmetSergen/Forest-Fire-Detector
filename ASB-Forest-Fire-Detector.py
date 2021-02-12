# ASB #

import cv2 
import numpy as np
from matplotlib import pyplot as plt
from decimal import *

#////////////////////Settings\\\\\\\\\\\\\\\\\\\\
# A regular(non-fire) image at noon time of area for calibration:
calibrationImageURL = "forest1.png"
# Fire or smoke check image:
checkImageURL = "forest1burn1.png"

smokeThreshold = 0.08 	# Recommended value is around ~0.1 | ~0.08 
fireThreshold = 0.1		# Recommended value is around ~0.1 | ~0.08

resizeImageWidth = 800	# Recommended value is 800
resizeImageHeight = 400	# Recommended value is 400

showPlot = True
#\\\\\\\\\\\\\\\\\\\\Settings////////////////////

print("\n########## ASB Forest Fire Detector ##########\n")
print("Calibration Image URL=",calibrationImageURL)
print("Check Image URL=",checkImageURL)

def skyFormulaRGB(threshold, inputImg, inputImgWidth, inputImgHeight): #calculates every pixel and sets white which has potential to be a pixel in the sky. others sets to black. 
	for x in range(inputImgWidth):    #roam every pixel
		for y in range(inputImgHeight):
			r = inputImg[y,x,2] #2:red
			g = inputImg[y,x,1] #1:green
			b = inputImg[y,x,0] #0:blue
			formula = 1*(int(r))+0.1*(int(g))+0.9*(int(b)) #give a value to each pixel respecting to a special formula
			#bigger threshold (threshold) value , generally more black pixels. bigger value=has more possibility to be a sky pixel. 
			if ( formula > threshold ): #sky
				inputImg.itemset((y,x,2),255) #if its resulted as a sky pixel, set every channel value to 255 (white)
				inputImg.itemset((y,x,1),255) #0:blue , 1:green, 2:red
				inputImg.itemset((y,x,0),255)
			else:               #ground
				inputImg.itemset((y,x,2),0) #if its resulted as a ground pixel, set every channel value to 0 (black)
				inputImg.itemset((y,x,1),0) #0:blue , 1:green, 2:red
				inputImg.itemset((y,x,0),0)
				
	return inputImg	#return modified image	
#________________________________________MAIN________________________________________

calibrationImg = cv2.imread(calibrationImageURL) # A regular(non-fire) image at noon time of area for calibration
checkImg = cv2.imread(checkImageURL)  # Fire or smoke check image 

#				   cols(width),rows(height)
resizedPlotImgCalibration = cv2.resize(calibrationImg, (resizeImageWidth, resizeImageHeight)) #resized calibration image for plotting
resizedPlotImgCheck = cv2.resize(checkImg, (resizeImageWidth, resizeImageHeight)) #resized check image for plotting
img = cv2.resize(calibrationImg, (resizeImageWidth, resizeImageHeight))     #actual image to work on it
skyExamination = cv2.resize(checkImg, (resizeImageWidth, resizeImageHeight))    
groundExamination = cv2.resize(checkImg, (resizeImageWidth, resizeImageHeight))
#print (img.shape)

#(threshold value,input image)				
inputImg = skyFormulaRGB(120, img, resizeImageWidth, resizeImageHeight) #bigger value,more black pixels.

kernel = np.ones((5,5),np.uint8) #set kernel matrix size
#**********SKY EXAMINATION (Disable Ground)**********
eroted = cv2.erode(inputImg,kernel,iterations = 15) #erote image to get rid of unwanted empty spaces
for x in range(resizeImageWidth):   #roam every pixel
		for y in range(resizeImageHeight):
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

for x in range(resizeImageWidth): #set to black all ground pixels
		for y in range(resizeImageHeight):
			if(eroted[y,x,0]==0):
				smoke[y,x] = 0

#**********GROUND EXAMINATION (Disable Sky)**********
dilated = cv2.dilate(eroted,kernel,iterations = 20) 
for x in range(resizeImageWidth):   #roam every pixel
		for y in range(resizeImageHeight):
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
print("\n########## Examination Results ##########")
skyWhite = 0
for x in range(resizeImageWidth):   #roam every pixel,search for white pixels (which indicates smoke)
		for y in range(resizeImageHeight):
			if(smoke[y,x]==255):
				skyWhite += 1
				
smokeRate = skyWhite/320000 #400*800 = 320000
print("\nSmoke ratio: ",smokeRate)
if(smokeRate > smokeThreshold):
	print('Possible Fire Thread In The Sky!')
else:
	print("No Thread Detected In The Sky.")

#*****GROUND(Fire)*****
groundWhite = 0
for x in range(resizeImageWidth):   #roam every pixel,search for white pixels (which indicates fire)
		for y in range(resizeImageHeight):
			if(fire[y,x]==255):
				groundWhite += 1
				
fireRate = groundWhite/320000 #400*800 = 320000
print("\nFlame ratio: ",fireRate)
if(fireRate > fireThreshold):
	print('Possible Fire Thread On The Ground!')
else:
	print("No Thread Detected On The Ground.")




#**********PLOT**********
if(showPlot == True):
	titles = ['Calibration Image','Check Image','Masked w/skyformula','Sky Mask\n(Masked+Eroted)','Sky Examination','Smoke(Sky)','Ground Mask\n(Masked+Eroted+Dilated)','Ground Examination','Fire(Ground)']
	images = [resizedPlotImgCalibration, resizedPlotImgCheck, inputImg,eroted, skyExamination, smoke, dilated, groundExamination, fire]
	for i in range(9):
		plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()
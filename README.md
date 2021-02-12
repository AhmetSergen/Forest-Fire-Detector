# Forest-Fire-Detector
An algorithm that examines sky and ground to decide if theres a forest fire going on. This software uses OpenCV library with Python pragramming language.

## Description [TR]

### Default Scenario

In order to use this software properly, a camera that shoots forest with the skyline is in the center of the frame is required.<br>
When all hardware is installed, the camera takes a shot for calibration image in the morning time with a clear sky.<br>
The images that taken from this camera can be used as input check image in ASB-Forest-Fire-Detector.py to check if there is any fire thread exists.

### How It Works?

1. Resize calibration image.
2. Sky and ground seperates with a black-white mask in calibration image.
3. Using black and white pixel positions in mask image, sky and ground seperates in current check image for sky and ground examination.
4. Any smoke are searched with HSV values in sky examination.
5. Any fire is searched with HSV values in ground examination.
6. If smoke or fire detection rate is above the smokeThreshold or fireThreshold value, software warns user in examination results.

## Test Screen Shots

Test for a check image of forest with no fire and no smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test1.JPG" width="100%" alt="test1">

Test for a check image of forest with only fire.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test2.JPG" width="100%" alt="test2">

Test for a check image of forest with only smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test3.JPG" width="100%" alt="test3">

Test for a check image of forest with fire and smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test4.JPG" width="100%" alt="test4">

Test for another check image of forest with no fire and no smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test5.JPG" width="100%" alt="test5">

Test for another check image of forest with no fire and no smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test6.JPG" width="100%" alt="test6">

Test for another check image of forest with no fire and no smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test7.JPG" width="100%" alt="test7">

Test for another check image of forest with no fire and no smoke.
<img src="https://github.com/AhmetSergen/Forest-Fire-Detector/blob/master/test8.JPG" width="100%" alt="test8">

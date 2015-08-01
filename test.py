import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while( cap.isOpened() ):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor( frame , cv2.COLOR_BGR2GRAY )
	blur = cv2.GaussianBlur( gray , ( 5 , 5 ) , 0)
	ret1 , thresholdImage = cv2.threshold( blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU )
	# ret1 , thresholdImage = cv2.threshold( blur , 70 , 255 , cv2.THRESH_BINARY )

	# thresholdImage = cv2.adaptiveThreshold( blur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY , 11 , 2)
 
	# print thresholdImage

	# Display the resulting frame
	cv2.imshow( 'frame' , thresholdImage )
	if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
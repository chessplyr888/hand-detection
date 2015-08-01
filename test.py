import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while( cap.isOpened() ):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Set an arbitrary region of interest which happened to be an solid color
	frame = frame[ 25:200 , 0:300 ]

	# Our operations on the frame come here
	gray = cv2.cvtColor( frame , cv2.COLOR_BGR2GRAY )
	blur = cv2.GaussianBlur( gray , ( 5 , 5 ) , 0)
	ret1 , thresholdImage = cv2.threshold( blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU )

	image, contours, heirarchy = cv2.findContours( thresholdImage , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )

	# print contours

	cv2.drawContours( frame , contours , -1, ( 0 , 255 , 0 ) , 3 )
	# hull = cv2.convexHull( contours )


	# Display the resulting frame
	cv2.imshow( 'frame' , frame )
	if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
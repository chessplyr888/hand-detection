import numpy as np
import cv2


def getIndexOfLongestContour( contours ):
	maxLength = 0
	maxIndex = 0
	for i in range( 0 , len( contours ) ):
		length = len( contours[i] )
		# print length
		if length > maxLength:
			maxLength = length
			maxIndex = i
	return maxIndex


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

	image, contours, heirarchy = cv2.findContours( thresholdImage , cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE )


	maxIndex = getIndexOfLongestContour( contours )
	cnt = contours[maxIndex]


	cv2.drawContours( frame , contours , maxIndex , ( 0 , 255 , 0 ) , 3 )
	hull = cv2.convexHull( cnt , returnPoints = False )

	# print hull
	
	defects = cv2.convexityDefects( cnt , hull )
	# print defects

	for i in range( defects.shape[0] ):
	    s , e , f , d = defects[i , 0]
	    start = tuple( cnt[s][0] )
	    end = tuple( cnt[e][0] )
	    far = tuple( cnt[f][0] )
	    cv2.line( frame , start , end , [0 , 255 , 0] , 2 )
	    cv2.circle( frame , far , 5 , [0 , 0 , 255] , -1 )


	# Display the resulting frame
	cv2.imshow( 'frame' , frame )
	if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
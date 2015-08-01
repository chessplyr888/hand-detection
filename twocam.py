import numpy as np
import cv2

width = 640;
height = 480;

cap1 = cv2.VideoCapture( 0 )
cap2 = cv2.VideoCapture( 1 )


# Set camera resolutions to 640 * 480
cap1.set( 3 , width )
cap1.set( 4 , height )
cap2.set( 3 , width )
cap2.set( 4 , height ) 


while( cap1.isOpened() ):
	# Capture frame-by-frame
	ret1 , frame1 = cap1.read()
	ret2 , frame2 = cap2.read()


	# Convert camera feeds to grayscale
	cap1_gray = cv2.cvtColor( frame1 , cv2.COLOR_BGR2GRAY );
	cap2_gray = cv2.cvtColor( frame2 , cv2.COLOR_BGR2GRAY );


	# Gaussian blur on the 
	cap1_blur = cv2.GaussianBlur( cap1_gray , ( 5 , 5 ) , 0 )
	cap2_blur = cv2.GaussianBlur( cap2_gray , ( 5 , 5 ) , 0 )


	# Otsu thresholding both feeds
	cap1_ret1 , cap1_threshold = cv2.threshold( cap1_blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU )
	cap2_ret1 , cap2_threshold = cv2.threshold( cap2_blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU )

	# Our operations on the frame come here
	# gray = cv2.cvtColor( frame , cv2.COLOR_BGR2GRAY )
	# blur = cv2.GaussianBlur( gray , ( 5 , 5 ) , 0)
	# ret1 , thresholdImage = cv2.threshold( blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU )

	# thresholdImage = cv2.adaptiveThreshold( blur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY , 11 , 2)
 
	# print thresholdImage

	# Display the resulting frame
    
    # Displays the first camera feed
	cv2.namedWindow( 'frame1' , cv2.WINDOW_NORMAL )
	cv2.imshow( 'frame1' , cap1_threshold )
    
    # Displays the second camera feed
	cv2.namedWindow( 'frame2' , cv2.WINDOW_NORMAL )
	cv2.imshow( 'frame2' , cap2_threshold ) 
	if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
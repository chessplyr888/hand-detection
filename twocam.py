from __future__ import division
import math
from copy import deepcopy
import numpy as np
import cv2
from time import sleep

width = 640;
height = 480;


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


def getIndexofContourWithMostDefects( contours ):
	maxCount = 0
	maxIndex = 0
	for i in range( 0 , len( contours ) ):
		countGoodDefects = 0
		cnt = contours[i]
		hull = cv2.convexHull( cnt , returnPoints = False )
		defects = cv2.convexityDefects( cnt , hull )

		# print defects
		if defects is not None:
			# print "hi"
			for j in range( defects.shape[0] ):
				s , e , f , d = defects[j , 0]
				start = tuple( cnt[s][0] )
				end = tuple( cnt[e][0] )
				far = tuple( cnt[f][0] )
				angle = getAngle( start , far , end )
				if angle < 80:
					countGoodDefects = countGoodDefects + 1

		if countGoodDefects > maxCount:
			maxCount = countGoodDefects
			maxIndex = i

	# print maxIndex
	return maxIndex


def getDistance( point1 , point2 ):
	dist = ( ( point2[0] - point1[0] ) ** 2 + ( point2[1] - point1[1] ) ** 2 ) ** 0.5
	return dist


def getAngle( point1 , point2 , point3 ):
	line1 = getDistance( point2 , point1 )
	line2 = getDistance( point2 , point3 )
	dot = ( point1[0] - point2[0] ) * ( point3[0] - point2[0] ) + ( point1[1] - point2[1] ) * ( point3[1] - point2[1] )
	# print dot
	# print ( line1 * line2 )
	angle = math.acos( dot / ( line1 * line2 ) )
	angle = angle * 180 / math.pi
	return angle


def checkDuplicates( newPoint , points ):
	# print ""
	# print points
	# print newPoint
	# print ""
	for i in points:
		dist = getDistance( newPoint , i )
		# Set arbitrary distance to be 10 px
		if ( dist < 30 ):
			return True
	return False


def vectorFromPoints( point1 , point2 ):
	vector = []
	dx = point2[0] - point1[0]
	dy = point2[1] - point1[1]
	vector.append( dx )
	vector.append( dy )
	return vector


def linearCombination( vector1 , vector2 , point ):
	constants = []

	a11 = vector1[0]
	a12 = vector2[0]
	a13 = point[0]
	a21 = vector1[1]
	a22 = vector2[1]
	a23 = point[1]

	a = [[a11 , a12 , a13] , [a21 , a22 , a23]]

	a = [[a11 / vector1[0] , a12 / vector1[0] , a13 / vector1[0]] , [a21 / vector1[1] , a22 / vector1[1] , a13 / vector1[1]]]

	a = [[a11 , a12 , a13] , [a21 - a11 , a22 - a12 , a23 - a13]]

	temp = a22

	a = [[a11 , a12 , a13] , [a21 / temp , a22 / temp , a23 / temp]]

	temp = a21

	a = [[a11 - temp * a21 , a21 - temp * a22 , a31 - temp * a23] , [a21 , a22 , a23]]

	constants.push( a[0][2] )
	constants.push( a[1][2] )

	return constants


def setTopLeft( cap1_point , cap2_point ):
	cap1_topLeft = cap1_point
	cap2_topLeft = cap2_point

def setTopRight( cap1_point , cap2_point ):
	cap1_topRight = cap1_point
	cap2_topRight = cap2_point

def setBotRight( cap1_point , cap2_point ):
	cap1_botRight = cap1_point
	cap2_botRight = cap2_point
	
def setBotLeft( cap1_point , cap2_point ):
	cap1_botLeft = cap1_point
	cap2_botLeft = cap2_point



cap1_topLeft = None
cap1_topRight = None
cap1_topRight = None
cap1_botLeft = None

cap2_topLeft = None
cap2_topRight = None
cap2_topRight = None
cap2_botLeft = None




cap1 = cv2.VideoCapture( 0 )
cap2 = cv2.VideoCapture( 1 )


# Set camera resolutions to 640 * 480
cap1.set( 3 , width )
cap1.set( 4 , height )
cap2.set( 3 , width )
cap2.set( 4 , height ) 


firstTime = True
while( cap1.isOpened() and cap2.isOpened() ):
	# Sleep to allow both cameras to start up
	if firstTime:
		firstTime = False
		sleep(5)

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


	# Identify contours
	cap1_contours , cap1_hierarchy = cv2.findContours( cap1_threshold , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )
	cap2_contours , cap2_hirearchy = cv2.findContours( cap2_threshold , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )


	# Find the biggest contour
	maxIndex1 = getIndexOfLongestContour( cap1_contours )
	maxIndex2 = getIndexOfLongestContour( cap2_contours )
	cap1_cnt = cap1_contours[maxIndex1]
	cap2_cnt = cap2_contours[maxIndex2]


	# Draw the largest contour on frame
	cv2.drawContours( frame1 , cap1_contours , maxIndex1 , ( 0 , 255 , 0 ) , 3 )
	cv2.drawContours( frame2 , cap2_contours , maxIndex2 , ( 0 , 255 , 0 ) , 3 )


	# Get the convex hull
	cap1_hull = cv2.convexHull( cap1_cnt , returnPoints = False )
	cap2_hull = cv2.convexHull( cap2_cnt , returnPoints = False )


	# Find the convexity defects
	cap1_defects = cv2.convexityDefects( cap1_cnt , cap1_hull )
	cap2_defects = cv2.convexityDefects( cap2_cnt , cap2_hull )


	# Draw defects for camera 1
	cap1_goodDefects = []
	for i in range( cap1_defects.shape[0] ):
		s , e , f , d = cap1_defects[1 , 0]
		cap1_start = tuple( cap1_cnt[s][0] )
		cap1_end = tuple( cap1_cnt[e][0] )
		cap1_far = tuple( cap1_cnt[f][0] )

		angle = getAngle( cap1_start , cap1_far , cap1_end )

		if angle < 80:
			cv2.line( frame1 , cap1_start , cap1_end , [0 , 255 , 0] , 2 )

			if len( cap1_goodDefects ) == 0:
				cap1_duplicateStart = False
				cap1_duplicateEnd = False
			else:
				cap1_duplicateStart = checkDuplicates( cap1_start , cap1_goodDefects )
				cap1_duplicateEnd = checkDuplicates( cap1_end , cap1_goodDefects )
				
			# cv2.circle( frame , far , 5 , [0 , 0 , 255] , -1 )
			if cap1_duplicateStart is False:
				cv2.circle( frame1 , cap1_start , 5 , [0 , 0 , 255] , -1 )
				cap1_goodDefects.append( cap1_start )
			if cap1_duplicateEnd is False:
				cv2.circle( frame1 , cap1_end , 5 , [0 , 0 , 255] , -1 )
				cap1_goodDefects.append( cap1_end )


	# Draw defects for camera 2
	cap2_goodDefects = []
	for i in range( cap2_defects.shape[0] ):
		s , e , f , d = cap2_defects[1 , 0]
		cap2_start = tuple( cap2_cnt[s][0] )
		cap2_end = tuple( cap2_cnt[e][0] )
		cap2_far = tuple( cap2_cnt[f][0] )

		angle = getAngle( cap2_start , cap2_far , cap2_end )

		if angle < 80:
			cv2.line( frame1 , cap2_start , cap2_end , [0 , 255 , 0] , 2 )

			if len( cap2_goodDefects ) == 0:
				cap2_duplicateStart = False
				cap2_duplicateEnd = False
			else:
				cap2_duplicateStart = checkDuplicates( cap2_start , cap2_goodDefects )
				cap2_duplicateEnd = checkDuplicates( cap2_end , cap2_goodDefects )
				
			# cv2.circle( frame , far , 5 , [0 , 0 , 255] , -1 )
			if cap2_duplicateStart is False:
				cv2.circle( frame2 , cap2_start , 5 , [0 , 0 , 255] , -1 )
				cap2_goodDefects.append( cap2_start )
			if cap2_duplicateEnd is False:
				cv2.circle( frame2 , cap2_end , 5 , [0 , 0 , 255] , -1 )
				cap2_goodDefects.append( cap2_end )
	
	
	# Displays the first camera feed
	cv2.namedWindow( 'frame1' , cv2.WINDOW_NORMAL )
	cv2.imshow( 'frame1' , frame1 )
	
	# Displays the second camera feed
	cv2.namedWindow( 'frame2' , cv2.WINDOW_NORMAL )
	cv2.imshow( 'frame2' , frame2 ) 
	if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
		break

# When everything done, release the capture
cap1.release()
cap2.release()
cv2.destroyAllWindows()


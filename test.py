from __future__ import division
import math
from copy import deepcopy
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


def getIndexofContourWithMostDefects( contours ):
	maxCount = 0
	maxIndex = 0
	for i in range( 0 , len( contours ) ):
		# countGoodDefects = 0
		cnt = contours[i]
		hull = cv2.convexHull( cnt , returnPoints = False )
		defects = cv2.convexityDefects( cnt , hull )

		# print defects
		goodDefects = []
		if defects is not None:
			# print "hi"
			for j in range( defects.shape[0] ):
				s , e , f , d = defects[j , 0]
				start = tuple( cnt[s][0] )
				end = tuple( cnt[e][0] )
				far = tuple( cnt[f][0] )
				angle = getAngle( start , far , end )
				if angle < 80:
					if len( goodDefects ) == 0:
						duplicateStart = False
						duplicateEnd = False
					else:
						duplicateStart = checkDuplicates( start , goodDefects )
						duplicateEnd = checkDuplicates( end , goodDefects )

					if duplicateStart is False:
						goodDefects.append( start )
					if duplicateEnd is False:
						goodDefects.append( end )

		if len( goodDefects ) > 0:
			goodDefects = removeOutliers( goodDefects )

		countGoodDefects = len( goodDefects )

		if countGoodDefects > maxCount:
			maxCount = countGoodDefects
			maxIndex = i

	# print maxIndex
	return maxIndex


def getAveragePoint( points ):
	count = len( points )
	# print count
	totalx = 0
	totaly = 0
	for i in points:
		totalx = totalx + i[0]
		totaly = totaly + i[1]

	newX = totalx // count
	newY = totaly // count

	point = []
	point.append( newX )
	point.append( newY )

	return point


def removeOutliers( points ):
	avgPoint = getAveragePoint( points )
	dist = []

	for i in points:
		distance = getDistance( avgPoint , i )
		dist.append( distance )


	totalDist = 0
	for i in dist:
		totalDist = totalDist + i
	avgDist = totalDist / len( dist )

	multiplier = 1.75
	newDist = avgDist * multiplier

	for i in points[:]:
		distance = getDistance( avgPoint , i )
		if distance > newDist:
			points.remove(i)

	return points


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
		if ( dist < 8 ):
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



def setTopLeft( point ):
	point_topLeft = point

def setTopRight( point ):
	point_topRight = point

def setBotRight( point ):
	point_botRight = point

def setBotLeft( point ):
	point_botLeft - point



point_topLeft = None 
point_topRight = None
point_botRight = None
point_botLeft = None



cap = cv2.VideoCapture(0)

while( cap.isOpened() ):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# frame = deepcopy( frame )

	# Set an arbitrary region of interest which happened to be an solid color
	# frame = frame[ 25:200 , 0:300 ]

	# Our operations on the frame come here
	gray = cv2.cvtColor( frame , cv2.COLOR_BGR2GRAY )
	blur = cv2.GaussianBlur( gray , ( 9 , 9 ) , 0)
	ret1 , thresholdImage = cv2.threshold( blur , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU )


	binThresh = deepcopy( thresholdImage )

	image, contours, heirarchy = cv2.findContours( thresholdImage , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )


	maxIndex = getIndexofContourWithMostDefects( contours )
	cnt = contours[maxIndex]


	cv2.drawContours( frame , contours , maxIndex , ( 0 , 255 , 0 ) , 3 )
	hull = cv2.convexHull( cnt , returnPoints = False )

	# print hull
	
	defects = cv2.convexityDefects( cnt , hull )
	# print defects

	goodDefects = []
	farpoints = []
	for i in range( defects.shape[0] ):
		s , e , f , d = defects[i , 0]
		start = tuple( cnt[s][0] )
		end = tuple( cnt[e][0] )
		far = tuple( cnt[f][0] )
		angle = getAngle( start , far , end )
		# print angle
		# print goodDefects
		if angle < 80:
			cv2.line( frame , start , end , [0 , 255 , 0] , 2 )

			if len( goodDefects ) == 0:
				duplicateStart = False
				duplicateEnd = False
			else:
				duplicateStart = checkDuplicates( start , goodDefects )
				duplicateEnd = checkDuplicates( end , goodDefects )
				
			# cv2.circle( frame , far , 5 , [0 , 0 , 255] , -1 )
			if duplicateStart is False:
				goodDefects.append( start )
				if not ( far[0] == 0 or far[0] == 640 or far[1] == 0 or far[1] == 480 ):
					cv2.circle( frame , start , 5 , [0 , 0 , 255] , -1 )
					farpoints.append( far )
			if duplicateEnd is False:
				goodDefects.append( end )
				if not( far[0] == 0 or far[0] == 640 or far[1] == 0 or far[1] == 480 ):
					cv2.circle( frame , end , 5 , [0 , 0 , 255] , -1 )
					farpoints.append( far )

	( x , y ) , radius = cv2.minEnclosingCircle( np.array( goodDefects ) )
	center = ( int( x ) , int( y ) )
	radius = int( radius )

	cv2.circle( frame , center , radius , [0 , 0 , 0] , 2)


	# Display the resulting frame
	cv2.imshow( 'frame' , frame )
	if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
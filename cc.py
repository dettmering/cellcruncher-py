#! /usr/bin/python

import csv
import sys
import math
import time

filename = sys.argv[1]

def readcsv( filename ):
	ifile  = open(filename, "rb")
	reader = csv.reader(ifile)
	
	rownum = 0	
	a = []

	for row in reader:
		a.append (row)
		rownum += 1
	ifile.close()
	
	return a

def createcolumnlist(a): # gets the name of the columns and creates dictionary with respective column numbers
	j = 0
	l = {}
	
	for x in a[0]:
		l[x] = j
		j += 1
	return l

def listSlices(a, column): # lists slices in experiment
	slice = 'FileName'	# need to skip first row
	slicelist = []
	
	for a in a:
		slice1 = a[column].split('_')[0]
		if slice != slice1:
			slice = slice1
			slicelist.append(slice1)
	return slicelist

def getValues(a, slice, column):	# gets the values for a given slice and row
	thevalues = []

	for a in a:
		if slice != 0:	# if slice = 0 then all values will be returned, irrespective of slice no
			if a[sliceinfo].split('_')[0] == slice:
				thevalues.append(a[column])
		else:
			thevalues.append(a[column])

	if slice == 0:	# removes column designation in case all values of a column are returned
		thevalues.pop(0)

	return thevalues

def getMetadata(a):
	thetime = time.asctime( time.localtime(time.time()) )	# local time
	thefolder = a[1][col['PathName_DAPI']]	# folder of images
	n = len(a) - 1	# -1 to account for column name
	
	nuclei = int(sum(getValues(a, 0, col['Count_Nuclei'])))
	timemanual = nuclei / 3	# estimation of counting time in seconds at a rate of 3 nuclei per s
	
	exectime = 0
	
	for i in col:	# calculates execution time of whole run in seconds
		if i.find('ExecutionTime') == 0:
			exectime += sum(getValues(a, 0, col[i]))
	
	x = [thetime, thefolder, n, nuclei, timemanual, exectime]
	return x

# MATH FUNCTIONS

def sum(array):
	n = 0
	y = [float(i) for i in array]

	n = math.fsum(y)	

	return n
	
def mean(array):
	i = len(array)
	y = sum(array)
	
	result = y / i
	
	return result
	
def stdev(array):
	n = int(len(array))
	m = float(mean(array))
	s = 0
	
	for x in array:
		y = float(x)
		sqdev = (y - m) * (y - m)
		s += sqdev
	
	if n > 1 :
		sigma = math.sqrt(s / (n - 1))
	else:
		sigma = 0

	return sigma

def sterr(array):
	n = int(len(array))
	sigma = stdev(array)
	
	ste = sigma / math.sqrt(n)
	
	return ste

# --------------------------------------------------------- .split('_')[0]

a = readcsv(filename)	# read file into array
col = createcolumnlist(a)	# creates dictionary with column positions

sliceinfo = col['FileName_DAPI']	# which column should be taken to parse the slice name?

slicelist = listSlices(a, sliceinfo)	# generate list of slices in file

meta = getMetadata(a)
print meta[0]
print meta[1]
print meta[2], 'Images'
print meta[3], 'Nuclei'
print 'at least', int((meta[4] / 3600)), 'hours of work saved by using CellProfiler'
print round((meta[5] / 3600),1), 'hours runtime of Pipeline'
print ''


print 'Slice\t','No Images\t','Nuclei\t', 'Green\t', 'Double\t', 'Red\t','PercentGreen\t', 'PercentRed\t', 'Mean_NucleiPic\t', 'Stdev_NucleiPic\t', 'Mean_ThreshGreen\t', 'Mean_ThreshRed\t'
for slicelist in slicelist:

	nuclei = getValues(a, slicelist, col['Count_Nuclei'])
	no = len(getValues(a, slicelist, col['Count_Nuclei']))
	green = getValues(a, slicelist, col['Count_FilteredGreen'])
	greenred = getValues(a, slicelist, col['Count_FilteredGreenRedDouble'])
	red = getValues(a, slicelist, col['Count_FilteredRed'])
	thresh_green = getValues(a, slicelist, col['Math_Math_Green'])
	thresh_red = getValues(a, slicelist, col['Math_Math_Red'])
	
	print slicelist,'\t',no,'\t',sum(nuclei),'\t',sum(green),'\t',sum(greenred),'\t',sum(red),'\t',round(((sum(green)-sum(greenred))/sum(nuclei)*100),2),'\t',round(((sum(red)-sum(greenred))/sum(nuclei)*100),2),'\t',round(mean(nuclei)),'\t',round(stdev(nuclei),2),'\t',round((mean(thresh_green) * 65536),1),'\t',round((mean(thresh_red) * 65536),1)

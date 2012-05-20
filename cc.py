#! /usr/bin/python
# CellProfiler analysis script by Till Dettmering, prinzipiell@gmail.com
# Please notify me if and how you use it.

import csv
import sys
import math
import time

def readcsv(filename):	# Reads csv file into an array which will then be used for all searches and calculations. Might be a problem with very large DefaultOut_Image.csv files, tested it with 100 MB
	ifile  = open(filename, "rb")
	reader = csv.reader(ifile)
	
	rownum = 0	
	a = []

	for row in reader:
		a.append (row)
		rownum += 1
	ifile.close()
	
	return a

def checkData(data, keywords):	# Searches string in Array by making one word out of the whole array. Very fast. Returns True if string is found.
	s = "\n".join(data)
	for k in keywords:
		if k in s:
			return True
	return False

def addUp(needle, haystack):	# adds up all values from certain columns, e.g. all starting with ModuleError
	result = 0
	
	for i in haystack:
		if i.find(needle) == 0:
			result += sum(getValues(a, 0, haystack[i]))
	return result

def createcolumnlist(a): # Creates dictionary with column names and respective column numbers. Facilitates using the script. col['<ColumnName'] returns number.
	j = 0
	l = {}
	
	for x in a[0]:
		l[x] = j
		j += 1
	return l

def listslides(a, column): # Creates list with all slides used in the experiment. Used later for whole-slide-operations. Assumes the file name to start with the slide name, followed by an underline: <slidename>_something.tif
	slide = 'FileName'	# need to skip first row
	slidelist = []
	
	for a in a:
		slide1 = a[column].split('_')[0]
		if slide != slide1:
			slide = slide1
			slidelist.append(slide1)
	return slidelist

def filterValues(a):	# If you specify a file with a list of images as a second command line argument, CellCruncher will analyze these images separately. 
	filterlist = readcsv(sys.argv[2]) 

	filtered = []
	rest = a[:]	# copies a, which will then be cleaned from the filtered images
	truecount = 0
	falsecount = len(a) - 1

	for j in filterlist:
		for i in a:
			if checkData(i, j) == True:
				filtered.append(i)
				rest.remove(i)
				truecount += 1
				falsecount -= 1	

	output = [filtered, rest]
	return output

def getValues(a, slide, column):	# Creates an array of all values for a given slide and a given column. 0 as a slide will return all values for a given column.
	thevalues = []

	for a in a:
		if slide != 0:	# if slide = 0 then all values will be returned, irrespective of slide no
			if a[slideinfo].split('_')[0] == slide:
				thevalues.append(a[column])
		else:
			thevalues.append(a[column])

	if slide == 0:	# removes column designation in case all values of a column are returned
		thevalues.pop(0)

	return thevalues

def getMetadata(a):	# retrieves some metadata from a
	thetime = time.asctime( time.localtime(time.time()) )	# local time
	thefolder = a[1][col['PathName_DAPI']]	# folder of images
	n = len(a) - 1	# Number of images; -1 to account for column name
	
	nuclei = int(sum(getValues(a, 0, col['Count_Nuclei'])))
	sumarea = n * area
	timemanual = nuclei / 3	# estimation of counting time in seconds at a rate of 3 nuclei per s
	exectime = addUp('ExecutionTime', col)
	errors = addUp('ModuleError', col)
	
	x = [thetime, thefolder, n, nuclei, timemanual, exectime, int(errors), sumarea]
	return x

def printResults(o, slidelist):		# Retrieves all the data and performs mathematical operations on it. CHANGE HERE FOR PERSONALIZED OUTPUT
	print 'Slide\t', 'No Images\t', 'Area (mm^2)\t', 'Nuclei\t', 'Green\t', 'Red\t', 'Double\t', 'PercentGreen\t', 'PercentRed\t', 'PercentDouble\t', 'Double/Green\t', 'Mean_NucleiPic\t', 'Stdev_NucleiPic\t', 'Mean_ThreshGreen\t', 'Mean_ThreshRed\t'

	for slidelist in slidelist:
		if len(getValues(o, slidelist, col['Count_Nuclei'])) > 0:	#only lists slide when nuclei > 0, for filtering!
			nuclei = getValues(o, slidelist, col['Count_Nuclei'])	# USAGE: your_result = getValues(o, slidelist, col['<desired_Column>']
			no = len(getValues(o, slidelist, col['Count_Nuclei']))
			green = getValues(o, slidelist, col['Count_FilteredGreen'])
			greenred = getValues(o, slidelist, col['Count_FilteredGreenRedDouble'])
			red = getValues(o, slidelist, col['Count_FilteredRed'])
			thresh_green = getValues(o, slidelist, col['Threshold_FinalThreshold_ThreshGreen'])
			thresh_red =  getValues(o, slidelist, col['Threshold_FinalThreshold_ThreshRed'])

			print slidelist,'\t',no,'\t',round((no * area),1),'\t',sum(nuclei),'\t',sum(green),'\t',sum(red),'\t',sum(greenred),'\t',round(((sum(green)-sum(greenred))/sum(nuclei)*100),2),'\t',round(((sum(red)-sum(greenred))/sum(nuclei)*100),2),'\t',round((sum(greenred)/sum(nuclei)*100),2),'\t',round((sum(greenred)/sum(green)*100),2),'\t',round(mean(nuclei),2),'\t',round(stdev(nuclei),2),'\t',round((mean(thresh_green) * 65536),1),'\t',round((mean(thresh_red) * 65536),1) # output to be printed. All maths are performed in this line. * 65536 to scale relative values to 16 bit grey values.

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
	
	if n > 1 :	# if n = 1 a division by zero error will occur
		sigma = math.sqrt(s / (n - 1))
	else:
		sigma = 0

	return sigma

def sem(array):
	n = int(len(array))
	sigma = stdev(array)
	
	sterr = sigma / math.sqrt(n)
	
	return sterr

def stdevnorm(x, y, dy, z, dz):	# normalization of stdev, when x = y/z
	wurzel = ((dy / y) * (dy / y)) + ((dz / z) * (dz / z))
	dx = x * math.sqrt(wurzel)
	
	return dx
	
# ---------------------------------------------------------

area = 635.34 * 474.57 / 1000000 # Area per image in mm^2 (Of course this is specific for the optical setup)
filename = sys.argv[1]

a = readcsv(filename)	# read file into array
col = createcolumnlist(a)	# creates dictionary with column positions
slideinfo = col['FileName_DAPI']	# which column should be taken to parse the slide name?
slidelist = listslides(a, slideinfo)	# generate list of slides in file

meta = getMetadata(a)
print meta[0]
print meta[1]
print meta[2], 'Images,',meta[6], 'Errors'
print meta[3], 'Nuclei,', round(meta[7],2), 'mm2 scanned'
print 'at least', int((meta[4] / 3600)), 'hours of work saved by using CellProfiler'
print round((meta[5] / 3600),1), 'hours runtime of Pipeline'
print ''

if len(sys.argv) == 3:	# if filtered list is given in command line...
	print 'FILTERED'
	printResults(filterValues(a)[0],slidelist)
	print ''
	print 'REST'
	printResults(filterValues(a)[1],slidelist)
else:
	printResults(a,slidelist)

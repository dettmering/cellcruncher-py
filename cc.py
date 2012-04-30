import csv
import sys
import math

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
		if a[sliceinfo].split('_')[0] == slice:
			thevalues.append(a[column])
	return thevalues

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
	
	sigma = math.sqrt(s / (n - 1))
	
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


print 'Slice\t','No Images\t','Nuclei\t', 'Green\t', 'Double\t', 'Red\t','PercentGreen\t', 'PercentRed\t', 'Mean_NucleiPic\t', 'Stdev_NucleiPic\t', 'Mean_ThreshGreen\t', 'Mean_ThreshRed\t'
for slicelist in slicelist:

	nuclei = getValues(a, slicelist, col['Count_Nuclei'])
	no = len(getValues(a, slicelist, col['Count_Nuclei']))
	green = getValues(a, slicelist, col['Count_FilteredGreen'])
	greenred = getValues(a, slicelist, col['Count_FilteredGreenRedDouble'])
	red = getValues(a, slicelist, col['Count_FilteredRed'])
	thresh_green = getValues(a, slicelist, col['Math_Math_Green'])
	thresh_red = getValues(a, slicelist, col['Math_Math_Red'])
	
	print slicelist,'\t',no,'\t',sum(nuclei),'\t',sum(green),'\t',sum(greenred),'\t',sum(red),'\t',(sum(green)-sum(greenred))/sum(nuclei)*100,'\t',(sum(red)-sum(greenred))/sum(nuclei)*100,'\t',round(mean(nuclei)),'\t',round(stdev(nuclei)),'\t',mean(thresh_green) * 65536,'\t',mean(thresh_red) * 65536
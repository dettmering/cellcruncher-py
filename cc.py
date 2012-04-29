import csv
import sys

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

def createcolumnlist(a): # use it to get definition of columns on top
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

def add(array):
	n = 0
	y = 0
	
	for x in array:
		y = float(x)
		n += y
	return n
	
def mean(array):
	n = 0
	y = 0
	i = 0
	
	for x in array:
		y = float(x)
		n += y
		i += 1
	result = n / i
	
	return result
		

# --------------------------------------------------------- .split('_')[0]

a = readcsv(filename)	# read file into array
col = createcolumnlist(a)	# creates dictionary with column positions

sliceinfo = col['FileName_DAPI']	# which column should be taken to parse the slice name?

slicelist = listSlices(a, sliceinfo)	# generate list of slices in file


print 'Slice\t','No Images\t','Nuclei\t', 'Green\t', 'Double\t', 'Red\t', 'Mean_ThreshGreen\t', 'Mean_ThreshRed\t', 'PercentGreen\t', 'PercentRed\t'
for slicelist in slicelist:

	nuclei = getValues(a, slicelist, col['Count_Nuclei'])
	no = len(getValues(a, slicelist, col['Count_Nuclei']))
	green = getValues(a, slicelist, col['Count_FilteredGreen'])
	greenred = getValues(a, slicelist, col['Count_FilteredGreenRedDouble'])
	red = getValues(a, slicelist, col['Count_FilteredRed'])
	thresh_green = getValues(a, slicelist, col['Math_Math_Green'])
	thresh_red = getValues(a, slicelist, col['Math_Math_Red'])
	
	print slicelist,'\t',no,'\t',add(nuclei),'\t',add(green),'\t',add(greenred),'\t',add(red),'\t',mean(thresh_green),'\t',mean(thresh_red),'\t',(add(green)-add(greenred))/add(nuclei)*100,'\t',(add(red)-add(greenred))/add(nuclei)*100
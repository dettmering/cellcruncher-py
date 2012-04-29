import csv
import sys

filename = sys.argv[1]

Count_Cells_Green = 0
Count_Cells_Red = 1
Count_FilteredGreen = 2
Count_FilteredGreenRedDouble = 3
Count_FilteredRed = 4
Count_Nuclei = 5
ExecutionTime_01LoadImages = 6
ExecutionTime_02CorrectIlluminationCalculate = 7
ExecutionTime_03CorrectIlluminationCalculate = 8
ExecutionTime_04CorrectIlluminationCalculate = 9
ExecutionTime_05CorrectIlluminationApply = 10
ExecutionTime_06CorrectIlluminationApply = 11
ExecutionTime_07CorrectIlluminationApply = 12
ExecutionTime_08IdentifyPrimaryObjects = 13
ExecutionTime_09IdentifySecondaryObjects = 14
ExecutionTime_10IdentifySecondaryObjects = 15
ExecutionTime_11MeasureImageIntensity = 16
ExecutionTime_12CalculateMath = 17
ExecutionTime_13CalculateMath = 18
ExecutionTime_14ApplyThreshold = 19
ExecutionTime_15ApplyThreshold = 20
ExecutionTime_16MeasureObjectSizeShape = 21
ExecutionTime_17MeasureObjectIntensity = 22
ExecutionTime_18MeasureObjectIntensity = 23
ExecutionTime_19ConserveMemory = 24
ExecutionTime_20FilterObjects = 25
ExecutionTime_21FilterObjects = 26
ExecutionTime_22RelateObjects = 27
ExecutionTime_23FilterObjects = 28
ExecutionTime_24RescaleIntensity = 29
ExecutionTime_25RescaleIntensity = 30
ExecutionTime_26RescaleIntensity = 31
ExecutionTime_27GrayToColor = 32
ExecutionTime_28OverlayOutlines = 33
ExecutionTime_29OverlayOutlines = 34
ExecutionTime_30SaveImages = 35
ExecutionTime_31SaveImages = 36
ExecutionTime_32SaveImages = 37
FileName_DAPI = 38
FileName_FITC = 39
FileName_PI = 40
Group_Index = 41
Group_Number = 42
ImageNumber = 43
Intensity_MADIntensity_CorrGreen_Cells_Green = 44
Intensity_MADIntensity_CorrRed_Cells_Red = 45
Intensity_MaxIntensity_CorrGreen_Cells_Green = 46
Intensity_MaxIntensity_CorrRed_Cells_Red = 47
Intensity_MeanIntensity_CorrGreen_Cells_Green = 48
Intensity_MeanIntensity_CorrRed_Cells_Red = 49
Intensity_MedianIntensity_CorrGreen_Cells_Green = 50
Intensity_MedianIntensity_CorrRed_Cells_Red = 51
Intensity_MinIntensity_CorrGreen_Cells_Green = 52
Intensity_MinIntensity_CorrRed_Cells_Red = 53
Intensity_PercentMaximal_CorrGreen_Cells_Green = 54
Intensity_PercentMaximal_CorrRed_Cells_Red = 55
Intensity_StdIntensity_CorrGreen_Cells_Green = 56
Intensity_StdIntensity_CorrRed_Cells_Red = 57
Intensity_TotalArea_CorrGreen_Cells_Green = 58
Intensity_TotalArea_CorrRed_Cells_Red = 59
Intensity_TotalIntensity_CorrGreen_Cells_Green = 60
Intensity_TotalIntensity_CorrRed_Cells_Red = 61
MD5Digest_DAPI = 62
MD5Digest_FITC = 63
MD5Digest_PI = 64
Math_Math_Green = 65
Math_Math_Red = 66
Metadata_Date = 67
Metadata_Run = 68
ModuleError_01LoadImages = 69
ModuleError_02CorrectIlluminationCalculate = 70
ModuleError_03CorrectIlluminationCalculate = 71
ModuleError_04CorrectIlluminationCalculate = 72
ModuleError_05CorrectIlluminationApply = 73
ModuleError_06CorrectIlluminationApply = 74
ModuleError_07CorrectIlluminationApply = 75
ModuleError_08IdentifyPrimaryObjects = 76
ModuleError_09IdentifySecondaryObjects = 77
ModuleError_10IdentifySecondaryObjects = 78
ModuleError_11MeasureImageIntensity = 79
ModuleError_12CalculateMath = 80
ModuleError_13CalculateMath = 81
ModuleError_14ApplyThreshold = 82
ModuleError_15ApplyThreshold = 83
ModuleError_16MeasureObjectSizeShape = 84
ModuleError_17MeasureObjectIntensity = 85
ModuleError_18MeasureObjectIntensity = 86
ModuleError_19ConserveMemory = 87
ModuleError_20FilterObjects = 88
ModuleError_21FilterObjects = 89
ModuleError_22RelateObjects = 90
ModuleError_23FilterObjects = 91
ModuleError_24RescaleIntensity = 92
ModuleError_25RescaleIntensity = 93
ModuleError_26RescaleIntensity = 94
ModuleError_27GrayToColor = 95
ModuleError_28OverlayOutlines = 96
ModuleError_29OverlayOutlines = 97
ModuleError_30SaveImages = 98
ModuleError_31SaveImages = 99
ModuleError_32SaveImages = 100
PathName_DAPI = 101
PathName_FITC = 102
PathName_PI = 103
Scaling_DAPI = 104
Scaling_FITC = 105
Scaling_PI = 106
Threshold_FinalThreshold_Cells_Green = 107
Threshold_FinalThreshold_Cells_Red = 108
Threshold_FinalThreshold_Nuclei = 109
Threshold_FinalThreshold_ThreshGreen = 110
Threshold_FinalThreshold_ThreshRed = 111
Threshold_OrigThreshold_Cells_Green = 112
Threshold_OrigThreshold_Cells_Red = 113
Threshold_OrigThreshold_Nuclei = 114
Threshold_OrigThreshold_ThreshGreen = 115
Threshold_OrigThreshold_ThreshRed = 116
Threshold_SumOfEntropies_Cells_Green = 117
Threshold_SumOfEntropies_Cells_Red = 118
Threshold_SumOfEntropies_Nuclei = 119
Threshold_SumOfEntropies_ThreshGreen = 120
Threshold_SumOfEntropies_ThreshRed = 121
Threshold_WeightedVariance_Cells_Green = 122
Threshold_WeightedVariance_Cells_Red = 123
Threshold_WeightedVariance_Nuclei = 124
Threshold_WeightedVariance_ThreshGreen = 125
Threshold_WeightedVariance_ThreshRed = 126

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

def createcolumnlist(a):
	j = 0
	
	for a[0] in a[0]:
		print a[0], '=', j
		j += 1

def listSlices(a, column):
	slice = 'FileName'	# need to skip first row
	slicelist = []
	
	for a in a:
		slice1 = a[column].split('_')[0]
		if slice != slice1:
			slice = slice1
			slicelist.append(slice1)
	return slicelist

def getValues(a, slice, column):
	thevalues = []

	for a in a:
		if a[sliceinfo].split('_')[0] == slice:
			thevalues.append(a[column])
	return thevalues

# MATH FUNCTIONS

def add(array):
	n = 0
	y = 0
	
	for array in array:
		y = float(array)
		n += y
	return n
	
def mean(array):
	n = 0
	y = 0
	i = 0
	
	for array in array:
		y = float(array)
		n += y
		i += 1
	result = n / i
	
	return result
		

# --------------------------------------------------------- .split('_')[0]

sliceinfo = FileName_DAPI

a = readcsv(filename)	# read file
slicelist = listSlices(a, sliceinfo)

for slicelist in slicelist:
	nuclei = getValues(a, slicelist, Count_Nuclei)
	green = getValues(a, slicelist, Count_FilteredGreen)
	greenred = getValues(a, slicelist, Count_FilteredGreenRedDouble)
	red = getValues(a, slicelist, Count_FilteredRed)
	print slicelist,'\t',add(nuclei),'\t',add(green),'\t',add(greenred),'\t',add(red)
#! python
import sys
import numpy as np
import os
import re
import csv

#Enter the boundaries for expected peaks
peak_1_lower = 0
peak_1_upper = 0
peak_2_lower = 0
peak_2_upper = 0
peak_3_lower = 0
peak_3_upper = 0
peak_rand_lower = 0
peak_rand_upper = 0
def openFile(file):
	myfile = open(file,'r', encoding = 'utf-8')
	a = str(repr(myfile.read()))
	return a 
def getStartPoint(fileString):
	startPoint = re.search('<startPosition>(\d+\.\d+)</startPosition>', fileString, re.VERBOSE).group(1)
	startPoint = float(startPoint)
	return startPoint
def getEndPoint(fileString):	
	endPoint = re.search('<endPosition>(\d+\.\d+)</endPosition>', fileString, re.VERBOSE).group(1)
	endPoint = float(endPoint)
	return endPoint
def getCountArray(fileString):
	a = re.search('<intensities unit=\"counts\">(\d+(?:\s*\d+)*(?:,\d+)?)</intensities>', fileString).group(1)
	a = a.split(' ')
	b = [int(i) for i in a]
	return b	
def getCountArrayLength(countArray):
	return (len(countArray))-1
def getStepSize(startPosition, endPosition, countArray):
	countArrayLength = (len(countArray))-1
	stepSize = (endPosition - startPosition)/(countArrayLength)
	return stepSize
def getTwoThetaArray(startPosition,endPosition,stepSize,countArrayLength):
	a = [i for i in range(countArrayLength)]
	twoThetaArray = [(((i) * stepSize) + startPosition ) for i in a]
	return twoThetaArray
def findPeakMax(lowerBound,upperBound,ttwArray,countArray):
	a = [int(i) for i in countArray]
	a = a[lowerBound:upperBound]
	b = ttwArray[lowerBound:upperBound]
	i = a.index(max(a))
	maxPeak = b[i]
	return maxPeak
def get_peak_1(ttwArray,countArray):
	peak_1 = findPeakMax(peak_1_lower,peak_1_upper,ttwArray,countArray)
	return peak_1
def get_peak_2(ttwArray,countArray):
	peak_2 = findPeakMax(peak_2_lower,peak_2_upper,ttwArray,countArray)
	return peak_2
def get_rand_peak(ttwArray,countArray):
	rand_peak = findPeakMax(peak_rand_lower,peak_rand_upper,ttwArray,countArray)
	return rand_peak
def get_peak_3(ttwArray,countArray):
	endIndex = len(countArray) - 1
	peak_3 = findPeakMax(peak_3_lower, endIndex,ttwArray,countArray)
	return peak_3
##FWHM function adapted from stack overflow solution
def FWHM(x_arr,y_arr):
	half_max = max(y_arr) / 2.
    #find when function crosses line half_max (when sign of diff flips)
    #take the 'derivative' of signum(half_max - Y[])
	d = np.sign(half_max - np.array(y_arr[0:-1])) - np.sign(half_max - np.array(y_arr[1:]))
    #find the left and right most indexes
	left_idx = int(np.where(d > 0)[0])
	right_idx = int(np.where(d < 0)[-1])
	FWHM = 3600 * (x_arr[right_idx] - x_arr[left_idx])
	return FWHM#return the difference (full width)
def get_files_in_directory(dir_name):
    files = []
    for file in os.listdir(dir_name):
        files.append(file)
    return files
def orderFiles(files):
	newFiles = ['0','0','0','0']
	for file in files:
		
		if(('ttw' in file or '2tw' in file) and '102' not in file):
			if('_00_' in file):
				newFiles[0] = file
				
			elif('_18_' in file):
				newFiles[1] = file
				
		if(('omega' in file  or 'Omega' in file) and '102' not in file):
			if('_00_' in file):
				newFiles[2] = file
				
			elif('_18_' in file):
				newFiles[3] = file
					
	return newFiles
def getOnePeak(file):
	startPoint = getStartPoint(file)
	endPoint = getEndPoint(file)
	countArray = getCountArray(file)
	maxIndex = countArray.index(max(countArray))
	endIndex = len(countArray) - 1
	countArrayLength = getCountArrayLength(countArray)
	stepSize = getStepSize(startPoint, endPoint, countArray)
	twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
	maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
	return maxPeak
def format_1(orderedFiles, path):
	data = []
	for i in range(4):
		if(i == 0):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				data.append(0)
				data.append(0)
			else:
				file = openFile(path + "/" +  orderedFiles[i])
				maxPeak = getOnePeak(file)
				data.append(0)
				data.append(0)
				data.append(maxPeak)
		elif(i == 1):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				data.append(0)
				data.append(0)
			else:
				file = openFile(path + "/" + orderedFiles[i])
				maxPeak = getOnePeak(file)
				data.append(0)
				data.append(0)
				data.append(maxPeak)
		elif(i == 2):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				Omega1 = 0
			else:
				file = openFile(path + "/" + orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
				FWHM00 = FWHM(twoThetaArray,countArray)
				data.append(FWHM00)
				Omega1 = maxPeak
		elif(i == 3):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				Omega2 = 0
			else:
				file = openFile(path + "/" + orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
				FWHM18 = FWHM(twoThetaArray,countArray)
				data.append(FWHM18)
				Omega2 = maxPeak
				deltaOmega = Omega2 - Omega1
				if(np.sign(deltaOmega) == -1):
					deltaOmega *= -1
					data.append(deltaOmega)
		#print(data)
	return data
def format_3(orderedFiles,path):
	data = []
	for i in range(4):
		if(i == 0):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				data.append(0)
				data.append(0)
			else:
				file = openFile(path + "/" +  orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				peak_3 = get_peak_3(twoThetaArray,countArray)
				data.append(0)
				data.append(0)
				data.append(peak_3)
		elif(i == 1):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				data.append(0)
				data.append(0)
			else:
				file = openFile(path + "/" +  orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				peak_3 = get_peak_3(twoThetaArray,countArray)
				data.append(0)
				data.append(0)
				data.append(peak_3)
		elif(i == 2):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				Omega1 = 0
			else:
				file = openFile(path + "/" + orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
				FWHM00 = FWHM(twoThetaArray,countArray)
				data.append(FWHM00)
				Omega1 = maxPeak
		elif(i == 3):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				Omega2 = 0
			else:
				file = openFile(path + "/" + orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
				FWHM18 = FWHM(twoThetaArray,countArray)
				data.append(FWHM18)
				Omega2 = maxPeak
				deltaOmega = Omega2 - Omega1
				if(np.sign(deltaOmega) == -1):
					deltaOmega *= -1
					data.append(deltaOmega)
		#print(data)
	return data
def format_2(orderedFiles,path):
	data = []
	for i in range(4):
		if(i == 0):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				data.append(0)
				data.append(0)
			else:
				file = openFile(path + "/" +  orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				peak_1 = get_peak_1(twoThetaArray,countArray)
				peak_2 = get_peak_2(twoThetaArray,countArray)
				peak_3 = get_peak_3(twoThetaArray,countArray)
				data.append(peak_1)
				data.append(peak_2)
				data.append(peak_3)
		elif(i == 1):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				data.append(0)
				data.append(0)
			else:
				file = openFile(path + "/" +  orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				peak_1 = get_peak_1(twoThetaArray,countArray)
				peak_2 = get_peak_2(twoThetaArray,countArray)
				peak_3 = get_peak_3(twoThetaArray,countArray)
				data.append(peak_1)
				data.append(peak_2)
				data.append(peak_3)
		elif(i == 2):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				Omega1 = 0
			else:
				file = openFile(path + "/" + orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
				FWHM00 = FWHM(twoThetaArray,countArray)
				data.append(FWHM00)
				Omega1 = maxPeak
		elif(i == 3):
			fpath = path + "/" + orderedFiles[i]
			if(os.path.isfile(fpath) == False):
				data.append(0)
				Omega2 = 0
			else:
				file = openFile(path + "/" + orderedFiles[i])
				startPoint = getStartPoint(file)
				endPoint = getEndPoint(file)
				countArray = getCountArray(file)
				maxIndex = countArray.index(max(countArray))
				endIndex = len(countArray) - 1
				countArrayLength = getCountArrayLength(countArray)
				stepSize = getStepSize(startPoint, endPoint, countArray)
				twoThetaArray = getTwoThetaArray(startPoint, endPoint, stepSize, countArrayLength)
				maxPeak = findPeakMax(0,countArrayLength,twoThetaArray,countArray)
				FWHM18 = FWHM(twoThetaArray,countArray)
				data.append(FWHM18)
				Omega2 = maxPeak
				deltaOmega = Omega2 - Omega1
				if(np.sign(deltaOmega) == -1):
					deltaOmega *= -1
					data.append(deltaOmega)
		#print(data)
	return data
		
##################################################################################################
inp = 'xrd_list.txt'
dt = open(inp)
dtt = dt.read()
xrd_list = dtt.splitlines()

for line in xrd_list:
	l = line.split()
	run = l[0]
	system = (run[0:run.find('-')])
	path = "path/to/file"
	print(path)
	if(os.path.exists(path)):
		files = get_files_in_directory(path)
		
		orderedFiles = orderFiles(files)
		for file in orderedFiles:
			print(file)
		print("\n")
		dataArray = []
		line = line.upper()
		if('tag_1' in line):
			dataArray = format_1(orderedFiles,path)
		elif('tag_2' in line):
			dataArray = format_2(orderedFiles,path)
		else:
			dataArray = format_3(orderedFiles,path)
		print(dataArray)
		dataArray.insert(0,run)
		with open('xrd_data.txt','a') as outputFile:
			for item in dataArray:
				outputFile.write("%s	" % item)
			outputFile.write("\n")
	else:
		dataArray = [run,0,0,0,0,0,0,0,0,0]
		with open('xrd_data.txt','a') as outputFile:
			for item in dataArray:
				outputFile.write("%s	" % item)
			outputFile.write("\n")	
		print("Files for %s don't exist, added line of zeroes to output file!" % (run))		
####################################################################################################
#exit = "Kevin is a baller"
#while(exit != "x"):	
#	run = input("enter the run number: ")
#	system = (run[0:run.find('-')])
#	path = "path/to/files"
#	if(os.path.exists(path)):	
#		files = get_files_in_directory(path)
#	
#		orderedFiles = orderFiles(files)
#		print("\n")
#		runType = input("Enter run type\n Run Type:  ")
#		dataArray = []
#		if(runType == '1'):
#			dataArray = format_1(orderedFiles,path)
#			
#		if(runType == '2'):
#			dataArray = format_3(orderedFiles,path)
#			
#		if(runType == '3'):
#			dataArray = format_2(orderedFiles,path)
#		
#		with open('xrd_data.txt','a') as outputFile:
#			for item in dataArray:
#				outputFile.write("%s " % item)
#			outputFile.write("\n")
#	else:
#		dataArray = [0,0,0,0,0,0,0,0,0]
#		with open('xrd_data.txt','a') as outputFile:
#			for item in dataArray:
#				outputFile.write("%s " % item)
#			outputFile.write("\n")	
#		print("Files don't exist, added line of zeroes to output file!")
#	exit = input("Type \'x\' to exit press enter to continue:")

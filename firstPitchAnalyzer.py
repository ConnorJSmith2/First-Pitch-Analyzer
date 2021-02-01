import sys
import csv
import copy

#If there are 2 files, return the first (command line), if none then exit
def getCommandLineArg():
	if (len(sys.argv) == 2):
		return sys.argv[1]
	else:
		print ("Error: No file inputted. \nUsage is: python firstPitchAnalyzer.py <filename.csv>")
		exit()

def printCSV(filename):
	
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')

		for row in csv_reader:
			print (row)

def readCSV(filename): 
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')

		FAILURES = ["GIDP", "STRIKEOUT", "OUT", "FIDP", "FC"]
		SUCCESSES = ["HIT", "BB"]

		FAILURE_DICT = { i : 0 for i in FAILURES } 
		SUCCESS_DICT = { i : 0 for i in SUCCESSES } 

		PITCH_DICT = {"SUCCESS": copy.deepcopy(SUCCESS_DICT), "FAILURE": copy.deepcopy(FAILURE_DICT)}

		firstPitchData = {"STRIKE": copy.deepcopy(PITCH_DICT), "BALL": copy.deepcopy(PITCH_DICT)}

		firstPitchType = None
		# Skips header row
		next(csv_reader, None)
		for row in csv_reader:
			if (row[1] == "0-0"):
				# Resets first pitch, useful if data incomplete and new at-bat starts before event type found
				firstPitchType = None
				continue
			elif (row[1] == "0-1"):
				firstPitchType = "STRIKE"

			elif (row[1] == "1-0"):
				firstPitchType = "BALL"

			if (firstPitchType and row[4]):
				# if event, register in dict
				event = row[4].upper()
				if (event in SUCCESSES):
					firstPitchData[firstPitchType]["SUCCESS"][event] += 1
				elif (event in FAILURES):
					firstPitchData[firstPitchType]["FAILURE"][event] += 1

				# At-bat event, reset first pitch
				firstPitchType = None

		return firstPitchData


def anaylzeData(pitchData):
	pass
	#return dict from notes

def printPitchData(atBatData):
	for pitchType, pitchData in atBatData.items():
		print("********", pitchType, "********")
		for statusType, statusData in pitchData.items():
			print("/", statusType, "\\")
			for eventType, eventData in statusData.items():
				print(eventType, ": ", eventData)


def main():
	filename = getCommandLineArg()
	atBatData = readCSV(filename)

	printPitchData(atBatData)

if __name__ == "__main__":
  main()
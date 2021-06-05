import os,sys
import pandas as pd
import datetime
import itertools
import math
import random

fileSamples = open(sys.argv[1],'r')

cabecera = fileSamples.readline()
months = []
output = {}
numInitial = 0

for line in fileSamples:
	line = line.strip().split("\t")
	id = line[0]
	name = line[1]
	date = line[2]
	month = date.split("/")[1]+"-"+date.split("/")[2]
	try:
		samples = output[month]
	except:
		samples = {}
	samples[id]=[name,date]

	output[month] = samples
	numInitial = numInitial + 1
	monthToDt = datetime.datetime.strptime(month, '%m-%Y').date()
	months.append(monthToDt)

months = sorted(list(set(months)))

numTotalSamples = float(sys.argv[2])
percentage = numTotalSamples/numInitial
sizeGroup = int(sys.argv[3])


def mygrouper(n, iterable):
	args = [iter(iterable)] * n
	return ([e for e in t if e != None] for t in itertools.zip_longest(*args))

groups = list(mygrouper(sizeGroup, months))

outfile = open(sys.argv[4],'a')
for group in groups:
	all = {}
	for element in group:
		date = datetime.datetime.strftime(element,'%m-%Y')
		monthD = output[date]
		all = {**all, **monthD}
	#Select randomly
	per = math.ceil(float(len(all))*percentage)
	keys = random.sample(list(all), per)
	for key in keys:
		escribir = key+"\t"+all[key][0]+"\t"+all[key][1]+"\n"
		outfile.write(escribir)


outfile.close()

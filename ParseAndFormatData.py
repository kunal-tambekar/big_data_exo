import os
from os import listdir
from os.path import isfile, join

'''Place the file at the directory level'''
mypath = 'keck_vels_binned'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
obsMap = {}
'''parsing all the files ald loading in map before its used to genrate the equivalent csv file for
 the star in opdir_binned directory'''
for filename in onlyfiles:
    tmpFile = open(mypath+'/'+filename)
    tmpFileContent = tmpFile.read()
    lines = tmpFileContent.split('\n')
    observations = []
    for line in lines:
        values = line.split(" ", -1)
        observation = []
        i = 0
        for value in values:
            if not (value == ''):
                i+=1
                if(i<=5):
                    observation.append(float(value))
                else:
                    observation.append(int(value))
        if not (observation == []):
            observations.append(observation)
    obsMap[filename.split("_")[0]]=observations
    tmpFile.close()

opdir='opdir_binned/'
if not os.path.exists(opdir):
    os.makedirs(opdir)
keyList = []
keyList.extend(obsMap.keys())
keyList.sort()
for key in keyList :
    print(key,obsMap[key])
    opfilepath=(opdir+key+".csv")
    opfile=open(opfilepath,'w')
    for reading in obsMap[key]:
        i = 0
        for obs in reading:
            i+=1
            opfile.write(str(obs))
            if i<7: opfile.write(",")
            else: opfile.write('\n')
    opfile.close()

print("Allmfiles have been converted to CSV files in the opdir_binned folder")
import csv
import pandas as pd
import urllib2
import json

def transform(pid):
    # gather the normal physiological values
    normVals = pd.read_csv('Normal Values_v2.csv')
    normVals.columns = ['a','b','c','d','e','f','g']
    norm_params = normVals.a
    fem_low = normVals.b
    fem_high = normVals.c
    male_low = normVals.d
    male_high = normVals.e
    fem_mean = normVals.f
    male_mean = normVals.g
    szAllParams = len(norm_params)

    # load the outcomes
    outcomes = pd.read_csv('Outcomes-a.txt')
    outcomes.columns = ['a','b','c','d','e','f']
    fileID = outcomes.a
    saps1 = outcomes.b
    sofa = outcomes.c

    url = ('http://www.paulbernier.fr/critical_api/api/patient/' + pid
           + '/stats/')
    r = urllib2.urlopen(url)
    data = json.load(r)

    url = ('http://www.paulbernier.fr/critical_api/api/patient/' + pid)
    r = urllib2.urlopen(url)
    pinfo = json.load(r)

    f = open('tmp.txt', 'w')
    f.write('Time,Parameter,Value\n')
    for k in pinfo.keys():
        f.write('00:00,%s,%s\n' % (k, pinfo[k]))
    for e in data['stats']:
        f.write('%s,%s,%s\n' % (e['time'], e['var'], e['value']))
    f.close()

    # find this file within the outcomes file
    ii = fileID[fileID == int(pid)].index[0]
    fSet = pd.read_csv('tmp.txt')
    params = fSet.Parameter
    vals = fSet.Value

    # Go through eachof the normal parameters, pick out corresponding values
    # in the data set, and perform parameter transformations.
    featInstMat = [0.0]*szAllParams*2
    for jj in range(szAllParams):
        # find occurrences of each parameter in the data set
        idx = params[params == norm_params[jj].strip()].index
        dataSetVals = vals[idx]
        cnt = len(dataSetVals)

        if cnt == 0:        # if this parameter is not recorded
            featInstMat[jj] = str(float('NaN'))
            featInstMat[jj+szAllParams] = str(float('NaN'))
        else:
            # find gender since some normal changes are gender-specific
            genderIdx = params[params == 'Gender'].index
            gender = vals[genderIdx]

            # make sure to deal with specific cases of weight and urine
            if norm_params[jj].strip()=='Weight' or norm_params[jj].strip()=='Urine':
                variance = sum([pow(bb,2) for bb in [aa-dataSetVals[idx[0]] for aa in dataSetVals]])/cnt
                abnormalPct = float('NaN')
            else:
                if gender==1:
                    variance = sum([pow(bb,2) for bb in [aa-male_mean[jj] for aa in dataSetVals]])/cnt
                    abnormIdx = len(dataSetVals[dataSetVals < male_low[jj]]) + len(dataSetVals[dataSetVals > male_high[jj]])
                else:
                    variance = sum([pow(bb,2) for bb in [aa-fem_mean[jj] for aa in dataSetVals]])/cnt
                    abnormIdx = len(dataSetVals[dataSetVals < fem_low[jj]]) + len(dataSetVals[dataSetVals > fem_high[jj]])
                abnormalPct = float(abnormIdx)/cnt

            featInstMat[jj] = str(variance)
            featInstMat[jj+szAllParams] = str(abnormalPct)

    # include mechanical ventilation and outcome scores
    mechIdx = params[params == 'MechVent'].index

    if sum(vals[mechIdx]) > 0:
        mechVentParam = 1
    else:
        mechVentParam = 0

    saps1_score = saps1[ii]
    sofa_score = sofa[ii]
    if saps1_score <= 0:
        saps1_score = float('NaN')
    if sofa_score <= 0:
        sofa_score = float('NaN')
    featInstMat.extend([str(mechVentParam), str(saps1_score), str(sofa_score)])

    # output to CSV
    outflname = 'transFeatSet.csv'
    file = open(outflname, "wb")
    csvWriter = csv.writer( file, dialect='excel' )  #Defaults to the excel dialect
    csvWriter.writerow(featInstMat)
    file.close()   #Required, or the data won't get flushed to the file!

if __name__ == '__main__':
    transform('132540')

import math
import csv

def calSlope(alti, distance):
    sinth = (float(alti)) / (float(distance)*1000)
    if sinth > 1 or sinth < -1:
        return 0
    else:
        s = math.degrees(math.asin(sinth))
        return s


if __name__ == "__main__":
    matchedProbeData = [line.split(',') for line in open('./Partition6467MatchedPoints.csv')]
    while len(matchedProbeData) > 1:
        temp = [t for t in matchedProbeData if t[8].startswith(matchedProbeData[0][8])]
        # print(temp[0][8])
        comb = ''
        for i in range(len(temp)):
            if i == 0:
                slope = 0
            else:
                slope = calSlope(float(temp[i][5]) - float(temp[i-1][5]),
                                 float(temp[i][10]) - float(temp[i-1][10]))
            if comb == '':
                comb = (temp[i][10]+'/'+str(slope))
            else:
                comb = comb + '|' + (temp[i][10]+'/'+str(slope))
        with open('slope.csv', 'a', newline='') as csvfile:
            output = csv.writer(csvfile)
            output.writerow((temp[0][8],comb))
        matchedProbeData = [k for k in matchedProbeData if matchedProbeData[0][8] not in k]
    print("Slope Calculate Done!")

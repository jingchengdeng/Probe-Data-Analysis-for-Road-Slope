import csv
import operator
from math import sin, cos, sqrt, atan2, radians


def calDistance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def getNode(data):
    points = data[14].split('|')
    ref = points[0].split('/')
    nref = points[-1].split('/')
    reflat = ref[0]
    reflon = ref[1]
    nreflat = nref[0]
    nreflon = nref[1]
    return reflat, reflon, nreflat, nreflon


def projection(probelat, probelong, reflat, reflon, nreflat, nreflon):
    x = float(probelat)
    y = float(probelong)
    x1, y1 = float(reflat), float(reflon)
    x2, y2 = float(nreflat), float(nreflon)

    tmp = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
    if (tmp <= 0):
        return calDistance(x, y, x1, y1)

    d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    if (tmp >= d2):
        return calDistance(x, y, x2, y2)

    r = tmp / d2
    px = x1 + (x2 - x1) * r
    py = y1 + (y2 - y1) * r

    return calDistance(x, y, px, py)


def getDirection(prob1, prob2, refpoint):

    dis1 = calDistance(float(prob1[0]), float(prob1[1]), float(refpoint[0]), float(refpoint[1]))
    dis2 = calDistance(float(prob2[0]), float(prob2[1]), float(refpoint[0]), float(refpoint[1]))

    if dis1-dis2 < 0:
        return True
    else:
        return False


if __name__ == "__main__":
    probeData = [line.split(',') for line in open('./Partition6467ProbePoints.csv')]
    linkData = [line.split(',') for line in open('./Partition6467LinkData.csv')]
    routeData = []
    probeData = probeData[:100]
    count =0
    # for i in range(len(probeData)):
    #     probeData[i].append(i)
    for k in range(len(linkData)):
        reflat, reflon, nreflat, nreflon = getNode(linkData[k])
        routeData.append((linkData[k][0], reflat, reflon, nreflat, nreflon))
    for i in range(len(probeData)):
        candidate = []
        for k in range(len(routeData)):
            lat = probeData[i][3]
            lon = probeData[i][4]
            distance = projection(lat, lon, routeData[k][1], routeData[k][2],
                                  routeData[k][3], routeData[k][4])
            candidate.append((routeData[k][0], distance, routeData[k][1], routeData[k][2]))

        matchMap = min(candidate, key=operator.itemgetter(1))

        with open('Partition6467MatchedPoints.csv', 'a', newline='') as csvfile:
            output = csv.writer(csvfile)
            sampleID = probeData[i][0]
            dateTime = probeData[i][1]
            sourceCode = probeData[i][2]
            latitude = probeData[i][3]
            lontitude = probeData[i][4]
            altitude = probeData[i][5]
            speed = probeData[i][6]
            heading = probeData[i][7].rstrip()
            linkPVID = matchMap[0]
            if getDirection((probeData[i][3],probeData[i][4]),(probeData[i-1][3],probeData[i-1][4]),
                            (matchMap[2],matchMap[3])):
                direction = 'T'
            else:
                direction = 'F'
            distFromRef = calDistance(float(probeData[i][3]),
                                      float(probeData[i][4]),
                                      float(matchMap[2]),
                                      float(matchMap[3]))
            distFromLink = matchMap[1]
            output.writerow((sampleID, dateTime, sourceCode, latitude, lontitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink))
    print("Match Point Finished!")


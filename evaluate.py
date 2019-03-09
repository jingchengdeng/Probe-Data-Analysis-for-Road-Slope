import csv


def getAverageSlope(data):
    if len(data) > 1:
        slope = 0
        points = data.split('|')
        for i in range(len(points)):
            if slope == '':
                slope = slope + 0
            else:
                slope = slope + float(points[i].split('/')[1])
        averageSlope = slope / len(points)
        return averageSlope
    else:
        return 0


def evaluate(num1, num2):
    if (num1 + num2)/2 == 0:
        return 0
    else:
        return abs(num1 - num2) / abs((num1 + num2)/2)


if __name__ == "__main__":
    slopeData = [line.split(',') for line in open('./slope.csv')]
    linkData = [line.split(',') for line in open('./Partition6467LinkData.csv')]

    for i in range(len(slopeData)):
        linkID = slopeData[i][0]
        calSlope = getAverageSlope(slopeData[i][1])
        target = [t for t in linkData if t[0].startswith(linkID)]
        surSlope = getAverageSlope(target[0][-1])
        result = evaluate(calSlope, surSlope)
        print(result)
        with open('evaluateSlope.csv', 'a', newline='') as csvfile:
            output = csv.writer(csvfile)
            output.writerow((linkID, calSlope, surSlope, (str("{:.2f}".format(result*100))) + '%'))

import functions as f

filepath = "C:/Users/Peter/Dropbox/Programming/Python/track-analysis/subset.txt"
count, data = f.getData(filepath)

'''
clickTypePerSession (stacked bar, pie)
monitorUsedPerSession (stacked bar, pie)
clicksPerSession (line (session, clicks), histogram, box)
timePerSession (line (session, time), histogram, box)
turnOnTimePerSession (line (session, time), histogram, box)
turnOffTimePerSession (line (session, time), histogram, box)
coordinatesPerSession (2d, 3d scatter, heat)
timeBetweenClicksPerSession (histogram, box)
clicksPerHourPerSession (histogram)
'''

print(count)
'''
data0 = f.printer(f.clickTypePerSession, data)
data1 = f.printer(f.monitorUsedPerSession, data)
data2 = f.printer(f.clicksPerSession, data)
data3 = f.printer(f.timePerSession, data)
data4 = f.printer(f.turnOnTimePerSession, data)
data5 = f.printer(f.turnOffTimePerSession, data)
dataX, dataY = f.printer(f.coordinatesPerSession, data)
data6 = f.printer(f.timeBetweenClicksPerSession, data)
data7 = f.printer(f.clicksPerHourPerSession, data)
'''


'''
# plotting overall count click type
plt1 = plt
plt1.plot(xData, yData, ".r")
plt1.plot(xModel, yModel, "-k")
plt1.title("Nuclear Liquid Drop Model Predictions")
# plt1.savefig("plot1.png")
plt1.show()

# plotting error
plt2 = plt
plt2.plot(xError, logyError, "-ko")
plt2.xlim([0, 300])
plt2.ylim([-6, 1])
plt2.xlabel("Nuclear Mass Number, A")
plt2.ylabel("log10 %Error Between Model And Data")
plt2.title("Nuclear Liquid Drop Model Error")
plt2.savefig("plot2.png")
plt2.show()
'''

import functions as f
import itertools
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import random

name = "Peter"
filepath = "C:/Users/Peter/Dropbox/Programming/Python/track-analysis/" + name + "/" + name + ".txt"
count, data = f.getData(filepath)
start, end = f.getDateRange(data)

'''
0. clickTypePerSession (stacked bar, pie)
1. monitorUsedPerSession (stacked bar, pie)
2. clicksPerSession (line (session, clicks), histogram, box)
3. timePerSession (line (session, time), histogram, box)
4. turnOnTimePerSession (line (session, time), histogram, box)
5. turnOffTimePerSession (line (session, time), histogram, box)
6. coordinatesPerSession (2d, 3d scatter, heat)
7. timeBetweenClicksPerSession (histogram, box)
8. clicksPerHourPerSession (bar)
9. clicksPerDayPerSession (bar)
'''

'''
# TODO
data4 = f.printer(f.turnOnTimePerSession, data)
data5 = f.printer(f.turnOffTimePerSession, data)
'''

'''
fig0 = {
    'data': [{
		'labels': ['Left', 'Right', 'Middle', '1', '2'],
		'values': [round(x / count * 100, 2) for x in f.sumSessions(f.clickTypePerSession(data))],
		'type': 'pie',
		'marker': {'colors': [
			'rgb(152, 202, 237)',
			'rgb(108, 180, 230)',
			'rgb(65, 158, 222)',
			'rgb(35, 133, 201)',
			'rgb(27, 104, 158)'
		]}
	}],
    'layout': {'title': "Click Type (" + name + ")<br>" + start + " - " + end}
}
py.image.save_as(fig0, name + "/fig0.png")

fig1 = {
    'data': [{
		'labels': ['Primary', 'Secondary'],
		'values': [round(x / count * 100, 2) for x in f.sumSessions(f.monitorUsedPerSession(data))],
		'type': 'pie',
		'marker': {'colors': [
			'rgb(152, 202, 237)',
			'rgb(65, 158, 222)'
		]}
	}],
    'layout': {'title': "Monitor Use (" + name + ")<br>" + start + " - " + end}
}
py.image.save_as(fig1, name + "/fig1.png")

fig2 = dict(
	data = [go.Scatter(
		x = f.turnOffTimePerSession(data),
		y = f.clicksPerSession(data)
	)],
	layout = go.Layout(
		title = "Clicks Per Date (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Date"
		),
		yaxis = dict(
			title = "Clicks"
		)
	)
)
py.image.save_as(fig2, name + "/fig2.png")

data3 = [round(x.total_seconds() / 3600, 2) for x in f.timePerSession(data)]
fig3 = dict(
	data = [go.Scatter(
		x = list(range(len(data3))),
		y = data3
	)],
	layout = go.Layout(
		title = "Hours Per Session (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Session"
		),
		yaxis = dict(
			title = "Hours"
		)
	)
)
py.image.save_as(fig3, name + "/fig3.png")

data6XTemp, data6YTemp = f.coordinatesPerSession(data)
# flatten
data6XTemp = list(itertools.chain(*data6XTemp))
data6YTemp = list(itertools.chain(*data6YTemp))
k = 0.10
random.seed(0)
indicies = random.sample(range(len(data6XTemp)), round(len(data6XTemp) * k))
data6X = [data6XTemp[i] for i in indicies]
data6Y = [data6YTemp[i] for i in indicies]
fig6 = dict(
	data = [go.Scatter(
		x = data6X,
		y = data6Y,
		mode = "markers",
		marker = dict(
			size = 1
		)
	)],
	layout = go.Layout(
		title = "Click Mapping, Random Sampling = " + str(k) + " out of " + str(count) + " (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "x",
			range = [min(data6X), max(data6X)]
		),
		yaxis = dict(
			title = "y",
			range = [min(data6Y), max(data6Y)],
			zeroline = False,
			autorange = "reversed"
		)
	)
)
py.image.save_as(fig6, name + "/fig6.png")

data7Temp = [x.total_seconds() for x in list(itertools.chain(*f.timeBetweenClicksPerSession(data)))]
arr = np.array(data7Temp)
# mean = np.mean(arr)
std = np.std(arr)
data7 = []
for x in data7Temp:
	if x <= std / 5 and x >= 0:
		data7.append(x)
fig7 = go.Figure(
	data = [go.Histogram(
		x = data7
	)],
	layout = go.Layout(
		title = "Seconds Between Clicks (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Seconds"
		),
		yaxis = dict(
			title = "Count"
		)
	)
)
py.image.save_as(fig7, name + "/fig7.png")

fig8 = go.Figure(
	data = [go.Bar(
        x = [
			'0:00', '1:00', '2:00', '3:00', '4:00', '5:00',
			'6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
			'12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
			'18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
		],
        y = f.sumSessions(f.clicksPerHourPerSession(data))
	)],
	layout = go.Layout(
		title = "Clicks Per Hour (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Hour",
			tickangle = -45,
		),
		yaxis = dict(
			title = "Clicks"
		)
	)
)
py.image.save_as(fig8, name + "/fig8.png")

fig9 = go.Figure(
	data = [go.Bar(
        x = [
			'Monday', 'Tuesday', 'Wednesday', 'Thursday',
			'Friday', 'Saturday', 'Sunday'
		],
        y = f.sumSessions(f.clicksPerDayPerSession(data))
	)],
	layout = go.Layout(
		title = "Clicks Per Day (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Day"
		),
		yaxis = dict(
			title = "Clicks"
		)
	)
)
py.image.save_as(fig9, name + "/fig9.png")
'''

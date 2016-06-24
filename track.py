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
0. Click Type (pie)
1. Monitor Use (pie)
2. Clicks Per Date (line)
3. Hours Per Session (line)
4. Frequency Of Turn On Times (histogram)
5. Frequency Of Shutdown Times (histogram)
6. Click Mapping (scatter)
7. Frequency Of Seconds Between Clicks (histogram)
8. Clicks By The Hour (bar)
9. Clicks By The Day (bar)
10. Frequency Of Clicks Per Session (histogram)
11. Frequency Of Hours Per Session (histogram)
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

data4Temp = []
for x in f.turnOnTimePerSession(data):
	if x is None:
		continue
	elif x.time().minute >= 30:
		data4Temp.append((x.time().hour + 1) % 24)
	else:
		data4Temp.append((x.time().hour) % 24)
data4 = [0] * 24
for x in data4Temp:
	data4[x] += 1

fig4 = go.Figure(
	data = [go.Bar(
        x = [
			'0:00', '1:00', '2:00', '3:00', '4:00', '5:00',
			'6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
			'12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
			'18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
		],
        y = data4
	)],
	layout = go.Layout(
		title = "Frequency Of Turn On Times (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Turn On Times",
			tickangle = -45,
		),
		yaxis = dict(
			title = "Frequency"
		),
		bargap = 0
	)
)
py.image.save_as(fig4, name + "/fig4.png")

data5Temp = []
for x in f.turnOffTimePerSession(data):
	if x is None:
		continue
	elif x.time().minute >= 30:
		data5Temp.append((x.time().hour + 1) % 24)
	else:
		data5Temp.append((x.time().hour) % 24)
data5 = [0] * 24
for x in data5Temp:
	data5[x] += 1

fig5 = go.Figure(
	data = [go.Bar(
        x = [
			'0:00', '1:00', '2:00', '3:00', '4:00', '5:00',
			'6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
			'12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
			'18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
		],
        y = data5
	)],
	layout = go.Layout(
		title = "Frequency Of Shutdown Times (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Shutdown Times",
			tickangle = -45,
		),
		yaxis = dict(
			title = "Frequency"
		),
		bargap = 0
	)
)
py.image.save_as(fig5, name + "/fig5.png")

data6XTemp, data6YTemp = f.coordinatesPerSession(data)
# flatten
data6XTemp = list(itertools.chain(*data6XTemp))
data6YTemp = list(itertools.chain(*data6YTemp))
k = 0.80
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
		title = "Click Mapping (Primary), Sampling " + str(k * 100) + "% out of " + str(count) + " (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "x",
			range = [0, 1920]
		),
		yaxis = dict(
			title = "y",
			range = [1080, 0],
			zeroline = False
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
		title = "Frequency Of Seconds Between Clicks (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Seconds Between Clicks"
		),
		yaxis = dict(
			title = "Frequency"
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
		title = "Clicks By The Hour (" + name + ")<br>" + start + " - " + end,
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
		title = "Clicks By The Day (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Day"
		),
		yaxis = dict(
			title = "Clicks"
		)
	)
)
py.image.save_as(fig9, name + "/fig9.png")

data10 = [round(x, -2) for x in f.clicksPerSession(data)]
fig10 = go.Figure(
	data = [go.Histogram(
		x = data10,
		autobinx = False,
		xbins = dict(
			start = 0,
			end = max(data10),
			size = 500
		)
	)],
	layout = go.Layout(
		title = "Frequency Of Clicks Per Session (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Clicks Per Session"
		),
		yaxis = dict(
			title = "Frequency"
		)
	)
)
py.image.save_as(fig10, name + "/fig10.png")

fig11 = go.Figure(
	data = [go.Histogram(
		x = [round(x.total_seconds() / 3600, 0) for x in f.timePerSession(data)],
		autobinx = False,
		xbins = dict(
			start = 0,
			end = 30,
			size = 1
		)
	)],
	layout = go.Layout(
		title = "Frequency Of Hours Per Session (" + name + ")<br>" + start + " - " + end,
		xaxis = dict(
			title = "Hours Per Session"
		),
		yaxis = dict(
			title = "Frequency"
		)
	)
)
py.image.save_as(fig11, name + "/fig11.png")
'''

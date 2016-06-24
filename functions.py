from datetime import datetime, timedelta

def getData(filepath):
	file = open(filepath, "r")

	# format timestamp string into datetime object
	format = "%Y%m%d%H%M%S"

	count = 0
	session = []
	action = []
	for line in file:
		# remove newlines and split comma-delimited string into a list
		line = line.rstrip("\n").split(",")

		# @ means a new session
		if line[0] is "@":
			session.append(action)
			action = []
		else:
			count += 1
			line[1] = int(line[1])
			line[2] = int(line[2])
			line[4] = datetime.strptime(line[4], format)
			action.append(line)

	file.close()
	return count, session

def getDateRange(data):
	for i in range(len(data)):
		try:
			date = data[i][0][4]
		except IndexError:
			date = None

		if date is not None:
			start = date.date()
			break

	for i in range(len(data)):
		i += 1

		try:
			date = data[len(data) - i][len(data[len(data) - 1]) - 1][4]
		except IndexError:
			date = None

		if date is not None:
			end = date.date()
			break
	return str(start), str(end)

# for debugging
def printer(f, *x):
	data = f(*x)
	print(f.__name__ + ":", data)
	return data

# combine data for all sessions
def sumSessions(data):
	length = len(data[0])
	ret = [0] * length
	for session in data:
		for i in range(length):
			try:
				ret[i] += session[i]
			except:
				ret[i]
	return ret

def clickTypePerSession(data):
	ret = []
	for session in data:
		# left, right, middle, 1, 2
		button = [0, 0, 0, 0, 0]
		for action in session:
			if action[0] is "L":
				button[0] += 1
			elif action[0] is "R":
				button[1] += 1
			elif action[0] is "M":
				button[2] += 1
			elif action[0] is "1":
				button[3] += 1
			elif action[0] is "2":
				button[4] += 1
			else:
				print("Invalid button type was read.")
				raise SystemExit
		ret.append(button)
	return ret

def monitorUsedPerSession(data):
	ret = []
	for session in data:
		# right monitor (primary), left monitor (secondary)
		monitor = [0, 0]
		for action in session:
			if action[1] >= 0:
				monitor[0] += 1
			else:
				monitor[1] += 1
		ret.append(monitor)
	return ret

def clicksPerSession(data):
	ret = []
	for session in data:
		ret.append(len(session))
	return ret

def timePerSession(data):
	ret = []
	for session in data:
		try:
			date = session[len(session) - 1][4] - session[0][4]
		except IndexError:
			date = timedelta(0, 0)
		ret.append(date)
	return ret

def turnOnTimePerSession(data):
	ret = []
	for session in data:
		try:
			date = session[0][4]
		except IndexError:
			date = None
		ret.append(date)
	return ret

def turnOffTimePerSession(data):
	ret = []
	for session in data:
		try:
			date = session[len(session) - 1][4]
		except IndexError:
			date = None
		ret.append(date)
	return ret

def coordinatesPerSession(data):
	retx = []
	rety = []
	for session in data:
		x = []
		y = []
		for action in session:
			x.append(action[1])
			y.append(action[2])
		retx.append(x)
		rety.append(y)
	return retx, rety

def timeBetweenClicksPerSession(data):
	ret = []
	for session in data:
		inbetween = []
		for i in range(len(session) - 1):
			delta = session[i + 1][4] - session[i][4]
			inbetween.append(delta)
		ret.append(inbetween)
	return ret

def clicksPerHourPerSession(data):
	ret = []
	for session in data:
		hours = [0] * 24
		for action in session:
			hours[action[4].hour] += 1
		ret.append(hours)
	return ret

def clicksPerDayPerSession(data):
	ret = []
	for session in data:
		days = [0] * 7
		for action in session:
			# mon : 0, sun: 6
			days[action[4].weekday()] += 1
		ret.append(days)
	return ret

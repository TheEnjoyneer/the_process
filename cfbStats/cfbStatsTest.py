#cfbStatsTest.py

import cfbStatsLib as api

testWeek = api.getCalendarWeek(2024, 1, "regular")

for weekList in testWeek:
	print(weekList)


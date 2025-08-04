#cfbStatsTest.py

import cfbStatsLib as api

testWeek = api.getCalendarWeek(2024, 1, "regular")

testGame = testWeek['game'][-1]

testGameDate = testGame['startDate']


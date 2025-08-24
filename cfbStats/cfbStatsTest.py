#cfbStatsTest.py

import cfbStatsLib as api

testWeek = api.getCalendarWeekReg(2024, 1)

print("\n------------- Week Nights -------------")
print(testWeek[0])
print("\n------------- Saturday Early -------------")
print(testWeek[1])
print("------------- Saturday Afternoon -------------")
print(testWeek[2])
print("\n------------- Saturday Evening -------------")
print(testWeek[3])
print("\n------------- Saturday Late -------------")
print(testWeek[4])
print("\n------------- Extra Nights -------------")
print(testWeek[5])
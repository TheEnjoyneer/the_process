#cfbStatsTest.py

import cfbStatsLib as api

testWeek = api.getCalendarWeek(2024, 1, "regular")

print("------------- Week Nights -------------")
print(testWeek[0])
print("------------- Saturday Early -------------")
print(testWeek[1])
print("------------- Saturday Afternoon -------------")
print(testWeek[2])
print("------------- Saturday Evening -------------")
print(testWeek[3])
print("------------- Saturday Late -------------")
print(testWeek[4])
print("------------- Extra Nights -------------")
print(testWeek[5])
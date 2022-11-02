# Test Script

import teamDataImport as tdi
from pprint import pprint
import numpy as np
import pandas as pd

statsObj = tdi.calcStats()
data = tdi.infoRequest(2022)
gamesData = data.getGames()


teamsData = data.getTeams()
teamsData = teamsData['school']

simpleRatings = statsObj.basicSRS(gamesData)

#filteredRatings = simpleRatings[(simpleRatings['team'].isin(teamsData))]

#print(filteredRatings[0:50])
print(simpleRatings[0:50])


















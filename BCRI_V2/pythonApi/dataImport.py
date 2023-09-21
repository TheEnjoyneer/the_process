# Christopher Brant
# Fall 2023
# dataImport.py
# Base Data Import Testing File

from __future__ import print_function
import time
import datetime
from datetime import date
import cfbd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cfbd.rest import ApiException
from pprint import pprint

class weekClass:
	def __init__(self, weekObj):
		self.firstGameDate = datetime.datetime(int(weekObj.first_game_start[0:4]), int(weekObj.first_game_start[5:7]), int(weekObj.first_game_start[8:10]))
		self.lastGameDate = datetime.datetime(int(weekObj.last_game_start[0:4]), int(weekObj.last_game_start[5:7]), int(weekObj.last_game_start[8:10]))
		self.weekNum = weekObj.week

class cfbGame:
	def __init__(self, gameObj):
		self.lines = []
		self.venue = None
		self.homeEpa = None
		self.homeAdvStats = None
		self.homeRank = None
		self.homeTeamRank = None
		self.awayEpa = None
		self.awayAdvStats = None
		self.awayRank = None
		self.awayTeamRank = None
		self.rankOnRank = False
		self.homeLogo = None
		self.awayLogo = None
		self.homeTeam =  gameObj.home_team
		self.awayTeam = gameObj.away_team
		self.homeCon = str(gameObj.home_conference)
		self.awayCon = str(gameObj.away_conference)
		self.confGame = False
		if self.homeCon == self.awayCon:
			self.confGame = True
		self.gameID = gameObj.id
		if hasattr(gameObj, "start_date"):
			self.startDate = gameObj.start_date
		if hasattr(gameObj, "lines"):
			linesList = gameObj.lines
			for item in linesList:
				if item.provider == "Bovada":
					self.lines.append(item)
		if hasattr(gameObj, "venue"):
			self.venue = gameObj.venue	
	
	def setLines(self, linesObj):
		for item in linesObj:
			if item.provider == "Bovada":
				self.lines.append(item)
 
	def printOnlyMatchup(self):
		print("\n\n" + self.awayTeamRank + " at " + self.homeTeamRank)

	def printBasicGameInfo(self):
		print("\n\n" + self.awayTeamRank + " at " + self.homeTeamRank)
		print(self.awayCon + " vs " + self.homeCon)
		if self.venue is not None:
			print("Venue: " + self.venue)

	def printLines(self):
		self.printBasicGameInfo()
		for line in self.lines:
			print("Line Provider: " + line.provider)
			print("Current Spread: " + line.formatted_spread)
			if line.spread_open > 0:
				print("Opening Spread: " + self.awayTeam + " -" + str(line.spread_open))
			elif line.spread_open < 0:
				print("Opening Spread: " + self.homeTeam + " " + str(line.spread_open))
			else:
				print("Opening Spread: Pick 'em")
			# Do calcs for line movement here too
			#print("Line movement: " + "\n")
			if (line.over_under_open is not None) and (line.over_under is not None):
				print("Current Point Total: " + str(line.over_under))
				print("Opening Point Total: " + str(line.over_under_open))
				lineMovement = line.over_under_open - line.over_under
				#print("Point Total Movement: " + str(lineMovement) + "\n")
		
	def printAdvStatsMatchup(self):
		print("\n{:<20} {:<20} {:<20}".format("Adv Stats", self.homeTeam, self.awayTeam))
		if (self.homeAdvStats is None) or (self.awayAdvStats is None):
			print("One or both teams in the given matchup does not have advanced stats data\n")
			return
		homeStats = self.homeAdvStats
		awayStats = self.awayAdvStats
		# Print adv stats in a table format
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffScsRt/DefScsRt", homeStats["offense"].success_rate, awayStats["defense"].success_rate))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefScsRt/OffScsRt", homeStats["defense"].success_rate, awayStats["offense"].success_rate))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffExpl/DefExpl", homeStats["offense"].explosiveness, awayStats["defense"].explosiveness))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefExpl/OffExpl", homeStats["defense"].explosiveness, awayStats["offense"].explosiveness))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffPwrScs/DefPwrScs", homeStats["offense"].power_success, awayStats["defense"].power_success))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefPwrScs/OffPwrScs", homeStats["defense"].power_success, awayStats["offense"].power_success))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffStfRt/DefStfRt", homeStats["offense"].stuff_rate, awayStats["defense"].stuff_rate))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefStfRt/OffStfRt", homeStats["defense"].stuff_rate, awayStats["offense"].stuff_rate))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffPPO/DefPPO", homeStats["offense"].points_per_opportunity, awayStats["defense"].points_per_opportunity))
		print("{:<20} {:<20.3f} {:<20.3f}\n".format("DefPPO/OffPPO", homeStats["defense"].points_per_opportunity, awayStats["offense"].points_per_opportunity))

	def printEpaMatchup(self):
		print("\n{:<20} {:<20} {:<20}".format("PPA Stats", self.homeTeam, self.awayTeam))
		if (self.homeEpa is None) or (self.awayEpa is None):
			print("One or both teams in the given matchup does epa data\n")
			return
		homeEpa = self.homeEpa
		awayEpa = self.awayEpa
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffOvr/DefOvr", homeEpa["offense"].overall, awayEpa["defense"].overall))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefOvr/OffOvr", homeEpa["defense"].overall, awayEpa["offense"].overall))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffPass/DefPass", homeEpa["offense"].passing, awayEpa["defense"].passing))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefPass/OffPass", homeEpa["defense"].passing, awayEpa["offense"].passing))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffRush/DefRush", homeEpa["offense"].rushing, awayEpa["defense"].rushing))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefRush/OffRush", homeEpa["defense"].rushing, awayEpa["offense"].rushing))
		print("{:<20} {:<20.3f} {:<20.3f}".format("OffRush/DefRush", homeEpa["offense"].rushing, awayEpa["defense"].rushing))
		print("{:<20} {:<20.3f} {:<20.3f}".format("DefRush/OffRush", homeEpa["defense"].rushing, awayEpa["offense"].rushing))
		print("{:<20} {:<20.3f} {:<20.3f}".format("Off1stD/Def1stD", homeEpa["offense"].first_down, awayEpa["defense"].first_down))
		print("{:<20} {:<20.3f} {:<20.3f}".format("Def1stD/Off1stD", homeEpa["defense"].first_down, awayEpa["offense"].first_down))
		print("{:<20} {:<20.3f} {:<20.3f}".format("Off2ndD/Def2ndD", homeEpa["offense"].second_down, awayEpa["defense"].second_down))
		print("{:<20} {:<20.3f} {:<20.3f}".format("Def3rdD/Off3rdD", homeEpa["defense"].third_down, awayEpa["offense"].third_down))
		print("{:<20} {:<20.3f} {:<20.3f}".format("Off3rdD/Def3rdD", homeEpa["offense"].third_down, awayEpa["defense"].third_down))
		print("{:<20} {:<20.3f} {:<20.3f}\n".format("Def2ndD/Off2ndD", homeEpa["defense"].second_down, awayEpa["offense"].second_down))

	def setMatchupAdvStats(self, advStatsObj):
		if self.homeTeam in advStatsObj:
			self.homeAdvStats = advStatsObj[self.homeTeam]
		if self.awayTeam in advStatsObj:
			self.awayAdvStats = advStatsObj[self.awayTeam]

	def setMatchupEpa(self, epaObj):
		if self.homeTeam in epaObj:
			self.homeEpa = epaObj[self.homeTeam]
		if self.awayTeam in epaObj:
			self.awayEpa = epaObj[self.awayTeam]

	def setMatchupRanks(self, rankObj):
		if self.homeTeam in rankObj:
			self.homeRank = rankObj[self.homeTeam]
			self.homeTeamRank = "#" + str(rankObj[self.homeTeam]) + " " + self.homeTeam
		else:
			self.homeTeamRank = self.homeTeam
		if self.awayTeam in rankObj:
			self.awayRank = rankObj[self.awayTeam]
			self.awayTeamRank = "#" + str(rankObj[self.awayTeam]) + " " + self.awayTeam
		else:
			self.awayTeamRank = self.awayTeam
		if (self.homeRank is not None) and (self.awayRank is not None):
			self.rankOnRank = True

	def setLogoLinks(self, teamObj):
		self.homeLogo = teamObj[self.homeTeam].logos[0]
		self.awayLogo = teamObj[self.awayTeam].logos[0]

	def createMatchupPreview(self):
		



		return

# Get initial time variables
today = datetime.date.today()
year = today.year
# Get week of season from command line (set up later, hard code for now)
division = 'fbs'

# Configure API key authorization
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'
configuration.api_key_prefix['Authorization'] = 'Bearer'

# Get info for weekly matchups for additional peripheral info
def getMatchupInfo():
	return 0

def getWeekGames(weekNum):
	# create an instance of the API class
	api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
	season_type = 'regular'
	try:
		api_response = api_instance.get_games(year, week=weekNum, season_type=season_type, division='fbs')
		return api_response
	except ApiException as e:
		print("Exception when calling GamesApi->get_games: %s\n" % e)
		return 0


def getWeekLines(weekNum):
	# create an instance of the API class
	api_instance = cfbd.BettingApi(cfbd.ApiClient(configuration))
	season_type = 'regular'
	try:
		api_response = api_instance.get_lines(year=year, week=weekNum, season_type=season_type)
		return api_response
	except ApiException as e:
		print("Exception when calling BettingApi->get_lines: %s\n" % e)
		return 0

# Get ranking data to order/organize matchups weekly, tend to use AP poll
def getTeamRankingsAP(weekNum):
	# create an instance of the API class
	api_instance = cfbd.RankingsApi(cfbd.ApiClient(configuration))
	season_type = 'regular'
	try:
		api_response = api_instance.get_rankings(year, week=weekNum, season_type=season_type)
		polls = api_response[0].polls
		apPollList = None
		for rankList in polls:
			if rankList.poll == "AP Top 25":
				apPollList = rankList.ranks
		if apPollList is not None:
			pollDict = {}
			for rankItem in apPollList:
				pollDict[rankItem.school] = rankItem.rank 
		return pollDict
	except ApiException as e:
		print("Exception when calling RankingsApi->get_rankings: %s\n" % e)
		return 0

# Get ppa/epa metrics per team
def getTeamEpa():
	# create an instance of the API class
	api_instance = cfbd.MetricsApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_team_ppa(year=year, exclude_garbage_time=True)
		teamEpa = {}
		for listTeam in api_response:
			teamEpa[listTeam.team] = {"offense": listTeam.offense, "defense": listTeam.defense}
		return teamEpa
	except ApiException as e:
		print("Exception when calling MetricsApi->get_team_ppa: %s\n" % e)
		return 0

# Get advanced metric data per team
def getTeamAdvStats():
	# create an instance of the API class
	api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_advanced_team_season_stats(year=year, exclude_garbage_time=True)
		teamAdvStats = {}
		for listTeam in api_response:
			teamAdvStats[listTeam.team] = {"offense": listTeam.offense, "defense": listTeam.defense}
		return teamAdvStats
	except ApiException as e:
		print("Exception when calling StatsApi->get_advanced_team_season_stats: %s\n" % e)
		return 0

def getTeams():
	# create an instance of the API class
	api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_teams()
		teamDict = {}
		for team in api_response:
			teamDict[team.school] = team
		return teamDict
	except ApiException as e:
		print("Exception when calling TeamsApi->get_teams: %s\n" % e)
		return 0

# Get calendar to know what week it is
def getCurrWeek():
	currWeek = 0
	# create an instance of the API class
	api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
	season_type = 'regular'
	try:
		api_response = api_instance.get_calendar(year=year)
		weeksFormatted = []
		for week in api_response:
			weeksFormatted.append(weekClass(week))
		currDate = str(date.today())
		testDate = datetime.datetime(int(currDate[0:4]), int(currDate[5:7]), int(currDate[8:10]))
		for i in range(1, len(weeksFormatted) - 1):
			if (testDate < weeksFormatted[i].lastGameDate) and (testDate > weeksFormatted[i-1].lastGameDate):
				currWeek = weeksFormatted[i].weekNum
		return currWeek
	except ApiException as e:
		print("Exception when calling GamesApi->get_calendar: %s\n" % e)
		return 0



# Order lists via conference games
def confGamesOrderList(gamesList):
	confOrder = []
	secList = []
	accList = []
	big10List = []
	big12List = []
	pac12List = []
	otherList = []
	for game in gamesList:
		if game.homeCon == "SEC" or game.awayCon == "SEC":
			secList.append(game)
		elif game.homeCon == "ACC" or game.awayCon == "ACC":
			accList.append(game)
		elif game.homeCon == "Big 10" or game.awayCon == "Big Ten":
			big10List.append(game)
		elif game.homeCon == "Big 12" or game.awayCon == "Big 12":
			big12List.append(game)
		elif game.homeCon == "Pac 12" or game.awayCon == "Pac-12":
			pac12List.append(game)
		else:
			otherList.append(game)

	confOrder = secList + accList + big10List + big12List + pac12List + otherList
	return confOrder

# Order games in list 
def orderGamesList(gamesList):
	rankOnRankList = []
	oneRankList = []
	otherList = []

	for game in gamesList:
		if game.rankOnRank == True:
			rankOnRankList.append(game)
		elif (game.homeRank is not None) or (game.awayRank is not None):
			oneRankList.append(game)
		else:
			otherList.append(game)

	orderedRankOnRank = confGamesOrderList(rankOnRankList)
	orderedOneRank = confGamesOrderList(oneRankList)
	orderedOther = confGamesOrderList(otherList)

	orderedList = orderedRankOnRank + orderedOneRank + orderedOther

	return orderedList

# Aggregate matchup information into list of week games and order them
def matchupListAggregator(weekNum):
	allTeams = getTeams()
	rankingsList = getTeamRankingsAP(weekNum)
	weekGamesList = getWeekGames(weekNum)
	weekGamesLines = getWeekLines(weekNum)
	teamEpaList = getTeamEpa()
	teamAdvStatsList = getTeamAdvStats()

	weekGames = []
	for game in weekGamesList:
		weekGame = cfbGame(game)
		weekGame.setLogoLinks(allTeams)
		weekGame.setMatchupEpa(teamEpaList)
		weekGame.setMatchupAdvStats(teamAdvStatsList)
		weekGame.setMatchupRanks(rankingsList)
		for lineGame in weekGamesLines:
			if weekGame.gameID == lineGame.id:
				weekGame.setLines(lineGame.lines)
		weekGames.append(weekGame)

	orderedGames = orderGamesList(weekGames)
	return orderedGames



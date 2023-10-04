# Christopher Brant
# Fall 2023
# dataImport.py
# Base Data Import Testing File

from __future__ import print_function
import datetime
from datetime import date
import cfbd
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
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
		self.homeWinProb = None
		self.venue = None
		self.location = None
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
		self.homePostWinProb = None
		self.awayPostWinProb = None
		self.homeTeamRecordTotal = None
		self.homeTeamRecordConf = None
		self.homeTeamRecordHome = None
		self.homeTeamRecordAway = None
		self.awayTeamRecordTotal = None
		self.awayTeamRecordConf = None
		self.awayTeamRecordHome = None
		self.awayTeamRecordAway = None
		self.startDate = gameObj.start_date
		self.completed = gameObj.completed
		self.homeTeam =  gameObj.home_team
		self.awayTeam = gameObj.away_team
		self.homeTeamAbbr = None
		self.awayTeamAbbr = None
		self.homeAbbrRank = None
		self.awayAbbrRank = None
		self.confGame = gameObj.conference_game
		self.gameID = gameObj.id
		self.venue = gameObj.venue
		if str(gameObj.home_conference) == "FBS Independents":
			self.homeCon = "FBS INDs"
		elif str(gameObj.home_conference) == "Conference USA":
			self.homeCon = "C-USA"
		elif str(gameObj.home_conference) == "Mid-American":
			self.homeCon = "MAC"
		elif str(gameObj.home_conference) == "American Athletic":
			self.homeCon = "AAC"
		elif str(gameObj.home_conference) == "Mountain West":
			self.homeCon = "MWC"
		else:
			self.homeCon = str(gameObj.home_conference)
		if str(gameObj.away_conference) == "FBS Independents":
			self.awayCon = "FBS INDs"
		elif str(gameObj.away_conference) == "Conference USA":
			self.awayCon = "C-USA"
		elif str(gameObj.away_conference) == "Mid-American":
			self.awayCon = "MAC"
		elif str(gameObj.away_conference) == "American Athletic":
			self.awayCon = "AAC"
		elif str(gameObj.away_conference) == "Mountain West":
			self.awayCon = "MWC"
		else:
			self.awayCon = str(gameObj.away_conference)
	
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
			self.homeAbbrRank = "#" + str(rankObj[self.homeTeam]) + " " + self.homeTeamAbbr
		else:
			self.homeTeamRank = self.homeTeam
			self.homeAbbrRank = self.homeTeamAbbr
		if self.awayTeam in rankObj:
			self.awayRank = rankObj[self.awayTeam]
			self.awayTeamRank = "#" + str(rankObj[self.awayTeam]) + " " + self.awayTeam
			self.awayAbbrRank = "#" + str(rankObj[self.awayTeam]) + " " + self.awayTeamAbbr
		else:
			self.awayTeamRank = self.awayTeam
			self.awayAbbrRank = self.awayTeamAbbr
		if (self.homeRank is not None) and (self.awayRank is not None):
			self.rankOnRank = True

	def setLogoLinks(self, teamObj):
		self.homeLogo = teamObj[self.homeTeam].logos[0]
		self.awayLogo = teamObj[self.awayTeam].logos[0]

	def setTeamAbbr(self, teamObj):
		self.homeTeamAbbr = teamObj[self.homeTeam].abbreviation
		self.awayTeamAbbr = teamObj[self.awayTeam].abbreviation

	def setVenueInfo(self, venObj):
		for venue in venObj:
			if venue.name == self.venue:
				self.location = venue.city + ", " + venue.state

	def setWinProb(self, wpObj):
		for game in wpObj:
			if game.game_id == self.gameID:
				self.homeWinProb = game.home_win_prob

	def setTeamRecords(self, recObj):
		for team in recObj:
			if team.team == self.homeTeam:
				self.homeTeamRecordTotal = self.recordFormat(team.total)
				self.homeTeamRecordConf = self.recordFormat(team.conference_games)
				self.homeTeamRecordHome = self.recordFormat(team.home_games)
				self.homeTeamRecordAway = self.recordFormat(team.away_games)
			elif team.team == self.awayTeam:
				self.awayTeamRecordTotal = self.recordFormat(team.total)
				self.awayTeamRecordConf = self.recordFormat(team.conference_games)
				self.awayTeamRecordHome = self.recordFormat(team.home_games)
				self.awayTeamRecordAway = self.recordFormat(team.away_games)

	def recordFormat(self, recObj):
		retStr = ""
		if recObj.ties == 0:
			retStr = str(recObj.wins) + "-" + str(recObj.losses) 
		else:
			retStr = str(recObj.wins) + "-" + str(recObj.losses) + "-" + str(recObj.ties)
		return retStr

# Get initial time variables
today = datetime.date.today()
year = today.year
# Get week of season from command line (set up later, hard code for now)
division = 'fbs'

# Configure API key authorization
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'
configuration.api_key_prefix['Authorization'] = 'Bearer'
#configuration.proxy = 'http://proxy.server:3128'

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
			offObj = listTeam.offense
			defObj = listTeam.defense
			teamOffense = {
				"overall": offObj.overall,
				"passing": offObj.passing,
				"rushing": offObj.rushing,
				"first_down": offObj.first_down,
				"second_down": offObj.second_down,
				"third_down": offObj.third_down
			}
			teamDefense = {
				"overall": defObj.overall,
				"passing": defObj.passing,
				"rushing": defObj.rushing,
				"first_down": defObj.first_down,
				"second_down": defObj.second_down,
				"third_down": defObj.third_down
			}
			teamEpa[listTeam.team] = {"offense": teamOffense, "defense": teamDefense}
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
			offObj = listTeam.offense
			defObj = listTeam.defense
			teamOffense = {
				"plays": offObj.plays,
				"drives": offObj.drives,
				"ppa": offObj.ppa,
				"success_rate": offObj.success_rate,
				"explosiveness": offObj.explosiveness,
				"power_success": offObj.power_success,
				"stuff_rate": offObj.stuff_rate,
				"line_yards": offObj.line_yards,
				"second_level_yards": offObj.second_level_yards,
				"open_field_yards": offObj.open_field_yards,
				"points_per_opportunity": offObj.points_per_opportunity,
				"average_fp_start": offObj.field_position.average_start,
				"average_fp_ppa": offObj.field_position.average_predicted_points,
				"rushing_success_rate": offObj.rushing_plays.success_rate,
				"rushing_rate": offObj.rushing_plays.rate,
				"rushing_explosiveness": offObj.rushing_plays.explosiveness,
				"passing_success_rate": offObj.passing_plays.success_rate,
				"passing_rate": offObj.passing_plays.rate,
				"passing_explosiveness": offObj.passing_plays.explosiveness
				}
			teamDefense = {
				"plays": defObj.plays,
				"drives": defObj.drives,
				"ppa": defObj.ppa,
				"success_rate": defObj.success_rate,
				"explosiveness": defObj.explosiveness,
				"power_success": defObj.power_success,
				"stuff_rate": defObj.stuff_rate,
				"line_yards": defObj.line_yards,
				"second_level_yards": defObj.second_level_yards,
				"open_field_yards": defObj.open_field_yards,
				"points_per_opportunity": defObj.points_per_opportunity,
				"average_fp_start": defObj.field_position.average_start,
				"average_fp_ppa": defObj.field_position.average_predicted_points,
				"rushing_success_rate": defObj.rushing_plays.success_rate,
				"passing_success_rate": defObj.passing_plays.success_rate,
				"rushing_explosiveness": defObj.rushing_plays.explosiveness,
				"passing_explosiveness": defObj.passing_plays.explosiveness,
				"havoc_total": defObj.havoc.total,
				"havoc_front_seven": defObj.havoc.front_seven,
				"havoc_db": defObj.havoc.db
				}
			teamAdvStats[listTeam.team] = {"offense": teamOffense, "defense": teamDefense}
		return teamAdvStats
	except ApiException as e:
		print("Exception when calling StatsApi->get_advanced_team_season_stats: %s\n" % e)
		return 0

# Get team stats both epa and adv stats in one object list
def getTeamStats():
	teamEpa = getTeamEpa()
	teamAdvStats = getTeamAdvStats()
	teams = getFBSTeams()
	teamStatsDict = {}
	for team in teams:
		if team in teamEpa:
			epaDict = teamEpa[team]
		else:
			epaDict = {"offense": "None", "defense": "None"}
		if team in teamAdvStats:
			advStatsDict = teamAdvStats[team]
		else:
			advStatsDict = None
		# Possibly add ability to have epa stats added to teamStatsDict
		teamStatsDict[team] = {"epa": epaDict, "advStats": advStatsDict}

	return teamStatsDict

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
	
def getFBSTeams():
	# create an instance of the API class
	api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_fbs_teams()
		teamDict = {}
		for team in api_response:
			teamDict[team.school] = team
		return teamDict
	except ApiException as e:
		print("Exception when calling TeamsApi->get_fbs_teams: %s\n" % e)
		return 0
	
def getVenueInfo():
	# create an instance of the API class
	api_instance = cfbd.VenuesApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_venues()
		return api_response
	except ApiException as e:
		print("Exception when calling VenuesApi->get_venues: %s\n" % e)
		return 0
	
def getPregameWinProb(weekNum):
	# create an instance of the API class
	season_type = 'regular'
	api_instance = cfbd.MetricsApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_pregame_win_probabilities(year=year, week=weekNum, season_type=season_type)
		return api_response
	except ApiException as e:
		print("Exception when calling MetricsApi->get_pregame_win_probabilities: %s\n" % e)
		return 0
	
def getTeamRecords():
	# create an instance of the API class
	api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
	try:
		api_response = api_instance.get_team_records(year=year)
		return api_response
	except ApiException as e:
		print("Exception when calling GamesApi->get_team_records: %s\n" % e)
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
	teamRecords = getTeamRecords()
	allVenues = getVenueInfo()
	rankingsList = getTeamRankingsAP(weekNum)
	weekGamesList = getWeekGames(weekNum)
	weekGamesLines = getWeekLines(weekNum)
	teamEpaList = getTeamEpa()
	teamAdvStatsList = getTeamAdvStats()
	weekGamesPreWinProb = getPregameWinProb(weekNum)

	weekGames = []
	for game in weekGamesList:
		weekGame = cfbGame(game)
		weekGame.setTeamRecords(teamRecords)
		weekGame.setLogoLinks(allTeams)
		weekGame.setTeamAbbr(allTeams)
		weekGame.setMatchupEpa(teamEpaList)
		weekGame.setMatchupAdvStats(teamAdvStatsList)
		weekGame.setMatchupRanks(rankingsList)
		weekGame.setVenueInfo(allVenues)
		weekGame.setWinProb(weekGamesPreWinProb)
		for lineGame in weekGamesLines:
			if weekGame.gameID == lineGame.id:
				weekGame.setLines(lineGame.lines)
		weekGames.append(weekGame)

	orderedGames = orderGamesList(weekGames)
	return orderedGames



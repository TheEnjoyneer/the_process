# teamDataImport.py
# Christopher Brant
# Fall 2022
# BCRI Data Import Class V2

from __future__ import print_function
import time, datetime, json
import cfbd
import numpy as np
import pandas as pd
from cfbd.rest import ApiException
from pprint import pprint
from urllib.parse import quote


# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'
configuration.api_key_prefix['Authorization'] = 'Bearer'

configuration = cfbd.ApiClient(configuration)

class infoRequest():

	# Initialize with the desired year
	def __init__(self, given_year):
		self.year = given_year
		self.exclude_garbage_time = True

	# # Basic information request to collect all team information
	# # Remember you have to give the year as an argument
	# def teamInfo(self):
	# 	apiString = self.api_url + "teams/fbs?year="
	# 	teams = requests.get(apiString + str(self.year), headers=self.headers)
	# 	if teams.status_code == 200:
	# 		return teams.json()
	# 	else:
	# 		print("\nError: Issue in teamInfo with status code: ", teams.status_code)
	# 		return -1


	# # Creates a list of strings that are all FBS team names
	# def teamNames(self, teams):
	# 	teamNameList = []
	# 	for team in teams:
	# 		teamNameList.append(team["school"])
	# 	return teamNameList


	# # Creates a list of conferences for FBS teams
	# def conferences(self):
	# 	apiString = self.api_url + "conferences"
	# 	conf = requests.get(apiString, headers=self.headers)
	# 	if conf.status_code == 200:
	# 		confList = []
	# 		for c in conf.json():
	# 			confList.append(c["name"])
	# 		return confList
	# 	else:
	# 		print("\nError: Issue in conferences with status code: ", conf.status_code)
	# 		return -1


	# # Searches for a teams info based on school name
	# def teamSearch(self, teams, teamName):
	# 	for team in teams:
	# 		if team["school"] == teamName:
	# 			return team


	# # Returns list of teams from that conference
	# def confTeams(self, teams, conf):
	# 	teamList = []
	# 	for team in teams:
	# 		if team["conference"] == conf:
	# 			teamList.append(team["school"])
	# 	return teamList


	# # Get a teams drive stats
	# def getDriveStats(self, teamName):
	# 	apiString = self.api_url + "drives?year="
	# 	apiString2 = "&team="
	# 	response = requests.get(apiString1 + str(self.year) + apiString2 + quote(teamName), headers=self.headers)
	# 	if response.status_code == 200:
	# 		stats = response.json()
	# 		return stats
	# 	else:
	# 		print("\nError: Issue in getDriveStats with status code: ", response.status_code)
	# 		return -1


	# Get a team's advanced stats for a specific game
	def getAdvGameStats(self, teamName, **kwargs):
		try:
			api_instance = cfbd.StatsApi(configuration)
			api_response = api_instance.get_advanced_team_game_stats(year=self.year, week=week, team=teamName, opponent=opponent, exclude_garbage_time=self.exclude_garbage_time, season_type=season_type)
			return api_response.json()
		except ApiException as e:
			print("Exception when calling StatsApi->get_advanced_team_game_stats: %s\n" % e)
			return -1


	# Get a team's advanced stats for the season
	def getAdvSeasonStats(self, teamName):
		try:
			api_instance = cfbd.StatsApi(configuration)
			api_response = api_instance.get_advanced_team_season_stats(year=self.year, team=teamName, exclude_garbage_time=self.exclude_garbage_time)
			return api_response[0]
		except ApiException as e:
			print("Exception when calling StatsApi->get_advanced_team_season_stats: %s\n" % e)
			return -1


	# Return offensive advanced stats
	def getAdvOff(self, teamAdvStats):
		return teamAdvStats.offense


	# Return defensive advanced stats
	def getAdvDef(self, teamAdvStats):
		return teamAdvStats.defense


# 	# Get team opponent list
# 	def getOpponents(self, teamName):
# 		apiString1 = self.api_url + "games?year="
# 		apiString2 = "&team="
# 		response = requests.get(apiString1 + str(self.year) + apiString2 + quote(teamName), headers=self.headers)
# 		if response.status_code == 200:
# 			opponentList = []
# 			for game in response.json():
# 				if game["home_team"] == teamName:
# 					opponentList.append(game["away_team"])
# 				else:
# 					opponentList.append(game["home_team"])

# 			return opponentList
# 		else:
# 			print("\nError: Issue in getOpponents with status code: ", response.status_code)
# 			return -1


# 	# Get team opponent win percentage
# 	def getWinPercent(self, teamName):
# 		apiString1 = self.api_url + "games?year="
# 		apiString2 = "&team="
# 		response = requests.get(apiString1 + str(self.year) + apiString2 + quote(teamName), headers=self.headers)
# 		if response.status_code == 200:
# 			wins = 0
# 			losses = 0
# 			for game in response.json():
# 				if game["home_points"] == None or game["away_points"] == None:
# 					# Do nothing
# 					pass
# 				elif game["home_team"] == teamName and (game["home_points"] >= game["away_points"]):
# 					wins += 1
# 				elif game["away_team"] == teamName and (game["away_points"] >= game["home_points"]):
# 					wins += 1
# 				else:
# 					losses += 1
# 			if (wins + losses) == 0:
# 				return 0
# 			else:
# 				return (wins / (wins + losses))
# 		else:
# 			print("\nError: Issue in getWinPercent with status code: ", response.status_code)
# 			return -1


# 	# Get a matchup's trends
# 	def getMatchupTrends(self, team1, team2):
# 		return


# 	# Get a team's betting stats on the season
# 	def getTeamBetData(self, teamName):
# 		apiString = self.api_url + "lines?year="
# 		stats = requests.get(apiString + str(self.year) + "&team=" + teamName)
# 		if stats.status_code == 200:
# 			betData = stats.json()
# 			apiString = "https://api.collegefootballdata.com/lines?year="
# 			stats = requests.get(apiString + str(self.year) + "&seasonType=postseason&team=" + teamName, headers=self.headers)
# 			if stats.status_code == 200:
# 				for i in stats.json():
# 					betData.append(i)
# 				return betData
# 			else:
# 				print("\nError in getTeamBetData")
# 				return -1
# 		else:
# 			print("\nError: Issue in getTeamBetTrends with status code: ", teams.status_code)
# 			return -1


# 	def getTeamHomeBetData(self, teamName):	
# 		apiString = self.api_url + "lines?year="
# 		stats = requests.get(apiString + str(self.year) + "&team=" + teamName + "&home=" + teamName, headers=self.headers)
# 		if stats.status_code == 200:
# 			betData = stats.json()
# 			apiString = "https://api.collegefootballdata.com/lines?year="
# 			stats = requests.get(apiString + str(self.year) + "&seasonType=postseason&team=" + teamName, headers=self.headers)
# 			if stats.status_code == 200:
# 				for i in stats.json():
# 					betData.append(i)
# 				return betData
# 			else:
# 				print("\nError in getTeamBetData")
# 				return -1
# 		else:
# 			print("\nError: Issue in getTeamBetTrends with status code: ", teams.status_code)
# 			return -1


# 	def getTeamAwayBetData(self, teamName):
# 		apiString = self.api_url + "lines?year="
# 		stats = requests.get(apiString + str(self.year) + "&team=" + teamName + "&away=" + teamName, headers=self.headers)
# 		if stats.status_code == 200:
# 			betData = stats.json()
# 			apiString = "https://api.collegefootballdata.com/lines?year="
# 			stats = requests.get(apiString + str(self.year) + "&seasonType=postseason&team=" + teamName, headers=self.headers)
# 			if stats.status_code == 200:
# 				for i in stats.json():
# 					betData.append(i)
# 				return betData
# 			else:
# 				print("\nError in getTeamBetData")
# 				return -1
# 		else:
# 			print("\nError: Issue in getTeamBetTrends with status code: ", teams.status_code)
# 			return -1


# class calcStats():
# 	# Definitions
# 	explosiveness_weight = 0.45
# 	success_weight = 0.40
# 	driveFinishing_weight = 0.15

# 	def calcHomeBetTrends(self, teamBetTrends, teamName):
# 		homeTrends = dict()
# 		homeTrends["SpreadWins"] = 0
# 		homeTrends["SpreadLosses"] = 0
# 		homeTrends["SpreadTies"] = 0
# 		homeTrends["TotalOvers"] = 0
# 		homeTrends["TotalUnders"] = 0
# 		homeTrends["TotalTies"] = 0
# 		for game in teamBetTrends:
# 			# This if statement is for when given team is at home
# 			if teamName == game["homeTeam"]:
# 				homeScore = game["homeScore"]
# 				awayScore = game["awayScore"]
# 				if type(homeScore) != type(None) and type(awayScore) != type(None):
# 					if type(game["lines"][0]["spread"]) != type(None):
# 						# Tally ATS record
# 						if (homeScore + float(game["lines"][0]["spread"])) > awayScore:
# 							homeTrends["SpreadWins"] += 1
# 						elif (homeScore + float(game["lines"][0]["spread"])) < awayScore:
# 							homeTrends["SpreadLosses"] += 1
# 						else:
# 							homeTrends["SpreadTies"] += 1

# 					if type(game["lines"][0]["overUnder"]) != type(None):
# 						# Tally point total record
# 						if (homeScore + awayScore) > float(game["lines"][0]["overUnder"]):
# 							homeTrends["TotalOvers"] += 1
# 						elif (homeScore + awayScore) < float(game["lines"][0]["overUnder"]):
# 							homeTrends["TotalUnders"] += 1
# 						else:
# 							homeTrends["TotalTies"] += 1

# 		return homeTrends


# 	def calcAwayBetTrends(self, teamBetTrends, teamName):
# 		awayTrends = dict()
# 		awayTrends["SpreadWins"] = 0
# 		awayTrends["SpreadLosses"] = 0
# 		awayTrends["SpreadTies"] = 0
# 		awayTrends["TotalOvers"] = 0
# 		awayTrends["TotalUnders"] = 0
# 		awayTrends["TotalTies"] = 0
# 		for game in teamBetTrends:
# 			# This if statement is for when given team is at home
# 			if teamName == game["awayTeam"]:
# 				homeScore = game["homeScore"]
# 				awayScore = game["awayScore"]
# 				if type(homeScore) != type(None) and type(awayScore) != type(None):
# 					if type(game["lines"][0]["spread"]) != type(None):
# 						# Tally ATS record
# 						if (homeScore + float(game["lines"][0]["spread"])) < awayScore:
# 							awayTrends["SpreadWins"] += 1
# 						elif (homeScore + float(game["lines"][0]["spread"])) > awayScore:
# 							awayTrends["SpreadLosses"] += 1
# 						else:
# 							awayTrends["SpreadTies"] += 1

# 					if type(game["lines"][0]["overUnder"]) != type(None):
# 						# Tally point total record
# 						if (homeScore + awayScore) < float(game["lines"][0]["overUnder"]):
# 							awayTrends["TotalOvers"] += 1
# 						elif (homeScore + awayScore) > float(game["lines"][0]["overUnder"]):
# 							awayTrends["TotalUnders"] += 1
# 						else:
# 							awayTrends["TotalTies"] += 1

# 		return awayTrends


# 	def calcBetTrends(self, homeTrends, awayTrends):
# 		betTrends = dict()
# 		betTrends["SpreadWins"] = homeTrends["SpreadWins"] + awayTrends["SpreadWins"]
# 		betTrends["SpreadLosses"] = homeTrends["SpreadLosses"] + awayTrends["SpreadLosses"]
# 		betTrends["SpreadTies"] = homeTrends["SpreadTies"] + awayTrends["SpreadTies"]
# 		betTrends["TotalOvers"] = homeTrends["TotalOvers"] + awayTrends["TotalOvers"]
# 		betTrends["TotalUnders"] = homeTrends["TotalUnders"] + awayTrends["TotalUnders"]
# 		betTrends["TotalTies"] = homeTrends["TotalTies"] + awayTrends["TotalTies"]

# 		return betTrends



# 	# NEED TO FIGURE OUT HOW BEST TO DO THIS
# 	# CURRENTLY I DO NOT ACCOUNT OR ADJUST FOR OPPONENT
# 	# Calculate overall team rating
# 	def calcTeamRating(self, teamOffRating, teamDefRating, teamSOR):
# 		# return ((teamOffRating * 1.05) - (teamDefRating * 0.95)) * teamSOR
# 		teamDiffRating = (teamOffRating * 1.1) - (teamDefRating * 0.9)
# 		return teamDiffRating * teamSOR * 5


# 	# Calculate offensive ranking based on explosiveness, success, 
# 	def calcOffRating(self, teamOffStats, teamDriveData, teamName):
# 		explosiveness = teamOffStats["explosiveness"] * self.explosiveness_weight
# 		success = teamOffStats["successRate"] * self.success_weight
# 		driveFinishing = self.calcOffPointsPer40Trip(teamDriveData, teamName) * self.driveFinishing_weight
# 		teamOffRating = explosiveness + success + driveFinishing
# 		return teamOffRating


# 	def calcDefRating(self, teamDefStats, teamDriveData, teamName):
# 		explosiveness = teamDefStats["explosiveness"] * self.explosiveness_weight
# 		success = teamDefStats["successRate"] * self.success_weight
# 		driveFinishing = self.calcDefPointsPer40Trip(teamDriveData, teamName) * self.driveFinishing_weight
# 		teamDefRating = explosiveness + success + driveFinishing
# 		return teamDefRating


# 	def calcOffPointsPer40Trip(self, teamDriveData, teamName):
# 		driveNum = 0
# 		points = 0
# 		for drive in teamDriveData:
# 			if drive["offense"] == teamName and drive["end_yardline"] <= 40:
# 				driveNum += 1
# 				if drive["scoring"] == "true":
# 					if drive["drive_result"] == "TD":
# 						points += 7
# 					elif drive["drive_result"] == "FG":
# 						points += 3
# 		# Calc points per drive here
# 		pointsPerTrip = points / driveNum
# 		return pointsPerTrip


# 	def calcDefPointsPer40Trip(self, teamDriveData, teamName):
# 		driveNum = 0
# 		points = 0
# 		for drive in teamDriveData:
# 			if drive["offense"] != teamName and drive["end_yardline"] <= 40:
# 				driveNum += 1
# 				if drive["scoring"] == "true":
# 					if drive["drive_result"] == "TD":
# 						points += 7
# 					elif drive["drive_result"] == "FG":
# 						points += 3
# 		# Calc points per drive here
# 		pointsPerTrip = points / driveNum
# 		return pointsPerTrip


# # Helper functions not part of a class
# def getStrengthOfRecord(dataInterface, teamName):
# 		dir_opponentList = dataInterface.getOpponents(teamName)
# 		# Get opponent's win percentage and indirect opponents list
# 		winPercent = 0
# 		# indir_opponentList = []
# 		for opponent in dir_opponentList:
# 			winPercent += dataInterface.getWinPercent(opponent)
# 			# indir_opponentList.extend(dataInterface.getOpponents(opponent))
# 		# Calculate first order win percentage
# 		if len(dir_opponentList) == 0:
# 			return 0
# 		else:
# 			oppWinPercent = winPercent / len(dir_opponentList)
# 			teamWinPercent = dataInterface.getWinPercent(teamName)

# 			sor = ((teamWinPercent * 0.8) + (oppWinPercent * 1.2)) / 2
# 			return sor



def main():
	data = infoRequest(2019)
	stats = calcStats()

	teams = data.teamNames(data.teamInfo())

	fbs_SOR = []
	for team in teams:
		fbs_SOR.append([team, getStrengthOfRecord(data, team)])

	fbs_SOR = sorted(fbs_SOR, key=lambda l:l[1], reverse=True)

	i = 0
	print("\n--- SoR Ranks ---")
	for team in fbs_SOR:
		i += 1
		if i > 5:
			break
		print(str(i) + ") " + team[0] + ": %4.3f" %(team[1]))


if __name__ == "__main__":
	main() 









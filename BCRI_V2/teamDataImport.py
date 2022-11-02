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

	def getTeams(self):
		try:
			api_instance = cfbd.TeamsApi(configuration)
			api_response = api_instance.get_fbs_teams(year=self.year)
			teamsData = pd.DataFrame.from_records([t.to_dict() for t in api_response])
			return teamsData
		except ApiException as e:
			print("Exception when calling TeamsApi->get_fbs_teams: %s\n" % e)

		# Get a team's advanced stats for the season
	def getGames(self):
		try:
			api_instance = cfbd.GamesApi(configuration)
			api_response = api_instance.get_games(year=self.year, season_type='both')
			gamesData = pd.DataFrame.from_records([g.to_dict() for g in api_response])
			# Filter out FCS opponent games and unplayed games
			teams = self.getTeams()
			teams = teams['school']
			gamesData = gamesData[(gamesData['home_team'].isin(teams)) & (gamesData['away_team'].isin(teams))]
			gamesData = gamesData[
			(gamesData['home_points'] == gamesData['home_points'])
			& (gamesData['away_points'] == gamesData['away_points'])
			& (pd.notna(gamesData['home_conference'])) 
			& (pd.notna(gamesData['away_conference']))
			]
			return gamesData
		except ApiException as e:
			print("Exception when calling GamesApi->get_games: %s\n" % e)
			return -1


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



class calcStats():

	def basicSRS(self, gamesData):
		# Set home field advantage to static 2.5 points for now
		gamesData['home_spread'] = np.where(gamesData['neutral_site'] == True, gamesData['home_points'] - gamesData['away_points'], (gamesData['home_points'] - gamesData['away_points'] - 2.5))
		gamesData['away_spread'] = -gamesData['home_spread']

		# Clean up data for team names and spreads
		teams = pd.concat([
			gamesData[['home_team', 'home_spread', 'away_team']].rename(columns={'home_team': 'team', 'home_spread': 'spread', 'away_team': 'opponent'}),
			gamesData[['away_team', 'away_spread', 'home_team']].rename(columns={'away_team': 'team', 'away_spread': 'spread', 'home_team': 'opponent'})
		])

		# Set maximum scoring margin to static 28 for now.
		teams['spread'] = np.where(teams['spread'] > 35, 35, teams['spread'])
		teams['spread'] = np.where(teams['spread'] < -35, -35, teams['spread'])

		# Get the mean spreads per team
		spreads = teams.groupby('team').spread.mean()

		# create empty arrays
		terms = []
		solutions = []

		for team in spreads.keys():
			row = []
			# get a list of team opponents
			opps = list(teams[teams['team'] == team]['opponent'])

			for opp in spreads.keys():
				if opp == team:
					# coefficient for the team should be 1
					row.append(1)
				elif opp in opps:
					# coefficient for opponents should be 1 over the number of opponents
					row.append(-1.0/len(opps))
				else:
					# teams not faced get a coefficient of 0
					row.append(0.000001)

			terms.append(row)

			# average game spread on the other side of the equation
			solutions.append(spreads[team])
		
		# Solve the system of equations here
		solutions = np.linalg.solve(np.array(terms), np.array(solutions))

		# Add team names back to a new dataframe
		ratings = list(zip(spreads.keys(), solutions))
		srs = pd.DataFrame(ratings, columns=['team', 'rating'])
		rankings = srs.sort_values('rating', ascending=False).reset_index()[['team', 'rating']]

		return rankings



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









# Christopher Brant
# Fall 2023 
# runApi.py
import dataImport as di
import threading
import pytz
from datetime import datetime
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS, cross_origin
	
app = Flask(__name__)

@app.route("/currGames")
@cross_origin(supports_credentials=True)
def getGameCards():
	gameCards = []
	for game in currWeekGamesOrdered:
		confStr = game.awayCon + " vs " + game.homeCon
		if len(game.lines) != 0:
			provider = game.lines[0].provider
			moneyline = game.lines[0].home_moneyline
			if (moneyline is not None) and (moneyline < 0):
				moneyline = game.awayTeamAbbr + " +" + (str(int(moneyline)))[1:]
			elif (moneyline is not None) and (moneyline > 0):
				moneyline = game.homeTeamAbbr + " +" + str(int(moneyline))
			# currSpread = game.lines[0].formatted_spread
			if (game.lines[0].spread is not None) and (game.lines[0].spread > 0):
				currSpread = game.awayTeamAbbr + " -" + str(game.lines[0].spread)
			elif (game.lines[0].spread is not None) and (game.lines[0].spread < 0): 
				currSpread = game.homeTeamAbbr + " " + str(game.lines[0].spread)
			elif game.lines[0].spread is None:
				currSpread = "N/A"
			if (game.lines[0].spread_open is not None) and (game.lines[0].spread_open > 0):
				openSpread = game.awayTeamAbbr + " -" + str(game.lines[0].spread_open)
			elif (game.lines[0].spread_open is not None) and (game.lines[0].spread_open < 0): 
				openSpread = game.homeTeamAbbr + " " + str(game.lines[0].spread_open)
			elif game.lines[0].spread_open is None:
				openSpread = "N/A"
			else:
				openSpread = "Pick 'em"
			if (game.lines[0].over_under_open is not None) and (game.lines[0].over_under is not None):
				currTotal = game.lines[0].over_under
				openTotal = game.lines[0].over_under_open
			else:
				currTotal = "N/A"
				openTotal = "N/A"
		else:
			provider = "N/A"
			openSpread = "N/A"
			currSpread = "N/A"
			currTotal = "N/A"
			openTotal = "N/A"
			moneyline = "N/A"	
		if game.homeLogo is not None:
			homeLogo = game.homeLogo
		else:
			homeLogo = "https://www.seekpng.com/png/full/140-1404801_ncaa-college-football-ncaa-football-logo.png"
		if game.awayLogo is not None:
			awayLogo = game.awayLogo
		else:
			homeLogo = "https://www.seekpng.com/png/full/140-1404801_ncaa-college-football-ncaa-football-logo.png"
		if (game.homePostWinProb) is not None:
			homePostWinProb = game.homePostWinProb
		else:
			homePostWinProb = 0.0
		if (game.awayPostWinProb) is not None:
			awayPostWinProb = game.awayPostWinProb
		else:
			awayPostWinProb = 0.0
		# Do string manipulation here to handle start time strings
		eastern = pytz.timezone('US/Eastern')
		startDate = datetime.fromisoformat(game.startDate.replace('Z', '+00:00'))
		startDateStr = startDate.strftime("%-m-%-d-%Y")
		if not startDate.time():
			startTimeStr = "TBD"
		else:
			startTimeStr = startDate.astimezone(eastern).strftime("%-I:%M %p")
		data = {
			'gameID': game.gameID,
			'homeTeam': game.homeTeam,
			'awayTeam': game.awayTeam,
			'homeTeamRank': game.homeTeamRank,
			'awayTeamRank': game.awayTeamRank,
			'homeLogo': homeLogo,
			'awayLogo': awayLogo,
			'homeAbbr': game.homeTeamAbbr,
			'awayAbbr': game.awayTeamAbbr,
			'homeAbbrRank': game.homeAbbrRank,
			'awayAbbrRank': game.awayAbbrRank,
			'homeRecord': game.homeTeamRecordTotal,
			'awayRecord': game.awayTeamRecordTotal,
			'conferences': confStr,
			'venue': game.venue,
			'location': game.location,
			'provider' : provider,
			'openSpread': openSpread,
			'currSpread': currSpread,
			'currTotal': currTotal,
			'openTotal': openTotal,
			'moneyline': moneyline,
			'homeWinProb': game.homeWinProb,
			'startTime': startTimeStr,
			'startDate': startDateStr,
			'completed': game.completed,
			'homePostWinProb': homePostWinProb,
			'awayPostWinProb': awayPostWinProb
		}
		gameCards.append(data)
	return jsonify(gameCards)

@app.route("/teamStatsDict")
@cross_origin(supports_credentials=True)
def getTeamStatsDict():
	data = teamStatsDict
	return jsonify(data)

@app.route("/teamStatsList")
@cross_origin(supports_credentials=True)
def getTeamStatsList():
	data = teamStatsList
	return jsonify(data)

@app.route("/reloadData")
@cross_origin(supports_credentials=True)
def reloadDataEndpoint():
	print("Reloading api data")
	global currWeekGamesOrdered
	global teamStatsDict
	global teamStatsList
	global currDate
	global currWeek
	teamStatsList = []
	currDate = datetime.now()
	currWeek = di.getCurrWeek()
	teamStatsDict = di.getTeamAdvStats()
	for key in teamStatsDict:
		teamStatsList.append({"team": key, "stats": teamStatsDict[key]})
	currWeekGamesOrdered = di.matchupListAggregator(currWeek)
	return "Data Reloaded"

@app.route("/reloadTest")
@cross_origin(supports_credentials=True)
def reloadTest():
	return str(currDate)

def loadApiData():
	global currWeekGamesOrdered
	global teamStatsDict
	global teamStatsList
	global currWeek
	teamStatsDict = di.getTeamAdvStats()
	teamStatsList = []
	for key in teamStatsDict:
		teamStatsList.append({"team": key, "stats": teamStatsDict[key]})
	currWeek = di.getCurrWeek()
	currWeekGamesOrdered = di.matchupListAggregator(currWeek)

def reloadApiData():
	print("Reloading api data")
	global currWeekGamesOrdered
	global teamStatsDict
	global teamStatsList
	global currDate
	global currWeek
	teamStatsList = []
	currDate = datetime.now()
	currWeek = di.getCurrWeek()
	teamStatsDict = di.getTeamAdvStats()
	for key in teamStatsDict:
		teamStatsList.append({"team": key, "stats": teamStatsDict[key]})
	currWeekGamesOrdered = di.matchupListAggregator(currWeek)
	threading.Timer(86400, loadApiData).start()

def runApiApp():
	app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))

if __name__ == '__main__':
	loadApiData()
	dataReloadThread = threading.Thread(target=reloadApiData)
	dataReloadThread.start()

	flaskThread = threading.Thread(target=runApiApp)
	flaskThread.start()

	flaskThread.join()
	dataReloadThread.join()



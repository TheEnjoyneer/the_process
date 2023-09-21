# Christopher Brant
# Fall 2023 
# runTest.py
# testing functions and scripting for dataImport.py
import dataImport as di
import sys
import getopt
import argparse
from flask import Flask, jsonify 
from flask_cors import CORS, cross_origin
from markupsafe import escape

app = Flask(__name__)

# Return total number of games for this week
@app.route("/numGames")
@cross_origin(supports_credentials=True)
def getNumGames():
	data = {
		'numGames': len(weekGamesOrdered)
	}
	return jsonify(data)

@app.route("/gameCards")
@cross_origin(supports_credentials=True)
def getGameCards():
	gameCards = []
	for game in weekGamesOrdered:
		matchupStr = game.awayTeamRank + " at " + game.homeTeamRank
		confStr = game.awayCon + " vs " + game.homeCon
		if len(game.lines) != 0:
			provider = game.lines[0].provider
			moneyline = game.lines[0].home_moneyline
			currSpread = game.lines[0].formatted_spread
			if game.lines[0].spread_open > 0:
				openSpread = game.awayTeam + " -" + str(game.lines[0].spread_open)
			elif game.lines[0].spread_open < 0: 
				openSpread = game.homeTeam + " " + str(game.lines[0].spread_open)
			else:
				openSpread = "Pick 'em"
			if (game.lines[0].over_under_open is not None) and (game.lines[0].over_under is not None):
				currTotal = game.lines[0].over_under
				openTotal = game.lines[0].over_under_open
			else:
				currTotal = None
				openTotal = None
		else:
			provider = "N/A"
			openSpread = "N/A"
			currSpread = "N/A"
			currTotal = "N/A"
			openTotal = "N/A"
			moneyline = "N/A"	
		data = {
			'gameID': game.gameID,
			'matchup': matchupStr,
			'conferences': confStr,
			'venue': game.venue,
			'provider' : provider,
			'openSpread': openSpread,
			'currSpread': currSpread,
			'currTotal': currTotal,
			'openTotal': openTotal,
			'moneyline': moneyline 
		}
		gameCards.append(data)
	return jsonify(gameCards)

if __name__ == '__main__':
	# Create ordered games data on server side
	weekGamesOrdered = di.matchupListAggregator(di.getCurrWeek())
	app.run()


'''
# Use first command line arg for weekNum
weekNum = sys.argv[1]
weekGamesOrdered = di.matchupListAggregator(int(weekNum))

for game in weekGamesOrdered:
	game.printLines()
'''



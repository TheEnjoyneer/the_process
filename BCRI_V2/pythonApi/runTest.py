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



app = Flask(__name__)

@app.route("/topGame")
@cross_origin(supports_credentials=True)
def getTopGame():
	matchupStr = weekGamesOrdered[0].awayTeamRank + " at " + weekGamesOrdered[0].homeTeamRank
	confStr = weekGamesOrdered[0].awayCon + " vs " + weekGamesOrdered[0].homeCon
	data = {
		'matchup': matchupStr,
		'conferences': confStr,
		'venue': weekGamesOrdered[0].venue
	}
	return jsonify(data)

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



# cfbStatsLib.py

import json
import pytz
import random
import warnings
from datetime import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

warnings.filterwarnings("ignore")

endpoint = "https://graphql.collegefootballdata.com/v1/graphql"
headers = {
    "Authorization": "Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9",
    "Content-Type": "application/json"
    }
timezone = pytz.timezone('America/New_York')

# Library functions for internal use definitions here
def createClient():
    transport = AIOHTTPTransport(url=endpoint, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)

# Come back and update watchability score metric based on old algo
def calcWatchabilityScore(game):
    return random.randint(1,100)

def calcWatchabilityScores(gameList):
    for i in range(len(gameList['game'])):
        gameList['game'][i]['watchability'] = calcWatchabilityScore(result['game'][i])
    return gameList


# CFB Data API related function definitions here

def getLiveScores(seasonYear, weekNum):
    return 0

def getCalendarWeekReg(seasonYear, weekNum):
    client = createClient()

    queryStr = """
    query getCalendarWeek($seasonYear: smallint!, $weekNum: smallint!, $seasonType: season_type!) {
        game(
            where: {
                season: { _eq: $seasonYear }
                week: { _eq: $weekNum }
                seasonType: { _eq: $seasonType }
                _or: {
                    homeClassification: { _eq: "fbs" }
                    awayClassification: { _eq: "fbs" }
                }
            }
            orderBy: { startDate: ASC }
        ) {
            attendance
            awayClassification
            awayConference
            awayConferenceId
            awayEndElo
            awayLineScores
            awayPoints
            awayPostgameWinProb
            awayStartElo
            awayTeam
            awayTeamId
            conferenceGame
            excitement
            homeConference
            homeConferenceId
            homeEndElo
            homeLineScores
            homePoints
            homePostgameWinProb
            homeStartElo
            homeTeam
            homeTeamId
            id
            neutralSite
            notes
            season
            seasonType
            startDate
            startTimeTbd
            status
            venueId
            week
            homeClassification
        }
    }
    """

    query = gql(queryStr)

    variables = {
        "seasonYear": seasonYear,
        "weekNum": weekNum,
        "seasonType": "regular"
    }

    # Grab all games, add watchability score calc, and sort by times and watchability
    result = client.execute(query, variable_values=variables)
    gamesWatch = calcWatchabilityScores(result)
    gameList = sorted(gamesWatch['game'], key=lambda x: x['watchability'])

    weekNights = []         # Anything before saturday at noon eastern
    saturdayEarly = []      # Anything saturday before 3 eastern
    saturdayAfternoon = []  # Anything saturday before 7 eastern
    saturdayEvening = []    # Anything saturday before 10 eastern
    saturdayLate = []       # Anything leftover
    extraNights = []
    weeknightOpts = ["Tuesday", "Wednesday", "Thursday", "Friday"]
    for game in gamesList['game']:
        currTime = datetime.strptime(game['startDate'], '%Y-%m-%dT%H:%M:%S')
        localTime = currTime.astimezone(timezone)
        localHour = localTime.strftime('%H')
        localDay = localTime.strftime('%A')

        if (localDay != "Saturday") and (localDay in weeknightOpts):
            weekNights.append(game)
        elif (localDay == "Saturday") and (int(localHour) < 15):
            saturdayEarly.append(game)
        elif (localDay == "Saturday") and (int(localHour) < 19):
            saturdayAfternoon.append(game)
        elif (localDay == "Saturday") and (int(localHour) < 22):
            saturdayEvening.append(game)
        elif (localDay == "Saturday") and (int(localHour) >= 22):
            saturdayLate.append(game)
        elif (localDay == "Sunday") and (int(localHour) < 8):
            saturdayLate.append(game)
        else:
            extraNights.append(game)

    weekSlate = [weekNights, saturdayEarly, saturdayAfternoon, saturdayEvening, saturdayLate, extraNights]

    return weekSlate


def getCalendarWeekPost(seasonYear):
    client = createClient()

    queryStr = """
    query getCalendarWeek($seasonYear: smallint!, $weekNum: smallint!, $seasonType: season_type!) {
        game(
            where: {
                season: { _eq: $seasonYear }
                week: { _eq: $weekNum }
                seasonType: { _eq: $seasonType }
                _or: {
                    homeClassification: { _eq: "fbs" }
                    awayClassification: { _eq: "fbs" }
                }
            }
            orderBy: { startDate: ASC }
        ) {
            attendance
            awayClassification
            awayConference
            awayConferenceId
            awayEndElo
            awayLineScores
            awayPoints
            awayPostgameWinProb
            awayStartElo
            awayTeam
            awayTeamId
            conferenceGame
            excitement
            homeConference
            homeConferenceId
            homeEndElo
            homeLineScores
            homePoints
            homePostgameWinProb
            homeStartElo
            homeTeam
            homeTeamId
            id
            neutralSite
            notes
            season
            seasonType
            startDate
            startTimeTbd
            status
            venueId
            week
            homeClassification
        }
    }
    """

    query = gql(queryStr)

    variables = {
        "seasonYear": seasonYear,
        "weekNum": 1,
        "seasonType": "postseason"
    }

    # Grab all games, add watchability score calc, and sort by times and watchability
    result = client.execute(query, variable_values=variables)
    gamesWatch = calcWatchabilityScores(result)
    gameList = sorted(gamesWatch['game'], key=lambda x: x['watchability'])

    # TODO: ADD ORGANIZATION FOR CALENDAR IN THE POSTSEASON TO SHOW GAMES
    # AT THE RIGHT TIMES AND IN THE RIGHT WEEKS


def getTeamMetrics(seasonYear, team):
    return 0


def getGameModalMetrics(game):
    return 0


def getGameDetailMetrics(game):
    return 0


def getTeamFullSeasonInfo(seasonYear, team):
    return 0










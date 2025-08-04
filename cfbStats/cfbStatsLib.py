# cfbStatsLib.py

import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

endpoint = "https://graphql.collegefootballdata.com/v1/graphql"
headers = {
    "Authorization": "Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9",
    "Content-Type": "application/json"
    }

# Library functions for internal use definitions here
def createClient():
    transport = AIOHTTPTransport(url=endpoint, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)

def calcWatchabilityScore(game):
    return 0


# CFB Data API related function definitions here

def getCalendarWeek(seasonYear, weekNum, seasonType):
    client = createClient()

    queryStr = """
    query getCalendarWeek($seasonYear: smallint!, $weekNum: smallint!, $seasonType: String!) {
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
        "seasonType": seasonType
    }

    result = client.execute(query, variable_values=variables)


    # COME BACK AND HAVE WATCHABILITY SCORE ADDED TO EACH GAME'S RESPONSE


    return result


def getTeamMetrics(seasonYear, team):
    return 0


def getGameModalMetrics(game):
    return 0


def getGameDetailMetrics(game):
    return 0


def getTeamFullSeasonInfo(seasonYear, team):
    return 0










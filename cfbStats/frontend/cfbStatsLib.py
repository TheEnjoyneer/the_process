# cfbStatsLib.py

import json
import pytz
import random
import warnings
import requests
from datetime import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

warnings.filterwarnings("ignore")

endpoint = "https://graphql.collegefootballdata.com/v1/graphql"
headers = {
    "Authorization": "Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9",
    "Content-Type": "application/json"
    }
# Note: Frontend will handle timezone conversion to user's local timezone
# This timezone is only used for backend organization if needed
timezone = pytz.timezone('America/New_York')

# Library functions for internal use definitions here
def createClient():
    transport = AIOHTTPTransport(url=endpoint, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)

def calcWatchabilityScore(game):
    """
    Calculate a watchability score (1-100) based on:
    1. ELO rating closeness (closer = more exciting)
    2. ELO rating magnitude (higher = more exciting, max 2200)
    3. Over/Under total (higher = more exciting)
    4. Spread closeness (closer = more exciting)
    """
    score = 0
    
    # 1. ELO Rating Component (40% weight)
    home_elo = game.get('homeStartElo', 1500)
    away_elo = game.get('awayStartElo', 1500)
    
    if home_elo is not None and away_elo is not None:
        # Calculate ELO closeness (0-100)
        elo_diff = abs(home_elo - away_elo)
        elo_closeness = max(0, 100 - (elo_diff / 20))  # 0 diff = 100, 2000 diff = 0
        
        # Calculate ELO magnitude bonus (0-30)
        avg_elo = (home_elo + away_elo) / 2
        elo_magnitude = min(30, max(0, (avg_elo - 1500) / 23.33))  # 1500 = 0, 2200 = 30
        
        elo_score = elo_closeness + elo_magnitude
        score += elo_score * 0.4  # 40% weight
    else:
        # Default ELO score if data missing
        score += 50 * 0.4
    
    # 2. Over/Under Component (30% weight)
    over_under = None
    if game.get('lines') and len(game['lines']) > 0:
        # Use the first available line's over/under
        over_under = game['lines'][0].get('overUnder')
    
    if over_under is not None:
        # Higher over/under = more exciting (0-100)
        # Range: 30-80 points (typical CFB range)
        ou_score = min(100, max(0, (over_under - 30) * 2))  # 30 = 0, 80 = 100
        score += ou_score * 0.3  # 30% weight
    else:
        # Default over/under score if data missing
        score += 30 * 0.3
    
    # 3. Spread Component (30% weight)
    spread = None
    if game.get('lines') and len(game['lines']) > 0:
        # Use the first available line's spread
        spread = game['lines'][0].get('spread')
    
    if spread is not None:
        # Closer spread = more exciting (0-100)
        # Range: 0-35 points
        spread_score = max(0, 100 - (abs(spread) * 2.86))  # 0 = 100, 35 = 0
        score += spread_score * 0.3  # 30% weight
    else:
        # Default spread score if data missing
        score += 30 * 0.3
    
    # 4. Conference Component (10% weight) - Power 5 conference bonus
    power5_conferences = ["SEC", "Big Ten", "Big 12", "ACC"]
    away_conference = game.get('awayConference', '')
    home_conference = game.get('homeConference', '')
    
    conference_bonus = 0
    if away_conference in power5_conferences or home_conference in power5_conferences:
        conference_bonus = 50  # Bump for Power 5 teams
    
    score += conference_bonus * 0.3  # 30% weight
    
    # Ensure score is between 1-100
    final_score = max(1, min(100, round(score)))
    
    return final_score

def calcWatchabilityScores(gamesList):
    for i in range(len(gamesList['game'])):
        gamesList['game'][i]['watchability'] = calcWatchabilityScore(gamesList['game'][i])
    return gamesList


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
            homeClassification: { _eq: "fbs" }
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
        homeClassification
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
        weather {
            dewpoint
            gameId
            humidity
            precipitation
            pressure
            snowfall
            temperature
            weatherConditionCode
            windDirection
            windGust
            windSpeed
        }
        lines {
            gameId
            linesProviderId
            moneylineAway
            moneylineHome
            overUnder
            overUnderOpen
            spread
            spreadOpen
        }
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
    gamesList = sorted(gamesWatch['game'], key=lambda x: x['watchability'], reverse=True)

    weekNights = []         # Anything before saturday at noon eastern
    saturdayEarly = []      # Anything saturday before 3 eastern
    saturdayAfternoon = []  # Anything saturday before 7 eastern
    saturdayEvening = []    # Anything saturday before 10 eastern
    saturdayLate = []       # Anything leftover
    extraNights = []
    # Note: Frontend will handle timezone conversion and organization
    # For now, we'll organize based on UTC time to maintain consistency
    # The frontend will convert to local time for display and re-organize as needed
    weeknightOpts = ["Tuesday", "Wednesday", "Thursday", "Friday"]
    for game in gamesList:
        # Parse UTC time and convert to Eastern for organization (backend logic)
        # Frontend will handle local timezone conversion for display
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
            homeClassification: { _eq: "fbs" }
        }
    ) { attendance
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
        homeClassification
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
        lines {
            gameId
            linesProviderId
            moneylineAway
            moneylineHome
            overUnder
            overUnderOpen
            spread
            spreadOpen
        }
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
    gamesList = sorted(gamesWatch['game'], key=lambda x: x['watchability'], reverse=True)

    # TODO: ADD ORGANIZATION FOR CALENDAR IN THE POSTSEASON TO SHOW GAMES
    # AT THE RIGHT TIMES AND IN THE RIGHT WEEKS
    return gamesList

def getTeamInfo(teamId):
    """
    Get comprehensive team/school information for a given team ID.
    
    Args:
        teamId (int): The team ID to get information for
        
    Returns:
        dict: Team information including school details, conference, location, etc.
    """
    client = createClient()
    
    # Query for current team information
    queryStr = """
    query getTeamInfo($teamId: Int!) {
        currentTeams(
            where: { teamId: { _eq: $teamId } }
        ) {
            teamId
            team
            school
            mascot
            abbreviation
            conference
            conferenceId
            division
            color
            altColor
            logos
            twitter
            locationCity
            locationState
            locationCountry
            latitude
            longitude
            timezone
            venueId
            venue
            capacity
            surface
            yearBuilt
            dome
            city
            state
            zip
            country
            timezone
            elevation
            capacity
            surface
            yearBuilt
            dome
        }
    }
    """
    
    query = gql(queryStr)
    
    variables = {
        "teamId": teamId
    }
    
    try:
        result = client.execute(query, variable_values=variables)
        
        if result and result.get('currentTeams') and len(result['currentTeams']) > 0:
            team_info = result['currentTeams'][0]
            
            # Also get historical team data for additional context
            historical_query = """
            query getHistoricalTeamInfo($teamId: Int!) {
                historicalTeam(
                    where: { teamId: { _eq: $teamId } }
                    orderBy: { year: DESC }
                    limit: 1
                ) {
                    teamId
                    team
                    school
                    conference
                    division
                    year
                    wins
                    losses
                    ties
                    pct
                    srs
                    spOverall
                    spOffense
                    spDefense
                    pointsFor
                    pointsAgainst
                }
            }
            """
            
            historical_query_gql = gql(historical_query)
            historical_result = client.execute(historical_query_gql, variable_values=variables)
            
            if historical_result and historical_result.get('historicalTeam') and len(historical_result['historicalTeam']) > 0:
                team_info['historical'] = historical_result['historicalTeam'][0]
            
            return team_info
        else:
            return {
                "error": f"No team found with ID {teamId}",
                "teamId": teamId
            }
            
    except Exception as e:
        return {
            "error": f"Error fetching team info: {str(e)}",
            "teamId": teamId
        }

def getTeamInfoByName(teamName):
    """
    Get team information by team name.
    
    Args:
        teamName (str): The team name to search for
        
    Returns:
        dict: Team information or error message
    """
    client = createClient()
    
    queryStr = """
    query getTeamInfoByName($teamName: String!) {
        currentTeams(
            where: { team: { _ilike: $teamName } }
        ) {
            teamId
            team
            school
            mascot
            abbreviation
            conference
            conferenceId
            division
            color
            altColor
            logos
            twitter
            locationCity
            locationState
            locationCountry
            latitude
            longitude
            timezone
            venueId
            venue
            capacity
            surface
            yearBuilt
            dome
            city
            state
            zip
            country
            elevation
        }
    }
    """
    
    query = gql(queryStr)
    
    variables = {
        "teamName": f"%{teamName}%"
    }
    
    try:
        result = client.execute(query, variable_values=variables)
        
        if result and result.get('currentTeams') and len(result['currentTeams']) > 0:
            return result['currentTeams']
        else:
            return {
                "error": f"No team found with name containing '{teamName}'",
                "searchTerm": teamName
            }
            
    except Exception as e:
        return {
            "error": f"Error fetching team info: {str(e)}",
            "searchTerm": teamName
        }

def getAllTeams():
    """
    Get all current FBS teams.
    
    Returns:
        list: List of all current teams with basic information
    """
    client = createClient()
    
    queryStr = """
    query getAllTeams {
        currentTeams(
            where: { division: { _eq: "fbs" } }
            orderBy: { team: ASC }
        ) {
            teamId
            team
            school
            abbreviation
            conference
            division
            color
            altColor
            locationCity
            locationState
        }
    }
    """
    
    query = gql(queryStr)
    
    try:
        result = client.execute(query)
        
        if result and result.get('currentTeams'):
            return result['currentTeams']
        else:
            return {
                "error": "No teams found",
                "teams": []
            }
            
    except Exception as e:
        return {
            "error": f"Error fetching teams: {str(e)}",
            "teams": []
        }

def getGameLines(gameId):
    """
    Get betting lines and odds for a specific game by game ID.
    
    Args:
        gameId (int): The game ID to get betting lines for
        
    Returns:
        dict: Game lines information including spreads, totals, money lines, etc.
    """
    client = createClient()
    
    # Query for game lines and betting information
    queryStr = """
    query getGameLines($gameId: Int!) {
        gameLines(
            where: { gameId: { _eq: $gameId } }
        ) {
            gameId
            linesProviderId
            moneylineAway
            moneylineHome
            overUnder
            overUnderOpen
            spread
            spreadOpen
        }
    }
    """
    
    query = gql(queryStr)
    
    variables = {
        "gameId": gameId
    }
    
    try:
        result = client.execute(query, variable_values=variables)
        
        if result:
            game_lines = result.get('gameLines', [])
            game_info = result.get('games', [])
            
            # Organize the response
            response = {
                "gameId": gameId,
                "gameInfo": game_info[0] if game_info else None,
                "bettingLines": game_lines,
                "lineCount": len(game_lines)
            }
            
            # Add summary statistics if lines exist
            if game_lines:
                # Get the most recent line from each provider
                providers = {}
                for line in game_lines:
                    provider = line.get('provider')
                    if provider not in providers or line.get('updated', '') > providers[provider].get('updated', ''):
                        providers[provider] = line
                
                response["latestLines"] = list(providers.values())
                response["providers"] = list(providers.keys())
                
                # Calculate average spreads and totals
                spreads = [line.get('homeSpread') for line in game_lines if line.get('homeSpread') is not None]
                totals = [line.get('overUnder') for line in game_lines if line.get('overUnder') is not None]
                
                if spreads:
                    response["averageSpread"] = sum(spreads) / len(spreads)
                if totals:
                    response["averageTotal"] = sum(totals) / len(totals)
            
            return response
        else:
            return {
                "error": f"No game lines found for game ID {gameId}",
                "gameId": gameId
            }
            
    except Exception as e:
        return {
            "error": f"Error fetching game lines: {str(e)}",
            "gameId": gameId
        }


# ALL getGameLinesByTeams functionality is not working as designed yet
def getGameLinesByTeams(awayTeam, homeTeam, seasonYear=None, week=None):
    """
    Get betting lines for a game by team names and optionally season/week.
    
    Args:
        awayTeam (str): Away team name
        homeTeam (str): Home team name
        seasonYear (int, optional): Season year to filter by
        week (int, optional): Week number to filter by
        
    Returns:
        dict: Game lines information
    """
    client = createClient()
    
    # Build the where clause for the game query
    gameWhere = f'awayTeam: {{ _eq: "{awayTeam}" }}, homeTeam: {{ _eq: "{homeTeam}" }}'
    if seasonYear:
        gameWhere += f', season: {{ _eq: {seasonYear} }}'
    if week:
        gameWhere += f', week: {{ _eq: {week} }}'
    
    queryStr = f"""
    query getGameLinesByTeams {{
        games(
            where: {{ {gameWhere} }}
            limit: 1
        ) {{
            id
            awayTeam
            homeTeam
            startDate
            season
            week
            seasonType
            status
        }}
    }}
    """
    
    query = gql(queryStr)
    
    try:
        result = client.execute(query)
        
        if result and result.get('games') and len(result['games']) > 0:
            game = result['games'][0]
            # Use the found game ID to get the lines
            return getGameLines(game['id'])
        else:
            return {
                "error": f"No game found between {awayTeam} and {homeTeam}",
                "awayTeam": awayTeam,
                "homeTeam": homeTeam,
                "seasonYear": seasonYear,
                "week": week
            }
            
    except Exception as e:
        return {
            "error": f"Error fetching game lines by teams: {str(e)}",
            "awayTeam": awayTeam,
            "homeTeam": homeTeam
        }

def getVenueInfo(venueId):
    """
    Get comprehensive venue information for a given venue ID using the REST API.
    
    Args:
        venueId (int): The venue ID to get information for
        
    Returns:
        dict: Venue information including name, location, capacity, surface, etc.
    """
    # REST API endpoint for venues
    api_url = f"https://api.collegefootballdata.com/venues"
    headers = {'Authorization': 'Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'}
    
    try:
        # Make GET request to the venues endpoint
        response = requests.get(api_url, timeout=10, headers=headers)
        
        if response.status_code == 200:
            venues = response.json()
            
            # Find the venue with matching ID
            venue = None
            for v in venues:
                if v.get('id') == venueId:
                    venue = v
                    break
            
            if venue:
                # Add computed fields for convenience
                venue['fullAddress'] = f"{venue.get('address', '')}, {venue.get('city', '')}, {venue.get('state', '')} {venue.get('zip', '')}".strip()
                venue['locationString'] = f"{venue.get('city', '')}, {venue.get('state', '')}"
                
                # Format capacity with commas
                if venue.get('capacity'):
                    venue['formattedCapacity'] = f"{venue['capacity']:,}"
                
                # Add venue type classification
                venue['venueType'] = 'Dome' if venue.get('dome') else 'Outdoor'
                if venue.get('roofType'):
                    venue['venueType'] = venue['roofType']
                
                return venue
            else:
                return {
                    "error": f"No venue found with ID {venueId}",
                    "venueId": venueId
                }
        else:
            return {
                "error": f"API request failed with status code {response.status_code}",
                "venueId": venueId
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Network error fetching venue info: {str(e)}",
            "venueId": venueId
        }
    except Exception as e:
        return {
            "error": f"Error fetching venue info: {str(e)}",
            "venueId": venueId
        }

def getVenueInfoByName(venueName):
    """
    Get venue information by venue name (supports partial matches) using the REST API.
    
    Args:
        venueName (str): The venue name to search for
        
    Returns:
        dict: Venue information or error message
    """
    # REST API endpoint for venues
    api_url = f"https://api.collegefootballdata.com/venues"
    headers = {'Authorization': 'Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'}
    
    try:
        # Make GET request to the venues endpoint
        response = requests.get(api_url, timeout=10, headers=headers)
        
        if response.status_code == 200:
            all_venues = response.json()
            
            # Filter venues by name (case-insensitive partial match)
            matching_venues = []
            venue_name_lower = venueName.lower()
            
            for venue in all_venues:
                if venue.get('name') and venue_name_lower in venue['name'].lower():
                    # Add computed fields to each venue
                    venue['fullAddress'] = f"{venue.get('address', '')}, {venue.get('city', '')}, {venue.get('state', '')} {venue.get('zip', '')}".strip()
                    venue['locationString'] = f"{venue.get('city', '')}, {venue.get('state', '')}"
                    
                    if venue.get('capacity'):
                        venue['formattedCapacity'] = f"{venue['capacity']:,}"
                    
                    venue['venueType'] = 'Dome' if venue.get('dome') else 'Outdoor'
                    if venue.get('roofType'):
                        venue['venueType'] = venue['roofType']
                    
                    matching_venues.append(venue)
            
            # Sort by name
            matching_venues.sort(key=lambda x: x.get('name', ''))
            
            if matching_venues:
                return {
                    "venues": matching_venues,
                    "count": len(matching_venues),
                    "searchTerm": venueName
                }
            else:
                return {
                    "error": f"No venues found with name containing '{venueName}'",
                    "searchTerm": venueName,
                    "venues": []
                }
        else:
            return {
                "error": f"API request failed with status code {response.status_code}",
                "searchTerm": venueName,
                "venues": []
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Network error fetching venue info: {str(e)}",
            "searchTerm": venueName,
            "venues": []
        }
    except Exception as e:
        return {
            "error": f"Error fetching venue info: {str(e)}",
            "searchTerm": venueName,
            "venues": []
        }

def getAllVenues():
    """
    Get all venues using the REST API.
    
    Returns:
        list: List of all venues with basic information
    """
    # REST API endpoint for venues
    api_url = f"https://api.collegefootballdata.com/venues"
    headers = {'Authorization': 'Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'}
    
    try:
        # Make GET request to the venues endpoint
        response = requests.get(api_url, timeout=10, headers=headers)
        
        if response.status_code == 200:
            venues = response.json()
            
            # Add computed fields
            for venue in venues:
                venue['locationString'] = f"{venue.get('city', '')}, {venue.get('state', '')}"
                if venue.get('capacity'):
                    venue['formattedCapacity'] = f"{venue['capacity']:,}"
                venue['venueType'] = 'Dome' if venue.get('dome') else 'Outdoor'
                if venue.get('roofType'):
                    venue['venueType'] = venue['roofType']
            
            # Sort by name
            venues.sort(key=lambda x: x.get('name', ''))
            
            return venues
        else:
            return {
                "error": f"API request failed with status code {response.status_code}",
                "venues": []
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Network error fetching venues: {str(e)}",
            "venues": []
        }
    except Exception as e:
        return {
            "error": f"Error fetching venues: {str(e)}",
            "venues": []
        }

def getRankings(seasonYear, weekNum):
    """
    Get current rankings for the specified season and week.
    Prioritizes CFP committee rankings when available, falls back to AP poll.
    
    Args:
        seasonYear (int): The season year
        weekNum (int): The week number
        
    Returns:
        dict: Rankings data with team rankings
    """
    headers = {'Authorization': 'Bearer pCTgkDkbCkcTh4OWrzO4ph5+/VR/5Fp98y4ORuZCbiG0HKTXt+8Xbs88IfVu4lK9'}
    
    try:
        # First try to get CFP committee rankings
        url = f"https://api.collegefootballdata.com/rankings"
        params = {
            'year': seasonYear,
            'week': weekNum,
            'seasonType': 'regular'
        }
        
        response = requests.get(url, params=params, timeout=10, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            #print(data[0]['polls'])
            # Look for CFP committee rankings
            for poll in data[0]['polls']:
                pollType = str(poll.get('poll'))
                if pollType == "Playoff Committee Rankings":
                    return poll['ranks']
                elif pollType == "AP Top 25":
                    return poll['ranks']
    except requests.exceptions.RequestException as e:
        return {
            'error': f"Network error fetching rankings: {str(e)}",
            'type': 'Error',
            'rankings': {}
        }
    except Exception as e:
        return {
            'error': f"Error fetching rankings: {str(e)}",
            'type': 'Error',
            'rankings': {}
        }

def getTeamMetrics(seasonYear, team):
    return 0


def getGameModalMetrics(game):
    return 0


def getGameDetailMetrics(game):
    return 0


def getTeamFullSeasonInfo(seasonYear, team):
    return 0










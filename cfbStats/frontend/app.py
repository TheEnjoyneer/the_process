from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os
import json
from datetime import datetime
import cfbStatsLib as api

# Global cache for games data, game lines, and venues
games_cache = {}
game_lines_cache = {}
venues_cache = {}
cache_expiry = 10 * 60  # 10 minutes in seconds

def get_cache_key(season_year, week_num, season_type):
    """Generate a cache key for games data"""
    return f"{season_type}_{season_year}_{week_num}"

def get_cached_games(season_year, week_num, season_type):
    """Get cached games data if available and not expired"""
    cache_key = get_cache_key(season_year, week_num, season_type)
    if cache_key in games_cache:
        cached_data = games_cache[cache_key]
        if (datetime.now() - cached_data['timestamp']).total_seconds() < cache_expiry:
            # Also ensure lines data is cached for each game
            if 'game' in cached_data['data'] and cached_data['data']['game']:
                for game in cached_data['data']['game']:
                    if 'lines' in game and game['lines'] and game['id']:
                        # Ensure lines data is cached for this game
                        if not get_cached_game_lines(game['id']):
                            formatted_lines_data = {
                                'gameId': game['id'],
                                'bettingLines': game['lines'],
                                'latestLines': game['lines'],
                                'lineCount': len(game['lines']),
                                'cached_from_games': True,
                                'providers': list(set(line.get('provider', 'Unknown') for line in game['lines']))
                            }
                            
                            # Add average calculations
                            spreads = [line.get('spread') for line in game['lines'] if line.get('spread') is not None]
                            totals = [line.get('overUnder') for line in game['lines'] if line.get('overUnder') is not None]
                            
                            if spreads:
                                formatted_lines_data['averageSpread'] = sum(spreads) / len(spreads)
                            if totals:
                                formatted_lines_data['averageTotal'] = sum(totals) / len(totals)
                            
                            set_cached_game_lines(game['id'], formatted_lines_data)
            
            return cached_data['data']
    return None

def set_cached_games(season_year, week_num, season_type, data):
    """Cache games data with timestamp and extract lines data"""
    cache_key = get_cache_key(season_year, week_num, season_type)
    
    # Extract lines data from games and cache them separately
    if 'game' in data and data['game']:
        for game in data['game']:
            if 'lines' in game and game['lines'] and game['id']:
                # Format lines data for caching
                formatted_lines_data = {
                    'gameId': game['id'],
                    'bettingLines': game['lines'],
                    'latestLines': game['lines'],  # Use the same data for latest lines
                    'lineCount': len(game['lines']),
                    'cached_from_games': True,
                    'providers': list(set(line.get('provider', 'Unknown') for line in game['lines']))
                }
                
                # Add average calculations if lines exist
                spreads = [line.get('spread') for line in game['lines'] if line.get('spread') is not None]
                totals = [line.get('overUnder') for line in game['lines'] if line.get('overUnder') is not None]
                
                if spreads:
                    formatted_lines_data['averageSpread'] = sum(spreads) / len(spreads)
                if totals:
                    formatted_lines_data['averageTotal'] = sum(totals) / len(totals)
                
                # Cache lines data for each game
                set_cached_game_lines(game['id'], formatted_lines_data)
    
    games_cache[cache_key] = {
        'data': data,
        'timestamp': datetime.now()
    }

def get_cached_game_lines(game_id):
    """Get cached game lines data if available and not expired"""
    if game_id in game_lines_cache:
        cached_data = game_lines_cache[game_id]
        if (datetime.now() - cached_data['timestamp']).total_seconds() < cache_expiry:
            return cached_data['data']
    return None

def set_cached_game_lines(game_id, data):
    """Cache game lines data with timestamp"""
    game_lines_cache[game_id] = {
        'data': data,
        'timestamp': datetime.now()
    }

def get_cached_venue(venue_id):
    """Get cached venue data if available and not expired"""
    if venue_id in venues_cache:
        cached_data = venues_cache[venue_id]
        if (datetime.now() - cached_data['timestamp']).total_seconds() < cache_expiry:
            return cached_data['data']
    return None

def set_cached_venue(venue_id, data):
    """Cache venue data with timestamp"""
    venues_cache[venue_id] = {
        'data': data,
        'timestamp': datetime.now()
    }

def get_cached_all_venues():
    """Get cached all venues data if available and not expired"""
    if 'all_venues' in venues_cache:
        cached_data = venues_cache['all_venues']
        if (datetime.now() - cached_data['timestamp']).total_seconds() < cache_expiry:
            return cached_data['data']
    return None

def set_cached_all_venues(data):
    """Cache all venues data with timestamp"""
    venues_cache['all_venues'] = {
        'data': data,
        'timestamp': datetime.now()
    }

def load_and_cache_all_venues():
    """Load all venues and cache them for quick lookup"""
    try:
        print("Loading all venues for caching...")
        all_venues = api.getAllVenues()
        
        if all_venues and isinstance(all_venues, list):
            # Cache the full list
            set_cached_all_venues(all_venues)
            
            # Also cache individual venues for quick lookup
            for venue in all_venues:
                if 'id' in venue:
                    set_cached_venue(venue['id'], venue)
            
            print(f"Successfully cached {len(all_venues)} venues")
            return True
        else:
            print("Failed to load venues or invalid data format")
            return False
            
    except Exception as e:
        print(f"Error loading venues: {e}")
        return False

def clear_expired_cache():
    """Clear expired cache entries"""
    current_time = datetime.now()
    expired_keys = []
    
    for key, value in games_cache.items():
        if (current_time - value['timestamp']).total_seconds() > cache_expiry:
            expired_keys.append(key)
    
    for key in expired_keys:
        del games_cache[key]
    
    # Clear expired game lines cache
    expired_game_lines = []
    for key, value in game_lines_cache.items():
        if (current_time - value['timestamp']).total_seconds() > cache_expiry:
            expired_game_lines.append(key)
    
    for key in expired_game_lines:
        del game_lines_cache[key]
    
    # Clear expired venues cache
    expired_venues = []
    for key, value in venues_cache.items():
        if (current_time - value['timestamp']).total_seconds() > cache_expiry:
            expired_venues.append(key)
    
    for key in expired_venues:
        del venues_cache[key]
    
    if expired_keys or expired_game_lines or expired_venues:
        print(f"Cleared {len(expired_keys)} expired games cache entries, {len(expired_game_lines)} expired game lines cache entries, and {len(expired_venues)} expired venues cache entries")

# Add the parent directory to the path so we can import cfbStatsLib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from cfbStatsLib import getCalendarWeekReg
except ImportError as e:
    print(f"Warning: Could not import cfbStatsLib: {e}")
    # Create a mock function for development
    def getCalendarWeekReg(seasonYear, weekNum):
        return [
            [],  # weekNights
            [],  # saturdayEarly
            [],  # saturdayAfternoon
            [],  # saturdayEvening
            [],  # saturdayLate
            []   # extraNights
        ]

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Serve the main web app"""
    return app.send_static_file('index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve assets from the static/assets directory"""
    return app.send_static_file(f'assets/{filename}')

@app.route('/api/games')
def get_games():
    """API endpoint to get games data"""
    try:
        # Get query parameters
        season_year = int(request.args.get('season', 2025))
        week_num = int(request.args.get('week', 1))
        season_type = request.args.get('type', 'regular')
        
        # Validate parameters
        if season_year < 2003 or season_year > 2030:
            return jsonify({'error': 'Invalid season year'}), 400
        
        if week_num < 1 or week_num > 17:
            return jsonify({'error': 'Invalid week number'}), 400
        
        if season_type not in ['regular', 'postseason']:
            return jsonify({'error': 'Invalid season type'}), 400
        
        # Check cache first
        cached_data = get_cached_games(season_year, week_num, season_type)
        if cached_data:
            print(f"Cache HIT: {season_type} {season_year} week {week_num}")
            return jsonify(cached_data)
        
        print(f"Cache MISS: {season_type} {season_year} week {week_num}")
        
        # Get games data from the library
        if season_type == 'regular':
            week_slate = api.getCalendarWeekReg(season_year, week_num)
        elif season_type == 'postseason':
            week_slate = api.getCalendarWeekPost(season_year)
        else:
            return jsonify({'error': 'Invalid season type'}), 400

        # Flatten the week slate into a single list of games
        all_games = []
        for slate in week_slate:
            if slate:  # Check if slate is not empty
                all_games.extend(slate)
        
        # Process lines data for each game
        for game in all_games:
            if 'lines' in game and game['lines']:
                # Format lines data to match the expected structure
                formatted_lines = []
                for line in game['lines']:
                    formatted_line = {
                        'id': f"{game['id']}_{line.get('linesProviderId', 'default')}",
                        'gameId': game['id'],
                        'provider': f"Provider_{line.get('linesProviderId', 'default')}",
                        'spread': line.get('spread'),
                        'overUnder': line.get('overUnder'),
                        'moneylineHome': line.get('moneylineHome'),
                        'moneylineAway': line.get('moneylineAway'),
                        'formattedSpread': f"{line.get('spread', 'N/A')}",
                        'formattedOverUnder': f"{line.get('overUnder', 'N/A')}",
                        'created': datetime.now().isoformat(),
                        'updated': datetime.now().isoformat()
                    }
                    formatted_lines.append(formatted_line)
                
                # Update game with formatted lines
                game['lines'] = formatted_lines
        
        # Convert to the format expected by the frontend
        games_data = {
            'game': all_games,
            'metadata': {
                'season': season_year,
                'week': week_num,
                'seasonType': season_type,
                'totalGames': len(all_games),
                'timestamp': datetime.now().isoformat(),
                'cached': False
            }
        }
        
        # Cache the data (this will also cache the lines data)
        set_cached_games(season_year, week_num, season_type, games_data)
        
        # Log lines data extraction
        lines_count = sum(1 for game in all_games if 'lines' in game and game['lines'])
        if lines_count > 0:
            print(f"Extracted and cached betting lines for {lines_count} games")
        
        return jsonify(games_data)
        
    except Exception as e:
        print(f"Error getting games: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/cache/status')
def cache_status():
    """Get cache status and statistics"""
    clear_expired_cache()  # Clean up expired entries first
    
    # Count lines data cached from games
    lines_from_games = sum(1 for data in game_lines_cache.values() 
                          if data.get('data', {}).get('cached_from_games', False))
    
    return jsonify({
        'games_cache_size': len(games_cache),
        'game_lines_cache_size': len(game_lines_cache),
        'venues_cache_size': len(venues_cache),
        'lines_from_games_cache': lines_from_games,
        'games_cache_keys': list(games_cache.keys()),
        'game_lines_cache_keys': list(game_lines_cache.keys()),
        'venues_cache_keys': list(venues_cache.keys()),
        'cache_expiry_minutes': cache_expiry // 60
    })

@app.route('/api/cache/clear')
def clear_cache():
    """Clear all cached data"""
    games_cache.clear()
    game_lines_cache.clear()
    venues_cache.clear()
    return jsonify({'message': 'All caches cleared successfully'})

@app.route('/api/cache/load-venues')
def load_venues_cache():
    """Manually trigger venue cache loading"""
    try:
        success = load_and_cache_all_venues()
        if success:
            return jsonify({'message': 'Venues loaded and cached successfully'})
        else:
            return jsonify({'error': 'Failed to load venues'}), 500
    except Exception as e:
        return jsonify({'error': f'Error loading venues: {str(e)}'}), 500

@app.route('/api/team/<int:team_id>')
def get_team_info(team_id):
    """API endpoint to get team information by ID"""
    try:
        team_info = api.getTeamInfo(team_id)
        return jsonify(team_info)
    except Exception as e:
        return jsonify({'error': f'Error getting team info: {str(e)}'}), 500

@app.route('/api/team/search/<team_name>')
def search_team_by_name(team_name):
    """API endpoint to search for teams by name"""
    try:
        teams = api.getTeamInfoByName(team_name)
        return jsonify(teams)
    except Exception as e:
        return jsonify({'error': f'Error searching teams: {str(e)}'}), 500

@app.route('/api/teams')
def get_all_teams():
    """API endpoint to get all FBS teams"""
    try:
        teams = api.getAllTeams()
        return jsonify(teams)
    except Exception as e:
        return jsonify({'error': f'Error getting teams: {str(e)}'}), 500

@app.route('/api/game-lines/<int:game_id>')
def get_game_lines(game_id):
    """API endpoint to get game lines by game ID"""
    try:
        # Check cache first
        cached_data = get_cached_game_lines(game_id)
        if cached_data:
            print(f"Cache HIT: Game lines for game {game_id}")
            return jsonify(cached_data)
        
        print(f"Cache MISS: Game lines for game {game_id}")
        
        # Get game lines from the library
        game_lines = api.getGameLines(game_id)
        
        # Cache the data
        set_cached_game_lines(game_id, game_lines)
        
        return jsonify(game_lines)
    except Exception as e:
        return jsonify({'error': f'Error getting game lines: {str(e)}'}), 500

@app.route('/api/game-lines/teams')
def get_game_lines_by_teams():
    """API endpoint to get game lines by team names"""
    try:
        away_team = request.args.get('away')
        home_team = request.args.get('home')
        season = request.args.get('season', type=int)
        week = request.args.get('week', type=int)
        
        if not away_team or not home_team:
            return jsonify({'error': 'Both away and home team names are required'}), 400
        
        game_lines = api.getGameLinesByTeams(away_team, home_team, season, week)
        return jsonify(game_lines)
    except Exception as e:
        return jsonify({'error': f'Error getting game lines: {str(e)}'}), 500

@app.route('/api/venue/<int:venue_id>')
def get_venue_info(venue_id):
    """API endpoint to get venue information by venue ID"""
    try:
        # Check cache first
        cached_venue = get_cached_venue(venue_id)
        if cached_venue:
            print(f"Cache HIT: Venue {venue_id}")
            return jsonify(cached_venue)
        
        print(f"Cache MISS: Venue {venue_id}")
        
        # If not in cache, try to get from API
        venue_info = api.getVenueInfo(venue_id)
        
        # Cache the result if it's valid
        if venue_info and 'error' not in venue_info:
            set_cached_venue(venue_id, venue_info)
        
        return jsonify(venue_info)
    except Exception as e:
        return jsonify({'error': f'Error getting venue info: {str(e)}'}), 500

@app.route('/api/venue/search/<venue_name>')
def search_venue_by_name(venue_name):
    """API endpoint to search for venues by name"""
    try:
        venues = api.getVenueInfoByName(venue_name)
        return jsonify(venues)
    except Exception as e:
        return jsonify({'error': f'Error searching venues: {str(e)}'}), 500

@app.route('/api/venues')
def get_all_venues():
    """API endpoint to get all venues"""
    try:
        venues = api.getAllVenues()
        return jsonify(venues)
    except Exception as e:
        return jsonify({'error': f'Error getting venues: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Dr. Moon Pie's CFB Stats Index...")
    
    # Clear expired cache on startup
    clear_expired_cache()
    
    # Load and cache all venues on startup
    load_and_cache_all_venues()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

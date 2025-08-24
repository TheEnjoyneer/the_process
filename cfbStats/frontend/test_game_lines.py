#!/usr/bin/env python3
"""
Test script to demonstrate the updated getGameLines function
"""

import sys
import os

# Add the current directory to the path so we can import cfbStatsLib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from cfbStatsLib import getGameLines, getGameLinesByTeams
except ImportError as e:
    print(f"Error importing cfbStatsLib: {e}")
    sys.exit(1)

def test_get_game_lines():
    """Test getting game lines by game ID"""
    print("Testing getGameLines by ID...")
    print("=" * 50)
    
    # Test with a known game ID (you'll need to replace with a real game ID)
    game_id = 401520636  # Example game ID - replace with actual ID
    
    result = getGameLines(game_id)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Game ID: {result.get('gameId', 'N/A')}")
        print(f"Line Count: {result.get('lineCount', 0)}")
        
        if result.get('gameInfo'):
            game = result['gameInfo']
            print(f"Game: {game.get('awayTeam', 'N/A')} at {game.get('homeTeam', 'N/A')}")
            print(f"Date: {game.get('startDate', 'N/A')}")
            print(f"Season: {game.get('season', 'N/A')} Week {game.get('week', 'N/A')}")
        
        if result.get('latestLines'):
            print(f"\nLatest Lines from {len(result['latestLines'])} providers:")
            for line in result['latestLines']:
                print(f"  {line.get('provider', 'Unknown')}:")
                if line.get('formattedSpread'):
                    print(f"    Spread: {line['formattedSpread']}")
                if line.get('formattedOverUnder'):
                    print(f"    Total: {line['formattedOverUnder']}")
                if line.get('homeMoneyline') or line.get('awayMoneyline'):
                    print(f"    Moneyline: {line.get('awayMoneyline', 'N/A')} / {line.get('homeMoneyline', 'N/A')}")
        
        if result.get('averageSpread'):
            print(f"\nAverage Spread: {result['averageSpread']:.1f}")
        if result.get('averageTotal'):
            print(f"Average Total: {result['averageTotal']:.1f}")

def test_get_game_lines_by_teams():
    """Test getting game lines by team names"""
    print("\n" + "=" * 50)
    print("Testing getGameLinesByTeams...")
    print("=" * 50)
    
    # Test with known teams
    away_team = "Michigan"
    home_team = "Ohio State"
    season = 2024
    week = 13
    
    result = getGameLinesByTeams(away_team, home_team, season, week)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found game lines for {away_team} at {home_team}")
        print(f"Line Count: {result.get('lineCount', 0)}")
        
        if result.get('latestLines'):
            print(f"\nLatest Lines:")
            for line in result['latestLines']:
                print(f"  {line.get('provider', 'Unknown')}:")
                if line.get('formattedSpread'):
                    print(f"    Spread: {line['formattedSpread']}")
                if line.get('formattedOverUnder'):
                    print(f"    Total: {line['formattedOverUnder']}")

def main():
    """Main test function"""
    print("CFB Game Lines Test")
    print("=" * 50)
    
    # Test game lines by ID
    test_get_game_lines()
    
    # Test game lines by teams
    test_get_game_lines_by_teams()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()

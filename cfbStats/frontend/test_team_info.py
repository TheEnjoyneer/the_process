#!/usr/bin/env python3
"""
Test script to demonstrate the updated getTeamInfo function
"""

import sys
import os

# Add the current directory to the path so we can import cfbStatsLib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from cfbStatsLib import getTeamInfo, getTeamInfoByName, getAllTeams
except ImportError as e:
    print(f"Error importing cfbStatsLib: {e}")
    sys.exit(1)

def test_get_team_info():
    """Test getting team information by ID"""
    print("Testing getTeamInfo by ID...")
    print("=" * 50)
    
    # Test with a known team ID (Michigan = 130)
    team_id = 130
    result = getTeamInfo(team_id)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Team: {result.get('team', 'N/A')}")
        print(f"School: {result.get('school', 'N/A')}")
        print(f"Mascot: {result.get('mascot', 'N/A')}")
        print(f"Conference: {result.get('conference', 'N/A')}")
        print(f"Location: {result.get('locationCity', 'N/A')}, {result.get('locationState', 'N/A')}")
        print(f"Venue: {result.get('venue', 'N/A')}")
        print(f"Capacity: {result.get('capacity', 'N/A')}")
        print(f"Colors: {result.get('color', 'N/A')} / {result.get('altColor', 'N/A')}")
        
        if 'historical' in result:
            hist = result['historical']
            print(f"\nHistorical Info (Year {hist.get('year', 'N/A')}):")
            print(f"Record: {hist.get('wins', 0)}-{hist.get('losses', 0)}-{hist.get('ties', 0)}")
            print(f"Win %: {hist.get('pct', 0):.3f}")
            print(f"SRS: {hist.get('srs', 'N/A')}")
            print(f"SP+ Overall: {hist.get('spOverall', 'N/A')}")

def test_get_team_by_name():
    """Test getting team information by name"""
    print("\n\nTesting getTeamInfoByName...")
    print("=" * 50)
    
    # Test with a team name
    team_name = "Michigan"
    result = getTeamInfoByName(team_name)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {len(result)} team(s) matching '{team_name}':")
        for team in result:
            print(f"- {team.get('team', 'N/A')} ({team.get('school', 'N/A')}) - {team.get('conference', 'N/A')}")

def test_get_all_teams():
    """Test getting all teams"""
    print("\n\nTesting getAllTeams...")
    print("=" * 50)
    
    result = getAllTeams()
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {len(result)} FBS teams:")
        print("First 10 teams:")
        for i, team in enumerate(result[:10]):
            print(f"{i+1}. {team.get('team', 'N/A')} ({team.get('abbreviation', 'N/A')}) - {team.get('conference', 'N/A')}")
        
        if len(result) > 10:
            print(f"... and {len(result) - 10} more teams")

def main():
    """Run all tests"""
    print("CFB Team Info Test")
    print("=" * 60)
    
    try:
        test_get_team_info()
        test_get_team_by_name()
        test_get_all_teams()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

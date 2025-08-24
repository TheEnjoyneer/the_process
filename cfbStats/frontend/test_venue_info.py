#!/usr/bin/env python3
"""
Test script to demonstrate the venue information functions
Updated to use REST API instead of GraphQL
"""

import sys
import os

# Add the current directory to the path so we can import cfbStatsLib
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from cfbStatsLib import getVenueInfo, getVenueInfoByName, getAllVenues
except ImportError as e:
    print(f"Error importing cfbStatsLib: {e}")
    sys.exit(1)

def test_get_venue_info():
    """Test getting venue information by venue ID"""
    print("Testing getVenueInfo by ID...")
    print("=" * 50)
    
    # Test with a known venue ID (Michigan Stadium = 1)
    # Note: Using REST API now, venue IDs may be different
    venue_id = 1
    
    result = getVenueInfo(venue_id)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Venue ID: {result.get('id', 'N/A')}")
        print(f"Name: {result.get('name', 'N/A')}")
        print(f"Location: {result.get('locationString', 'N/A')}")
        print(f"Capacity: {result.get('formattedCapacity', 'N/A')}")
        print(f"Surface: {result.get('surface', 'N/A')}")
        print(f"Venue Type: {result.get('venueType', 'N/A')}")
        print(f"Home Team: {result.get('homeTeam', 'N/A')}")
        print(f"Conference: {result.get('conference', 'N/A')}")
        print(f"Year Opened: {result.get('yearOpened', 'N/A')}")
        print(f"Full Address: {result.get('fullAddress', 'N/A')}")

def test_get_venue_by_name():
    """Test getting venue information by name"""
    print("\n" + "=" * 50)
    print("Testing getVenueInfoByName...")
    print("=" * 50)
    
    # Test with a known venue name
    venue_name = "Michigan Stadium"
    
    result = getVenueInfoByName(venue_name)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {result.get('count', 0)} venues matching '{venue_name}'")
        
        for venue in result.get('venues', []):
            print(f"\nVenue: {venue.get('name', 'N/A')}")
            print(f"  ID: {venue.get('id', 'N/A')}")
            print(f"  Location: {venue.get('locationString', 'N/A')}")
            print(f"  Capacity: {venue.get('formattedCapacity', 'N/A')}")
            print(f"  Surface: {venue.get('surface', 'N/A')}")

def test_get_all_venues():
    """Test getting all venues"""
    print("\n" + "=" * 50)
    print("Testing getAllVenues...")
    print("=" * 50)
    
    result = getAllVenues()
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {len(result)} total venues")
        
        # Show first 5 venues as examples
        print("\nFirst 5 venues:")
        for i, venue in enumerate(result[:5]):
            print(f"{i+1}. {venue.get('name', 'N/A')} - {venue.get('locationString', 'N/A')} ({venue.get('formattedCapacity', 'N/A')})")

def test_venue_search():
    """Test venue search functionality"""
    print("\n" + "=" * 50)
    print("Testing venue search...")
    print("=" * 50)
    
    # Test with partial name
    search_term = "Stadium"
    
    result = getVenueInfoByName(search_term)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {result.get('count', 0)} venues containing '{search_term}'")
        
        # Show first 3 results
        for i, venue in enumerate(result.get('venues', [])[:3]):
            print(f"{i+1}. {venue.get('name', 'N/A')} - {venue.get('locationString', 'N/A')}")

def main():
    """Main test function"""
    print("CFB Venue Information Test")
    print("=" * 50)
    
    # Test venue info by ID
    test_get_venue_info()
    
    # Test venue info by name
    test_get_venue_by_name()
    
    # Test venue search
    test_venue_search()
    
    # Test get all venues (commented out to avoid too much output)
    # test_get_all_venues()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()

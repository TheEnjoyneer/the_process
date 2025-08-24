# Dr. Moon Pie's CFB Stats Index

A one-page web application that displays College Football games information in a card-based layout, similar to the Angular app design. The app fetches game data from the GraphQL API using the `getCalendarWeekReg` function from `cfbStatsLib.py`, and venue information from the REST API.

## Features

- **Responsive Design**: Card-based layout that works on desktop and mobile devices
- **Game Organization**: Games are organized by time slots (Weeknight, Saturday Early, Afternoon, Evening, Late)
- **Real-time Data**: Fetches live game data from the College Football Data GraphQL API
- **Venue Information**: Retrieves venue details from the College Football Data REST API
- **Visual Design**: Based on the Angular app's dark theme with Material Design elements
- **Game Details**: Displays team matchups, game times, venues, scores, and statistics

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure cfbStatsLib.py is available**:
   The app expects `cfbStatsLib.py` to be in the parent directory (`../cfbStatsLib.py`).

## Running the Application

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```

2. **Access the Web App**:
   Open your browser and navigate to: `http://localhost:5000`

3. **API Endpoint**:
   The API endpoint for game data is: `http://localhost:5000/api/games`

## Usage

1. **Select Parameters**:
   - Season Year (2020-2030)
   - Week Number (1-17)
   - Season Type (Regular Season or Postseason)

2. **Load Games**:
   Click the "Load Games" button to fetch and display games for the selected criteria.

3. **View Game Information**:
   - Game matchups with team abbreviations
   - Game times and venues
   - Excitement scores and win probabilities
   - Conference game indicators
   - Final scores for completed games

## Data Structure

The app expects game data in the following format (from the GraphQL query response):

```json
{
  "game": [
    {
      "id": "12345",
      "awayTeam": "Michigan",
      "homeTeam": "Ohio State",
      "awayPoints": 30,
      "homePoints": 27,
      "startDate": "2024-11-30T15:30:00",
      "venueId": "123",
      "neutralSite": false,
      "conferenceGame": true,
      "excitement": 85.5,
      "awayPostgameWinProb": 0.65,
      "homePostgameWinProb": 0.35,
      "status": "final",
      "watchability": 95
    }
  ]
}
```

## File Structure

```
cfbStats/frontend/
├── app.py              # Flask server and API endpoints
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── static/
    └── index.html     # Main web application
```

## API Endpoints

- `GET /` - Serves the main web application
- `GET /api/games` - Returns game data for specified season/week/type
- `GET /api/health` - Health check endpoint
- `GET /api/team/<team_id>` - Returns team information by team ID
- `GET /api/team/search/<team_name>` - Searches for teams by name
- `GET /api/teams` - Returns all FBS teams
- `GET /api/game-lines/<game_id>` - Returns betting lines for a specific game by game ID
- `GET /api/game-lines/teams` - Returns betting lines for a game by team names
- `GET /api/venue/<venue_id>` - Returns venue information by venue ID
- `GET /api/venue/search/<venue_name>` - Searches for venues by name
- `GET /api/venues` - Returns all venues

### Query Parameters for `/api/games`:

- `season` (int): Season year (2020-2030)
- `week` (int): Week number (1-17)
- `type` (string): Season type ("regular" or "postseason")

### Team Information Endpoints:

- `/api/team/<team_id>` - Get comprehensive team information by team ID
- `/api/team/search/<team_name>` - Search for teams by name (supports partial matches)
- `/api/teams` - Get all current FBS teams

### Team Information Data Structure:

The team information includes:
- Basic team details (name, school, mascot, abbreviation)
- Conference and division information
- Location data (city, state, coordinates)
- Venue information (stadium, capacity, surface type)
- Team colors and logos
- Historical performance data (when available)

### Game Lines Endpoints:

- `/api/game-lines/<game_id>` - Get betting lines by game ID
- `/api/game-lines/teams` - Get betting lines by team names

### Query Parameters for `/api/game-lines/teams`:

- `away` (string): Away team name (required)
- `home` (string): Home team name (required)
- `season` (int, optional): Season year to filter by
- `week` (int, optional): Week number to filter by

### Game Lines Data Structure:

The game lines information includes:
- Game details (teams, date, venue, status)
- Betting lines from multiple providers
- Spread, total, and moneyline odds
- Formatted display values
- Average spreads and totals across providers
- Latest lines from each provider

### Venue Endpoints:

- `/api/venue/<venue_id>` - Get venue information by venue ID
- `/api/venue/search/<venue_name>` - Search for venues by name (supports partial matches)
- `/api/venues` - Get all venues

### Venue Data Structure:

The venue information includes:
- Basic venue details (name, location, capacity)
- Physical characteristics (surface type, roof type, grass/dome)
- Location data (city, state, coordinates, timezone)
- Historical information (year opened, elevation)
- Contact information (address, phone, website)
- Team associations (home team, conference, division)
- Computed fields (formatted capacity, full address, venue type)

## Troubleshooting

1. **Import Error**: If you see an import error for `cfbStatsLib`, ensure the file is in the correct location (`../cfbStatsLib.py`).

2. **API Connection**: If the API calls fail, check that the Flask server is running and accessible.

3. **No Games Displayed**: This could indicate:
   - No games scheduled for the selected criteria
   - API connection issues
   - Data format issues

## Development

The web app is built with:
- **HTML5** for structure
- **CSS3** with CSS Grid and Flexbox for layout
- **Vanilla JavaScript** for interactivity
- **Flask** for the backend API
- **College Football Data API** for game data

The design follows the Angular app's visual theme with:
- Dark color scheme
- Card-based layout
- Material Design shadows and elevation
- Responsive grid system
- Typography matching the original design

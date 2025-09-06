import requests

def get_games_from_api(week: int):
    API_KEY = "Uedy3yaRnJtnmRSHIx14HmazWwlLaQiVdd46649fTd7HaNXQtb0Xnbgz4w4DivXw"
    url = f"https://api.collegefootballdata.com/games?year=2025&seasonType=regular&week={week}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_rankings_from_api(week: int):
    API_KEY = "Uedy3yaRnJtnmRSHIx14HmazWwlLaQiVdd46649fTd7HaNXQtb0Xnbgz4w4DivXw"
    url = f"https://api.collegefootballdata.com/rankings?year=2025&week={week}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    for item in data:
        for poll in item['polls']:
            if poll['poll'] == 'AP Top 25':
                return poll['ranks']
    return []

def is_top_25_game(home_team: str, away_team: str, rankings: dict):
    for team in rankings:
        if team['school'] == home_team:
            home_rank = team['rank']
            return True
        if team['school'] == away_team:
            away_rank = team['rank']
            return True
    return False

def to_top_25_team(team: str, rankings: dict):
    for ranking in rankings:
        if ranking['school'] == team:
            return f"{ranking['rank']} {team}"
    return team

def get_top_25_games(games: dict, rankings: dict):
    for game in games:
        home_team_name = game['homeTeam']
        away_team_name = game['awayTeam']
        home_team_formatted = to_top_25_team(home_team_name, rankings)
        away_team_formatted = to_top_25_team(away_team_name, rankings)
        
        is_top_25_game = home_team_formatted != home_team_name or away_team_formatted != away_team_name

        if is_top_25_game:
            print(f"{away_team_formatted} @ {home_team_formatted}")
            print(f"Score: {game['awayPoints']} - {game['homePoints']}")
            print("-" * 30)

def __main__():
    week = 1
    games = get_games_from_api(week)
    rankings = get_rankings_from_api(week)
    get_top_25_games(games, rankings)

if __name__ == "__main__":
    __main__()
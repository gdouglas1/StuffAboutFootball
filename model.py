import operator
from datetime import datetime


class Competition:
    def __init__(self, id, name, year):
        self.id = id
        self.name = name
        self.year = year


class Team:
    def __init__(self, id, name, short_name, market_value, crest_url):
        self.id = id
        self.name = name
        self.short_name = short_name
        self.market_value = market_value
        self.crest_url = crest_url


class Player:
    def __init__(self, name, position, jersey_number, dob, nationality, contract_until, market_value):
        self.name = name
        self.position = position
        self.jersey_number = int(jersey_number)
        self.dob = datetime.strftime(datetime.strptime(dob, "%Y-%m-%d"), "%d/%m/%Y")
        self.age = (datetime.now() - datetime.strptime(dob, "%Y-%m-%d")).days // 365
        self.nationality = nationality
        # Populate contract_until_date and contract_duration by parsing the contract_until parameter
        if contract_until is not None:
            # Might be slightly inaccurate in some circumstances.
            # More accurate measurement of years is done by relativedelta lib
            contract_until_date = datetime.strptime(contract_until, "%Y-%m-%d")
            contract_duration = (contract_until_date - datetime.now()).days // 365
            self.contract_until = datetime.strftime(contract_until_date, "%d/%m/%Y")
            if contract_duration < 1:
                self.contract_duration_years = "< 1"
            else:
                self.contract_duration_years = contract_duration
        else:
            self.contract_until = None
            self.contract_duration_years = None

        self.market_value = market_value


class Fixture:
    def __init__(self, fixture_id, competition_id, fixture_date, fixture_status, home_team_name, home_team_id,
                 away_team_name, away_team_id, result, head_to_head, match_day):
        self.fixture_id = fixture_id
        self.competition_id = competition_id
        self.fixture_date = datetime.strptime(fixture_date,  "%Y-%m-%dT%H:%M:%SZ").strftime('%d/%m/%Y')
        self.fixture_actual_date = datetime.strptime(fixture_date,  "%Y-%m-%dT%H:%M:%SZ")
        self.fixture_status = fixture_status
        self.home_team_name = home_team_name
        self.home_team_id = home_team_id
        self.away_team_name = away_team_name
        self.away_team_id = away_team_id

        # Result object
        self.result = result

        # Head to Head object
        self.head_to_head = head_to_head

        self.match_day = int(match_day)


class Result:
    def __init__(self, home_team_goals, away_team_goals, halftime_home_team_goals, halftime_away_team_goals):
        if home_team_goals is not None:
            self.home_team_goals = int(home_team_goals)
        else:
            self.home_team_goals = None

        if away_team_goals is not None:
            self.away_team_goals = int(away_team_goals)
        else:
            self.away_team_goals = None

        if halftime_home_team_goals is not None:
            self.halftime_home_team_goals = int(halftime_home_team_goals)
        else:
            self.halftime_home_team_goals = None

        if halftime_away_team_goals is not None:
            self.halftime_away_team_goals = int(halftime_away_team_goals)
        else:
            self.halftime_away_team_goals = None


class HeadToHead:
    def __init__(self, count, date_start, date_end, home_wins, away_wins, draws, last_home_win_home_team,
                 last_win_home_team, last_away_win_away_team, last_win_away_team, fixtures):
        self.count = count
        self.date_start = date_start
        self.date_end = date_end
        self.home_wins = int(home_wins)
        self.away_wins = int(away_wins)
        self.draws = int(draws)

        # Fixture objects
        self.last_home_win_home_team = last_home_win_home_team
        self.last_win_home_team = last_win_home_team
        self.last_away_win_away_team = last_away_win_away_team
        self.last_win_away_team = last_win_away_team

        # List of fixtures
        self.fixtures = fixtures

class LeagueTable:
    def __init__(self, standings):
        # Default ordering will always be by position in the table
        self.standings = sorted(standings, key=operator.attrgetter('position'))


class Standing:
    def __init__(self, team_id, team_name, position, played_games, goals, points, team_form, home_form, away_form):
        self.team_id = team_id
        self.team_name = team_name
        self.position = position
        self.played_games = played_games
        self.goals = int(goals)
        self.points = int(points)
        self.team_form = team_form
        self.home_form = home_form
        self.away_form = away_form


class TeamForm:
    def __init__(self, wins, draws, losses, goals_for, goals_against):
        self.wins = int(wins)
        self.draws = int(draws)
        self.losses = int(losses)
        self.goals_for = int(goals_for)
        self.goals_against = int(goals_against)

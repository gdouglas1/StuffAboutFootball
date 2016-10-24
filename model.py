import operator
from datetime import datetime
from typing import List, Optional


class Competition:
    def __init__(self, id: int, name: str, year: str) -> None:
        self.id = id
        self.name = name
        self.year = year


class Team:
    def __init__(self, id: int, name: str, short_name: str, market_value: str, crest_url: str) -> None:
        self.id = id
        self.name = name
        self.short_name = short_name
        self.market_value = market_value
        self.crest_url = crest_url


class Player:
    def __init__(self, name: str, position: str, jersey_number: Optional[str], dob: str, nationality: str,
                 contract_until: str, market_value: str) -> None:
        self.name = name
        self.position = position
        self.jersey_number = int(jersey_number) or None
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
                self.contract_duration_years = str(contract_duration)
        else:
            self.contract_until = None
            self.contract_duration_years = None

        self.market_value = market_value


class Result:
    def __init__(self, home_team_goals: Optional[int], away_team_goals: Optional[int],
                 halftime_home_team_goals: Optional[int], halftime_away_team_goals: Optional[int]) -> None:
        self.home_team_goals = home_team_goals or 0
        self.away_team_goals = away_team_goals or 0
        self.halftime_home_team_goals = halftime_home_team_goals or 0
        self.halftime_away_team_goals = halftime_away_team_goals or 0


class Fixture:
    def __init__(self, fixture_id: int, competition_id: int, fixture_date: str, fixture_status: str,
                 home_team_name: str, home_team_id: int, away_team_name: str, away_team_id: int, result: Result,
                 head_to_head: 'HeadToHead', match_day: str) -> None:
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


class HeadToHead:
    def __init__(self, count: int, date_start: str, date_end: str, home_wins: str, away_wins: str, draws: str,
                 last_home_win_home_team: Fixture, last_win_home_team: Fixture, last_away_win_away_team: Fixture,
                 last_win_away_team: Fixture, fixtures: List[Fixture]) -> None:
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
    def __init__(self, standings: List['Standing']) -> None:
        # Default ordering will always be by position in the table
        self.standings = sorted(standings, key=operator.attrgetter('position'))


class TeamForm:
    def __init__(self, wins: Optional[int], draws: Optional[int], losses: Optional[int],
                 goals_for: Optional[int], goals_against: Optional[int]) -> None:
        self.wins = int(wins) or 0
        self.draws = int(draws) or 0
        self.losses = int(losses) or 0
        self.goals_for = int(goals_for)
        self.goals_against = int(goals_against)


class Standing:
    def __init__(self, team_id: int, team_name: str, position: int, played_games: int, goals: int,
                 points: int, team_form: TeamForm, home_form: TeamForm, away_form: TeamForm) -> None:
        self.team_id = team_id
        self.team_name = team_name
        self.position = position
        self.played_games = played_games
        self.goals = goals
        self.points = points
        self.team_form = team_form
        self.home_form = home_form
        self.away_form = away_form

import collections

from typing import Union, List, Dict

from model import Player, Fixture, Result, TeamForm, Standing, Competition, HeadToHead, LeagueTable, Team


def to_competition(json_dict: dict) -> Competition:
    """
    Converts json dictionary into Competition object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = Competition(json_dict['id'], json_dict['caption'], json_dict['year'])

    return result


def to_competitions(json_dict: dict) -> List[Competition]:
    """
    Converts json dictionary to list of Competition objects
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = [to_competition(competition_json) for competition_json in json_dict]

    return result


def to_team(json_dict: dict) -> Team:
    """
    Converts json dictionary to Team object
    :param json_dict:
    :return: Team
    """
    if json_dict is None:
        return None

    team_link = json_dict['_links']['self']['href']
    team_id = team_link[team_link.rfind('/') + 1:]

    result = Team(team_id, json_dict['name'], json_dict['shortName'], json_dict['squadMarketValue'],
                  json_dict['crestUrl'])

    return result


def to_player(json_dict: dict) -> Player:
    """
    Converts json dictionary to Player object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = Player(json_dict['name'], json_dict['position'], json_dict['jerseyNumber'], json_dict['dateOfBirth'],
                    json_dict['nationality'], json_dict['contractUntil'], json_dict['marketValue'])
    return result


def to_fixture(json_dict: dict) -> Fixture:
    """
    Converts json dictionary to Fixture object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    # Get fixture
    fixture_url = json_dict['_links']['self']['href']
    fixture_id = fixture_url[fixture_url.rfind('/') + 1:]

    # Get competition id
    competition_url = json_dict['_links']['competition']['href']
    competition_id = competition_url[competition_url.rfind('/') + 1:]

    # Get home team data
    home_team_url = json_dict['_links']['homeTeam']['href']
    home_team_id = home_team_url[home_team_url.rfind('/') + 1:]

    # Get away team data
    away_team_url = json_dict['_links']['awayTeam']['href']
    away_team_id = away_team_url[away_team_url.rfind('/') + 1:]

    # Get result object
    fixture_result = to_result(json_dict['result'])

    fixture = Fixture(fixture_id, competition_id, json_dict['date'], json_dict['status'], json_dict['homeTeamName'],
                      home_team_id, json_dict['awayTeamName'], away_team_id, fixture_result, None,
                      json_dict['matchday'])

    return fixture


def to_result(json_dict: dict) -> Result:
    """
    Converts json dictionary to Result object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = Result(json_dict['goalsHomeTeam'], json_dict['goalsAwayTeam'], None, None)

    if 'halfTime' in json_dict:
        result.halftime_home_team_goals = json_dict['halfTime']['goalsHomeTeam']
        result.halftime_away_team_goals = json_dict['halfTime']['goalsAwayTeam']

    return result


def to_teamform(json_dict: dict) -> TeamForm:
    """
    Converts json dictionary into TeamForm object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = TeamForm(json_dict['wins'], json_dict['draws'], json_dict['losses'], json_dict['goals'],
                      json_dict['goalsAgainst'])

    return result


def to_headtohead(json_dict: dict) -> HeadToHead:
    """
    Converts json dictionary to HeadToHead object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    last_home_win_home_team = to_fixture(json_dict['lastHomeWinHomeTeam'])
    last_away_win_away_team = to_fixture(json_dict['lastAwayWinAwayTeam'])
    last_win_home_team = to_fixture(json_dict['lastWinHomeTeam'])
    last_win_away_team = to_fixture(json_dict['lastWinAwayTeam'])
    fixtures = [to_fixture(fixture_json) for fixture_json in json_dict['fixtures']]

    head2head = HeadToHead(json_dict['count'],
                           json_dict['timeFrameStart'],
                           json_dict['timeFrameEnd'],
                           json_dict['homeTeamWins'],
                           json_dict['awayTeamWins'],
                           json_dict['draws'],
                           last_home_win_home_team,
                           last_win_home_team,
                           last_away_win_away_team,
                           last_win_away_team,
                           fixtures)

    return head2head


def to_leaguetable_standing(json_dict: dict) -> Standing:
    """
    Converts json dictionary to Standing object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    team_url = json_dict['_links']['team']['href']
    team_id = team_url[team_url.rfind("/") + 1:]

    team_form = to_teamform(json_dict)
    home_form = to_teamform(json_dict['home'])
    away_form = to_teamform(json_dict['away'])

    standing = Standing(team_id, json_dict['teamName'], json_dict['position'], json_dict['playedGames'],
                        json_dict['goals'], json_dict['points'], team_form, home_form, away_form)

    return standing


def to_league_table(json_dict: dict) -> Union[LeagueTable, List[LeagueTable]]:
    """
    Converts json dictionary to LeagueTable object, or list of LeagueTable objects depending on the contents
    of json_dict
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    if 'standings' in json_dict:
        league_tables = to_cup_league_tables(json_dict)
        return league_tables
    else:
        standings = [to_leaguetable_standing(standing_json) for standing_json in json_dict['standing']]
        result = LeagueTable(standings)
        return result


def to_cup_league_tables(json_dict: dict) -> Dict[str, LeagueTable]:
    """
    Converts json dictionary to ordered dictionary of league tables.
    Dictionary will be ordered by name
    :param json_dict:
    """
    league_dict = {}

    for league in json_dict['standings']:
        standings = [to_cup_standing(standing_json) for standing_json in json_dict['standings'][league]]
        league_table = LeagueTable(standings)
        if league not in league_dict:
            league_dict[league] = []
        league_dict[league] = league_table

    # Order league tables by name
    result = collections.OrderedDict(sorted(league_dict.items()))

    return result


def to_cup_standing(json_dict: dict) -> Standing:
    """
    Converts json dictionary to Standing object
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    team_form = to_cup_teamform(json_dict)

    standing = Standing(json_dict['teamId'], json_dict['team'], json_dict['rank'], json_dict['playedGames'],
                        json_dict['goals'], json_dict['points'], team_form, None, None)

    return standing


def to_cup_teamform(json_dict: dict) -> TeamForm:
    """
        Converts json dictionary into TeamForm object
        :param json_dict:
        :return:
        """
    if json_dict is None:
        return None

    result = TeamForm(None, None, None, json_dict['goals'],
                      json_dict['goalsAgainst'])

    return result
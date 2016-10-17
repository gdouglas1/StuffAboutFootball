from model import Player, Fixture, Result, TeamForm, Standing, Competition, HeadToHead, LeagueTable, Team


def to_competition(json_dict):
    """
    Converts json dictionary into Competition object
    :rtype: Competition
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = Competition(json_dict['id'], json_dict['caption'], json_dict['year'])

    return result


def to_competitions(json_dict):
    """
    Converts json dictionary to list of Competition objects
    :rtype: list of Competition
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = [to_competition(competition_json) for competition_json in json_dict]

    return result


def to_team(json_dict):
    """
    Converts json dictionary to Team object
    :rtype: Team
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


def to_player(json_dict):
    """
    Converts json dictionary to Player object
    :rtype: Player
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = Player(json_dict['name'], json_dict['position'], json_dict['jerseyNumber'], json_dict['dateOfBirth'],
                    json_dict['nationality'], json_dict['contractUntil'], json_dict['marketValue'])
    return result


def to_fixture(json_dict):
    """
    Converts json dictionary to Fixture object
    :rtype: Fixture
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


def to_result(json_dict):
    """
    Converts json dictionary to Result object
    :rtype: Result
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


def to_teamform(json_dict):
    """
    Converts json dictionary into TeamForm object
    :rtype: TeamForm
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    result = TeamForm(json_dict['wins'], json_dict['draws'], json_dict['losses'], json_dict['goals'],
                      json_dict['goalsAgainst'])

    return result


def to_headtohead(json_dict):
    """
    Converts json dictionary to HeadToHead object
    :rtype: HeadToHead
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


def to_standing(json_dict):
    """
    Converts json dictionary to Standing object
    :rtype: Standing
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


def to_leaguetable(json_dict):
    """
    Converts json dictionary to LeagueTable object
    :rtype: LeagueTable
    :param json_dict:
    :return:
    """
    if json_dict is None:
        return None

    standings = [to_standing(standing_json) for standing_json in json_dict['standing']]
    result = LeagueTable(standings)

    return result

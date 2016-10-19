import collections
from typing import Union, List, Dict

import requests
import json

import decoders
from model import Player, Fixture, Competition, LeagueTable, Team

api_key = '7b84e542649b417e931fb951f160b7fe'
base_url = 'http://api.football-data.org/v1/'


# region Helper functions
def make_request(endpoint: str) -> requests.Response:
    """
    Sends a request to the specified endpoint of the base URL
    :param endpoint:
    :return: response Json
    """
    return requests.get(base_url + endpoint, headers={"X-Auth-Token": api_key})


def group_fixtures_by_match_day(fixtures: List[Fixture]) -> Dict[str, List[Fixture]]:
    """
    Takes a list of Fixture objects, and groups them by matchday
    :param fixtures:
    :return:
    """
    result = collections.OrderedDict()  # type: Dict[str, List[Fixture]]
    for fixture in fixtures:
        key = str(fixture.match_day)
        if key not in result:
            result[key] = []
        result[key].append(fixture)

    return collections.OrderedDict(result)


def group_players_by_position(players: List[Player]) -> Dict[str, List[Player]]:
    """
    Takes a list of Player objects, and groups them by position
    :param players:
    :return:
    """
    # This list defines the order that positions should appear on-screen
    position_order = {k: v for v, k in enumerate(["Keeper", "Centre Back", "Left-Back", "Right-Back", 
                                                  "Defensive Midfield", "Central Midfield", "Left Wing", "Right Wing", 
                                                  "Attacking Midfield", "Centre Forward", "Secondary Striker"])}
    result = collections.OrderedDict()  # type: Dict[str, List[Player]]
    for player in players:
        key = player.position
        if key not in result:
            result[key] = []
        result[key].append(player)

    return collections.OrderedDict(sorted(result.items(), key=lambda i: position_order.get(i[0])))
# endregion


def get_competitions() -> List[Competition]:
    """
    Retrieves allcompetition data from the web service, and returns it as a list of Competition objects
    :return:
    """
    response = make_request("competitions/")
    json_dict = json.loads(response.text)

    # Cast dictionary to object, append to list and then return list
    result = decoders.to_competitions(json_dict)

    return result


def get_competition(competition_id: int) -> Competition:
    """
    Retrieves competition data for the specified competition ID from the web service, and returns it as a
    Competition object
    :param competition_id:
    :return:
    """
    response = make_request("competitions/" + str(competition_id))
    json_dict = json.loads(response.text)

    result = decoders.to_competition(json_dict)

    return result


def get_teams_for_competition(competition_id: int) -> List[Team]:
    """
    Retrieves all teams associated to the specified competition ID, and returns a list of Team objects
    :param competition_id:
    :return:
    """
    response = make_request("competitions/" + str(competition_id) + "/teams")
    json_dict = json.loads(response.text)

    result = [decoders.to_team(team_json) for team_json in json_dict['teams']]

    return result


def get_team(team_id: int) -> Team:
    """
    Retrieves the team with the specified team ID from the web service, and returns a Team object
    :param team_id:
    :return:
    """
    response = make_request("/teams/" + str(team_id))
    json_dict = json.loads(response.text)

    team_url = json_dict['_links']['self']['href']
    team_id = team_url[team_url.rfind('/') + 1:]

    result = decoders.to_team(json_dict)

    return result


def get_fixtures_for_competition(competition_id: int) -> List[Fixture]:
    """
    Retrieves all fixtures associated to the specified competition ID, and returns a list of Fixture objects
    :param competition_id:
    :return:
    """
    response = make_request("/competitions/" + str(competition_id) + "/fixtures")
    json_dict = json.loads(response.text)
    result = [decoders.to_fixture(fixture) for fixture in json_dict['fixtures']]

    return result


def get_fixtures_for_team(team_id: int) -> List[Fixture]:
    """
    Retrieves all fixtures for the associated team ID, and returns a list of Fixture objects
    :param team_id:
    :return:
    """
    response = make_request("/teams/" + str(team_id) + "/fixtures")
    json_dict = json.loads(response.text)
    result = [decoders.to_fixture(fixture_json) for fixture_json in json_dict['fixtures']]

    return result


def get_players_grouped(team_id: int) -> Dict[str, List[Player]]:
    """
    Retrieves all players that play for the team with the specified team ID.  Returns a dictionary of Player objects
    grouped by position
    :param team_id:
    :return:
    """
    response = make_request("/teams/" + str(team_id) + "/players")
    json_dict = json.loads(response.text)
    result = [decoders.to_player(player_json) for player_json in json_dict['players']]
    grouped_result = group_players_by_position(result)

    return grouped_result


def get_players_ungrouped(team_id: int) -> List[Player]:
    """
    Retrieves all players that play for the team with the specified team ID.  Returns a list of Player objects
    :param team_id:
    :return:
    """
    response = make_request("/teams/" + str(team_id) + "/players")
    json_dict = json.loads(response.text)
    result = [decoders.to_player(player_json) for player_json in json_dict['players']]

    return result


def get_fixture(fixture_id: int) -> Fixture:
    """
    Retrieves the fixture with the specified fixture ID, and returns a Fixture object including head-to-head data for
    the two teams
    :param fixture_id:
    :return:
    """
    response = make_request("/fixtures/" + str(fixture_id))
    json_dict = json.loads(response.text)

    head2head = decoders.to_headtohead(json_dict['head2head'])
    fixture = decoders.to_fixture(json_dict['fixture'])
    fixture_id_str = str(fixture_id)

    # Remove current fixture from head to head collection
    for i, obj in enumerate(head2head.fixtures):
        if obj.fixture_id == fixture_id_str:
            del head2head.fixtures[i]
            break

    fixture.head_to_head = head2head

    return fixture


def get_league_table(competition_id: int) -> Union[LeagueTable, Dict[str, LeagueTable]]:
    """
    Retrieves league table data for the specified competition ID, and returns a LeagueTable object for normal leagues
    Returns a dictionary of LeagueTable objects if competition is a tournament e.g Euro 2016
    :param competition_id:
    :return:
    """
    response = make_request("competitions/" + str(competition_id) + "/leagueTable")
    json_dict = json.loads(response.text)
    league_table = decoders.to_league_table(json_dict)

    return league_table

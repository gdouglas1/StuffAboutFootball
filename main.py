import operator

from flask import Flask, render_template
import footballapi
from model import LeagueTable

app = Flask(__name__)


@app.route("/")
def index():
    """
    Controller for root
    :return:
    """
    return get_competitions()


@app.route("/GetCompetitions")
def get_competitions():
    """
    Controller for getting all competitions
    :return:
    """
    competitions = footballapi.get_competitions()
    return render_template("competitions.html", **locals())


@app.route("/Competition/<int:competition_id>")
def get_competition(competition_id: int):
    """
    Controller for returning data regarding the specified competition ID
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)
    return render_template("competition.html", **locals())


@app.route("/Competition/<int:competition_id>/teams")
def get_teams_for_competition(competition_id: int):
    """
    Controller for getting all teams taking part in the specified competition
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)
    teams = footballapi.get_teams_for_competition(competition_id)
    return render_template("competition_teams.html", **locals())


@app.route("/Competition/<int:competition_id>/fixtures")
def get_fixtures_for_competition(competition_id: int):
    """
    Controller for retrieving Fixture data for all fixtures for the specified competition
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)

    fixture_list_type = "competition"
    page_title = competition.name
    title_id = competition_id

    all_fixtures = footballapi.get_fixtures_for_competition(competition_id)

    ungrouped_results = [x for x in all_fixtures if x.fixture_status == "FINISHED"]
    ungrouped_results.sort(key=operator.attrgetter('match_day'), reverse=True)
    results = footballapi.group_fixtures_by_match_day(ungrouped_results)

    ungrouped_fixtures = [x for x in all_fixtures if x.fixture_status != "FINISHED"]
    ungrouped_fixtures.sort(key=operator.attrgetter('match_day'))
    fixtures = footballapi.group_fixtures_by_match_day(ungrouped_fixtures)

    return render_template("fixtures.html", **locals())


@app.route("/Fixtures/<int:fixture_id>")
def get_fixture(fixture_id: int):
    """
    Controller for retrieving Fixture data for the specified fixture ID
    :param fixture_id:
    :return:
    """
    fixture = footballapi.get_fixture(fixture_id)
    competition = footballapi.get_competition(fixture.competition_id)
    home_team = footballapi.get_team(int(fixture.home_team_id))
    away_team = footballapi.get_team(int(fixture.away_team_id))
    return render_template("fixture.html", **locals())


@app.route("/Competition/<int:competition_id>/table")
def get_table_for_competition(competition_id: int):
    """
    Controller for retrieving league table info
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)
    league_table = footballapi.get_league_table(competition_id)

    # Check if returned league_table object is a single table, or list of tables
    # Use normal template if single table, or competition template for group of tables
    if type(league_table) is LeagueTable:
        return render_template("league_table.html", **locals())
    else:
        return render_template("competition_league_table.html", **locals())


@app.route("/Teams/<int:team_id>")
def get_team(team_id: int):
    team = footballapi.get_team(team_id)
    return render_template("team.html", **locals())


@app.route("/Teams/<int:team_id>/fixtures")
def get_fixtures_for_team(team_id: int):
    team = footballapi.get_team(team_id)

    fixture_list_type = "team"
    page_title = team.name
    title_id = team_id

    all_fixtures = footballapi.get_fixtures_for_team(team_id)

    ungrouped_results = [x for x in all_fixtures if x.fixture_status == "FINISHED"]
    ungrouped_results.sort(key=operator.attrgetter('match_day'), reverse=True)
    results = footballapi.group_fixtures_by_match_day(ungrouped_results)

    ungrouped_fixtures = [x for x in all_fixtures if x.fixture_status != "FINISHED"]
    ungrouped_fixtures.sort(key=operator.attrgetter('match_day'))
    fixtures = footballapi.group_fixtures_by_match_day(ungrouped_fixtures)

    return render_template("fixtures.html", **locals())


@app.route("/Teams/<int:team_id>/players/grouped")
def get_players_for_team_grouped(team_id: int):
    team = footballapi.get_team(team_id)
    players_grouped = footballapi.get_players_grouped(team_id)

    return render_template("players_by_position.html", **locals())


@app.route("/Teams/<int:team_id>/players")
def get_players_for_team_ungrouped(team_id: int):
    team = footballapi.get_team(team_id)
    players = footballapi.get_players_ungrouped(team_id)

    return render_template("players.html", **locals())

if __name__ == '__main__':
    app.run(debug=True)

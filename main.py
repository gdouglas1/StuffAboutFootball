import operator

from flask import Flask, render_template
import footballapi

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
def get_competition(competition_id):
    """
    Controller for returning data regarding the specified competition ID
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)
    return render_template("competition.html", **locals())


@app.route("/Competition/<int:competition_id>/teams")
def get_teams_for_competition(competition_id):
    """
    Controller for getting all teams taking part in the specified competition
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)
    teams = footballapi.get_teams_for_competition(competition_id)
    return render_template("competition_teams.html", **locals())


@app.route("/Competition/<int:competition_id>/fixtures")
def get_fixtures_for_competition(competition_id):
    """
    Controller for retrieving Fixture data for all fixtures for the specified competition
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)

    fixture_list_type = "competition"
    page_title = competition.name
    title_id = competition_id

    fixtures = footballapi.get_fixtures_for_competition(competition_id)

    results = [x for x in fixtures if x.fixture_status == "FINISHED"]
    results.sort(key=operator.attrgetter('match_day'), reverse=True)
    results = footballapi.group_fixtures_by_match_day(results)

    fixtures = [x for x in fixtures if x.fixture_status != "FINISHED"]
    fixtures.sort(key=operator.attrgetter('match_day'))
    fixtures = footballapi.group_fixtures_by_match_day(fixtures)

    return render_template("fixtures.html", **locals())


@app.route("/Fixtures/<int:fixture_id>")
def get_fixture(fixture_id):
    """
    Controller for retrieving Fixture data for the specified fixture ID
    :param fixture_id:
    :return:
    """
    fixture = footballapi.get_fixture(fixture_id)
    competition = footballapi.get_competition(fixture.competition_id)
    home_team = footballapi.get_team(fixture.home_team_id)
    away_team = footballapi.get_team(fixture.away_team_id)
    return render_template("fixture.html", **locals())


@app.route("/Competition/<int:competition_id>/table")
def get_table_for_competition(competition_id):
    """
    Controller for retrieving league table info
    :param competition_id:
    :return:
    """
    competition = footballapi.get_competition(competition_id)
    league_table = footballapi.get_league_table(competition_id)

    return render_template("league_table.html", **locals())


@app.route("/Teams/<int:team_id>")
def get_team(team_id):
    team = footballapi.get_team(team_id)
    return render_template("team.html", **locals())


@app.route("/Teams/<int:team_id>/fixtures")
def get_fixtures_for_team(team_id):
    team = footballapi.get_team(team_id)

    fixture_list_type = "team"
    page_title = team.name
    title_id = team_id

    fixtures = footballapi.get_fixtures_for_team(team_id)

    results = [x for x in fixtures if x.fixture_status == "FINISHED"]
    results.sort(key=operator.attrgetter('matchday'), reverse=True)
    results = footballapi.group_fixtures_by_match_day(results)

    fixtures = [x for x in fixtures if x.fixture_status != "FINISHED"]
    fixtures.sort(key=operator.attrgetter('matchday'))
    fixtures = footballapi.group_fixtures_by_match_day(fixtures)

    return render_template("fixtures.html", **locals())


@app.route("/Teams/<int:team_id>/players/grouped")
def get_players_for_team_grouped(team_id):
    team = footballapi.get_team(team_id)
    players_grouped = footballapi.get_players_grouped(team_id)

    return render_template("players_by_position.html", **locals())


@app.route("/Teams/<int:team_id>/players")
def get_players_for_team_ungrouped(team_id):
    team = footballapi.get_team(team_id)
    players = footballapi.get_players_ungrouped(team_id)

    return render_template("players.html", **locals())

if __name__ == '__main__':
    app.run(debug=True)

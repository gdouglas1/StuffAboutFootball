import json
import unittest

import datetime

import decoders

class DecoderTestCase(unittest.TestCase):
    def test_to_competition(self):
        competition_json = "{\"_links\":" \
                            "{\"self\":" \
                                "{\"href\":\"http://api.football-data.org/v1/competitions/431\"}," \
                           "\"teams\":" \
                            "{\"href\":\"http://api.football-data.org/v1/competitions/431/teams\"}," \
                           "\"fixtures\":" \
                            "{\"href\":\"http://api.football-data.org/v1/competitions/431/fixtures\"}," \
                           "\"leagueTable\":" \
                            "{\"href\":\"http://api.football-data.org/v1/competitions/431/leagueTable\"}}," \
                           "\"id\":431," \
                           "\"caption\":\"2. Bundesliga 2016/17\"," \
                           "\"league\":\"BL2\"," \
                           "\"year\":\"2016\"," \
                           "\"currentMatchday\":9," \
                           "\"numberOfMatchdays\":34," \
                           "\"numberOfTeams\":18," \
                           "\"numberOfGames\":306," \
                           "\"lastUpdated\":\"2016-10-13T00:02:46Z\"}"

        json_dict = json.loads(competition_json)
        competition = decoders.to_competition(json_dict)

        self.assertEqual(competition.id, 431)
        self.assertEqual(competition.name, "2. Bundesliga 2016/17")
        self.assertEqual(competition.year, "2016")

    def test_to_team(self):
        team_json = "{\"_links\":" \
                        "{\"self\":" \
                            "{\"href\":\"http://api.football-data.org/v1/teams/57\"}," \
                        "\"fixtures\":" \
                            "{\"href\":\"http://api.football-data.org/v1/teams/57/fixtures\"}," \
                        "\"players\":" \
                            "{\"href\":\"http://api.football-data.org/v1/teams/57/players\"}}," \
                    "\"name\":\"Arsenal FC\"," \
                    "\"code\":\"AFC\"," \
                    "\"shortName\":\"Arsenal\"," \
                    "\"squadMarketValue\":\"468,500,000 €\"," \
                    "\"crestUrl\":\"http://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg\"}"
        json_dict = json.loads(team_json)
        team = decoders.to_team(json_dict)

        self.assertEqual(team.name, "Arsenal FC")
        self.assertEqual(team.id, "57")
        self.assertEqual(team.crest_url, "http://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg")
        self.assertEqual(team.market_value, "468,500,000 €")
        self.assertEqual(team.short_name, "Arsenal")

    def test_to_competitions(self):
        competitions_json = "[" \
                            "{\"_links\":" \
                                "{\"self\":{\"href\":\"http://api.football-data.org/v1/competitions/424\"}," \
                            "\"teams\":" \
                                "{\"href\":\"http://api.football-data.org/v1/competitions/424/teams\"}" \
                            ",\"fixtures\":" \
                                "{\"href\":\"http://api.football-data.org/v1/competitions/424/fixtures\"}," \
                            "\"leagueTable\":" \
                                "{\"href\":\"http://api.football-data.org/v1/competitions/424/leagueTable\"}}," \
                            "\"id\":424," \
                            "\"caption\":\"European Championships France 2016\"," \
                            "\"league\":\"EC\"," \
                            "\"year\":\"2016\"," \
                            "\"currentMatchday\":7," \
                            "\"numberOfMatchdays\":7," \
                            "\"numberOfTeams\":24," \
                            "\"numberOfGames\":51," \
                            "\"lastUpdated\":\"2016-07-10T21:32:20Z\"}," \
                            "{\"_links\":" \
                                "{\"self\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/426\"}," \
                                "\"teams\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/426/teams\"}," \
                                "\"fixtures\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/426/fixtures\"}," \
                                "\"leagueTable\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/426/leagueTable\"}}," \
                            "\"id\":426," \
                            "\"caption\":\"Premier League 2016/17\"," \
                            "\"league\":\"PL\"," \
                            "\"year\":\"2016\"," \
                            "\"currentMatchday\":8," \
                            "\"numberOfMatchdays\":38," \
                            "\"numberOfTeams\":20," \
                            "\"numberOfGames\":380," \
                            "\"lastUpdated\":\"2016-10-13T00:00:27Z\"}," \
                            "{\"_links\":" \
                                "{\"self\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/427\"}," \
                                "\"teams\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/427/teams\"}," \
                                "\"fixtures\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/427/fixtures\"}," \
                                "\"leagueTable\":" \
                                    "{\"href\":\"http://api.football-data.org/v1/competitions/427/leagueTable\"}}," \
                            "\"id\":427," \
                            "\"caption\":\"Championship 2016/17\"," \
                            "\"league\":\"ELC\"," \
                            "\"year\":\"2016\"," \
                            "\"currentMatchday\":12," \
                            "\"numberOfMatchdays\":46," \
                            "\"numberOfTeams\":24," \
                            "\"numberOfGames\":552," \
                            "\"lastUpdated\":\"2016-10-13T00:00:57Z\"}" \
                            "]"

        json_dict = json.loads(competitions_json)
        competitions = decoders.to_competitions(json_dict)

        self.assertEqual(len(competitions), 3)

        self.assertEqual(competitions[0].id, 424)
        self.assertEqual(competitions[0].name, "European Championships France 2016")
        self.assertEqual(competitions[0].year, "2016")

        self.assertEqual(competitions[1].id, 426)
        self.assertEqual(competitions[1].name, "Premier League 2016/17")
        self.assertEqual(competitions[1].year, "2016")

        self.assertEqual(competitions[2].id, 427)
        self.assertEqual(competitions[2].name, "Championship 2016/17")
        self.assertEqual(competitions[2].year, "2016")

    def test_to_player(self):
        player_json = "{\"name\":\"Shkodran Mustafi\"," \
                      "\"position\":\"Centre Back\"," \
                      "\"jerseyNumber\":20," \
                      "\"dateOfBirth\":\"1992-04-17\"," \
                      "\"nationality\":\"Germany\"," \
                      "\"contractUntil\":\"2021-06-30\"," \
                      "\"marketValue\":\"20,000,000 €\"}"

        json_dict = json.loads(player_json)
        player = decoders.to_player(json_dict)

        self.assertEqual(player.name, "Shkodran Mustafi")
        self.assertEqual(player.market_value, "20,000,000 €")
        self.assertEqual(player.age, 24)
        self.assertEqual(player.contract_duration_years, 4)
        self.assertEqual(player.contract_until, "30/06/2021")
        self.assertEqual(player.dob, "17/04/1992")
        self.assertEqual(player.jersey_number, 20)
        self.assertEqual(player.nationality, "Germany")
        self.assertEqual(player.position, "Centre Back")

    def test_to_result(self):
        result_json = "{\"goalsHomeTeam\":4," \
                      "\"goalsAwayTeam\":3, " \
                      "\"halfTime\":" \
                        "{\"goalsHomeTeam\":3, " \
                        "\"goalsAwayTeam\": 2}" \
                      "}"

        json_dict = json.loads(result_json)
        result = decoders.to_result(json_dict)

        self.assertEqual(result.away_team_goals, 3)
        self.assertEqual(result.home_team_goals, 4)
        self.assertEqual(result.halftime_away_team_goals, 2)
        self.assertEqual(result.halftime_home_team_goals, 3)


    def test_to_teamform(self):
        team_form_json = "{\"goals\":9," \
                         "\"goalsAgainst\":2," \
                         "\"wins\":3," \
                         "\"draws\":0," \
                         "\"losses\":0" \
                         "}"

        json_dict = json.loads(team_form_json)
        teamform = decoders.to_teamform(json_dict)

        self.assertEqual(teamform.wins, 3)
        self.assertEqual(teamform.draws, 0)
        self.assertEqual(teamform.losses, 0)
        self.assertEqual(teamform.goals_for, 9)
        self.assertEqual(teamform.goals_against, 2)


    def test_to_headtohead(self):
        return None


    def test_to_standing(self):
        standing_json = "{" \
                          "\"_links\": {" \
                            "\"team\": {" \
                              "\"href\": \"http://api.football-data.org/v1/teams/65\"" \
                            "}" \
                          "}," \
                          "\"position\": 1," \
                          "\"teamName\": \"Manchester City FC\"," \
                          "\"crestURI\": \"https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg\"," \
                          "\"playedGames\": 7," \
                          "\"points\": 18," \
                          "\"goals\": 18," \
                          "\"goalsAgainst\": 7," \
                          "\"goalDifference\": 11," \
                          "\"wins\": 6," \
                          "\"draws\": 0," \
                          "\"losses\": 1," \
                          "\"home\": {" \
                            "\"goals\": 9," \
                            "\"goalsAgainst\": 2," \
                            "\"wins\": 3," \
                            "\"draws\": 0," \
                            "\"losses\": 0" \
                          "}," \
                          "\"away\": {" \
                            "\"goals\": 9," \
                            "\"goalsAgainst\": 5," \
                            "\"wins\": 3," \
                            "\"draws\": 0," \
                            "\"losses\": 1" \
                          "}" \
                        "}"

        json_dict = json.loads(standing_json)
        standing = decoders.to_leaguetable_standing(json_dict)

        self.assertEqual(standing.team_name, "Manchester City FC")
        self.assertEqual(standing.team_id, "65")
        self.assertEqual(standing.goals, 18)
        self.assertEqual(standing.points, 18)
        self.assertEqual(standing.position, 1)
        self.assertEqual(standing.team_form.wins, 6)
        self.assertEqual(standing.team_form.draws, 0)
        self.assertEqual(standing.team_form.losses, 1)
        self.assertEqual(standing.team_form.goals_for, 18)
        self.assertEqual(standing.team_form.goals_against, 7)
        self.assertEqual(standing.home_form.wins, 3)
        self.assertEqual(standing.home_form.draws, 0)
        self.assertEqual(standing.home_form.losses, 0)
        self.assertEqual(standing.home_form.goals_for, 9)
        self.assertEqual(standing.home_form.goals_against, 2)
        self.assertEqual(standing.away_form.wins, 3)
        self.assertEqual(standing.away_form.draws, 0)
        self.assertEqual(standing.away_form.losses, 1)
        self.assertEqual(standing.away_form.goals_for, 9)
        self.assertEqual(standing.away_form.goals_against, 5)


    def test_to_fixture(self):
        fixture_json = "{\"_links\":{\"self\":{\"href\":\"http://api.football-data.org/v1/fixtures/150766\"},\"competition\":{\"href\":\"http://api.football-data.org/v1/competitions/426\"},\"homeTeam\":{\"href\":\"http://api.football-data.org/v1/teams/57\"},\"awayTeam\":{\"href\":\"http://api.football-data.org/v1/teams/72\"}},\"date\":\"2016-10-15T00:00:00Z\",\"status\":\"TIMED\",\"matchday\":8,\"homeTeamName\":\"Arsenal FC\",\"awayTeamName\":\"Swansea City FC\",\"result\":{\"goalsHomeTeam\":null,\"goalsAwayTeam\":null},\"odds\":null}"

        json_dict = json.loads(fixture_json)
        fixture = decoders.to_fixture(json_dict)

        self.assertEqual(fixture.away_team_id, "72")
        self.assertEqual(fixture.away_team_name, "Swansea City FC")
        self.assertEqual(fixture.competition_id, "426")
        self.assertEqual(fixture.fixture_actual_date, datetime.datetime(2016, 10, 15))
        self.assertEqual(fixture.fixture_id, "150766")
        self.assertEqual(fixture.fixture_date, "15/10/2016")
        self.assertEqual(fixture.fixture_status, "TIMED")
        self.assertEqual(fixture.home_team_id, "57")
        self.assertEqual(fixture.home_team_name, "Arsenal FC")
        self.assertEqual(fixture.match_day, 8)

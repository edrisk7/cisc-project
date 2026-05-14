from drafter import *
from teams_data import *
import random


@dataclass
'''
stores all user selections and prediction choices for the NBA matchup simulator website
'''
class State:
    home_team: str
    away_team: str
    message: str
    predicted_winner: str

    home_lead_scorer_ou: str
    home_second_scorer_ou: str
    home_lead_rebounder_ou: str
    home_lead_assister_ou: str

    away_lead_scorer_ou: str
    away_second_scorer_ou: str
    away_lead_rebounder_ou: str
    away_lead_assister_ou: str


def get_team_names():
    '''
    gets all team names for dropdown menu
    '''
    return [team.name for team in TEAMS]


def find_team(name):
    '''
    finds team object from string name
    '''
    for team in TEAMS:
        if team.name == name:
            return team
    return TEAMS[0]


def stat_table(team):
    '''
    displays player stats before prediction page
    '''
    content = [Header(team.name + " Players")]

    for player in team.members:
        content.append(Text(player.name))
        content.append(Text(player.position))
        content.append(Text(str(player.ppg) + " PPG"))
        content.append(Text(str(player.apg) + " APG"))
        content.append(Text(str(player.rpg) + " RPG"))
        content.append(Text("-------------"))

    return content


def top_players(team):
    '''
    gets top scorers rebounders and assisters based on ratings
    '''
    off_players = sorted(team.members, key=lambda player: player.off_rating, reverse=True)
    def_players = sorted(team.members, key=lambda player: player.def_rating, reverse=True)

    return (
        off_players[0].name,
        off_players[1].name,
        def_players[0].name,
        off_players[0].name
    )


def make_box_scores(team, team_score):
    
    '''
    simulates realistic box scores
    
    points use offensive rating
    
    rebounds use defense + bigs
    
    assists use offense + guards
    '''
    
    point_players = sorted(team.members, key=lambda player: player.off_rating, reverse=True)
    point_shares = [0.20, 0.175, 0.15, 0.125, 0.10, 0.10, 0.075, 0.075]

    bigs = []
    guards = []

    for player in team.members:
        if player.position == "C" or player.position == "F":
            bigs.append(player)
        else:
            guards.append(player)

    # bigs get rebound priority
    rebound_bigs = sorted(bigs, key=lambda player: player.def_rating, reverse=True)
    rebound_guards = sorted(guards, key=lambda player: player.def_rating, reverse=True)
    rebound_players = rebound_bigs + rebound_guards
    rebound_shares = [0.20, 0.175, 0.15, 0.125, 0.15, 0.10, 0.075, 0.025]

    # guards get assist priority
    assist_guards = sorted(guards, key=lambda player: player.off_rating, reverse=True)
    assist_bigs = sorted(bigs, key=lambda player: player.off_rating, reverse=True)
    assist_players = assist_guards + assist_bigs
    assist_shares = [0.20, 0.175, 0.15, 0.125, 0.15, 0.10, 0.075, 0.025]

    total_rebounds = int(team_score * 0.35)
    total_assists = int(team_score * 0.22)

    box_scores = []

    for player in team.members:
        points = 0
        rebounds = 0
        assists = 0

        for i in range(len(point_players)):
            if point_players[i].name == player.name:
                points = int(team_score * point_shares[i])

        for i in range(len(rebound_players)):
            if rebound_players[i].name == player.name:
                rebounds = int(total_rebounds * rebound_shares[i])

        for i in range(len(assist_players)):
            if assist_players[i].name == player.name:
                assists = int(total_assists * assist_shares[i])

        box_scores.append([player.name, points, rebounds, assists])

    return box_scores


def get_player_stat(box_scores, player_name, stat_name):
    
    '''
    finds a players stat used for prediction checks
    '''
    
    for stat_line in box_scores:
        if stat_line[0] == player_name:
            if stat_name == "points":
                return stat_line[1]
            elif stat_name == "rebounds":
                return stat_line[2]
            elif stat_name == "assists":
                return stat_line[3]
    return 0


def check_over_under(choice, actual_value, line):
    '''
    checks if over under pick is right or wrong
    '''
    
    if "Over" in choice and actual_value > line:
        return True
    elif "Under" in choice and actual_value < line:
        return True
    else:
        return False


def add_box_score_to_page(content, team_name, box_scores, selected_players):
    '''
    adds box score to results page
    '''
   
    content.append(Header(team_name))
    
    for stat_line in box_scores:
        name = stat_line[0]
        points = stat_line[1]
        rebounds = stat_line[2]
        assists = stat_line[3]

        if name in selected_players:
            content.append(Text("*** " + name + " ***"))
        else:
            content.append(Text(name))

        content.append(LineBreak())
        content.append(Text(str(points) + " PTS"))
        content.append(LineBreak())
        content.append(Text(str(rebounds) + " REB"))
        content.append(LineBreak())
        content.append(Text(str(assists) + " AST"))
        content.append(LineBreak())
        content.append(LineBreak())

    return content


def add_prediction_result(content, prediction_name, user_pick, actual_value, line, correct):
    '''
    adds each prediction result to final results page
    '''
    
    if check_over_under(user_pick, actual_value, line):
        result = "Correct"
        correct = correct + 1
    else:
        result = "Incorrect"

    content.append(Text(prediction_name))
    content.append(LineBreak())
    content.append(Text("Pick: " + user_pick))
    content.append(LineBreak())
    content.append(Text("Actual: " + str(actual_value)))
    content.append(LineBreak())
    content.append(Text(result))
    content.append(LineBreak())
    content.append(LineBreak())

    return correct


@route
def index(state: State) -> Page:
   
    '''
    homepage
    '''
    return Page(state, [
        Header("NBA Simulator"),
        Text("Pick teams, make predictions, simulate games, and earn points."),
        Button("Rules", rules),
        Button("Pick Teams", pick_teams)
    ])


@route
def rules(state: State) -> Page:
   
    '''
    explains game rules
    '''
   
    return Page(state, [
        Header("Rules"),
        Text("1. Pick a home team and an away team."),
        Text("2. Fill out the prediction sheet before the game starts."),
        Text("3. You will predict the winner and choose Over or Under for player stat lines."),
        Text("4. The stat lines are based on the teams best players in each category."),
        Text("5. After predictions are saved the game will be simulated."),
        Text("6. Team rating controls how many possession loops each team gets."),
        Text("7. Each possession gives a team 0 to 3 points."),
        Text("8. After the game your predictions will be checked."),
        Button("Pick Teams", pick_teams),
        Button("Back Home", index)
    ])


@route
def pick_teams(state: State) -> Page:
    
    '''
    user selects teams
    '''
    
    return Page(state, [
        Header("Pick Teams"),
        Text("Home Team:"),
        SelectBox("home_team", get_team_names(), state.home_team),
        Text("Away Team:"),
        SelectBox("away_team", get_team_names(), state.away_team),
        Button("Continue", save_matchup),
        Button("Back Home", index)
    ])


@route
def save_matchup(state: State, home_team: str, away_team: str) -> Page:
    
    '''
    saves selected matchup
    '''
    
    state.home_team = home_team
    state.away_team = away_team
    state.predicted_winner = home_team

    if home_team == away_team:
        return Page(state, [
            Header("Matchup Error"),
            Text("Please pick two different teams."),
            Button("Pick Again", pick_teams),
            Button("Back Home", index)
        ])

    return Page(state, [
        Header("Matchup Saved"),
        Text(state.home_team + " vs " + state.away_team),
        Button("Fill Out Predictions", prediction_sheet),
        Button("Change Teams", pick_teams),
        Button("Back Home", index)
    ])


@route
def prediction_sheet(state: State) -> Page:
    
    '''
    page where user makes predictions
    '''
    
    home = find_team(state.home_team)
    away = find_team(state.away_team)

    home_top, home_second, home_reb, home_ast = top_players(home)
    away_top, away_second, away_reb, away_ast = top_players(away)

    content = [
        Header("Prediction Sheet"),
        Text("Pick the winner and choose Over or Under for each player line."),
        Text("Game Winner:"),
        SelectBox("predicted_winner", [state.home_team, state.away_team], state.predicted_winner),
        Text("")
    ]

    content += stat_table(home)

    content += [
        Header(state.home_team + " Predictions"),
        Text(home_top + " points"),
        SelectBox("home_lead_scorer_ou", ["Over 29.5", "Under 29.5"], state.home_lead_scorer_ou),
        Text(home_second + " points"),
        SelectBox("home_second_scorer_ou", ["Over 24.5", "Under 24.5"], state.home_second_scorer_ou),
        Text(home_reb + " rebounds"),
        SelectBox("home_lead_rebounder_ou", ["Over 9.5", "Under 9.5"], state.home_lead_rebounder_ou),
        Text(home_ast + " assists"),
        SelectBox("home_lead_assister_ou", ["Over 7.5", "Under 7.5"], state.home_lead_assister_ou),
        Text("")
    ]

    content += stat_table(away)

    content += [
        Header(state.away_team + " Predictions"),
        Text(away_top + " points"),
        SelectBox("away_lead_scorer_ou", ["Over 29.5", "Under 29.5"], state.away_lead_scorer_ou),
        Text(away_second + " points"),
        SelectBox("away_second_scorer_ou", ["Over 24.5", "Under 24.5"], state.away_second_scorer_ou),
        Text(away_reb + " rebounds"),
        SelectBox("away_lead_rebounder_ou", ["Over 9.5", "Under 9.5"], state.away_lead_rebounder_ou),
        Text(away_ast + " assists"),
        SelectBox("away_lead_assister_ou", ["Over 7.5", "Under 7.5"], state.away_lead_assister_ou),
        Button("Save Predictions", save_predictions),
        Button("Change Teams", pick_teams),
        Button("Back Home", index)
    ]

    return Page(state, content)


@route
def save_predictions(state: State,
                     predicted_winner: str,
                     home_lead_scorer_ou: str,
                     home_second_scorer_ou: str,
                     home_lead_rebounder_ou: str,
                     home_lead_assister_ou: str,
                     away_lead_scorer_ou: str,
                     away_second_scorer_ou: str,
                     away_lead_rebounder_ou: str,
                     away_lead_assister_ou: str) -> Page:
    '''
    stores all user predictions
    '''
    state.predicted_winner = predicted_winner
    state.home_lead_scorer_ou = home_lead_scorer_ou
    state.home_second_scorer_ou = home_second_scorer_ou
    state.home_lead_rebounder_ou = home_lead_rebounder_ou
    state.home_lead_assister_ou = home_lead_assister_ou
    state.away_lead_scorer_ou = away_lead_scorer_ou
    state.away_second_scorer_ou = away_second_scorer_ou
    state.away_lead_rebounder_ou = away_lead_rebounder_ou
    state.away_lead_assister_ou = away_lead_assister_ou

    return Page(state, [
        Header("Predictions Saved"),
        Text("Pick: " + state.predicted_winner),
        Text("Your predictions are saved."),
        Button("Simulate Game", results),
        Button("Edit Predictions", prediction_sheet),
        Button("Back Home", index)
    ])


@route
def results(state: State) -> Page:
    '''
    simulates full game then checks all predictions
    '''
    home = find_team(state.home_team)
    away = find_team(state.away_team)

    home_score = 0
    away_score = 0

    # possessions based on team rating
    for possession in range(home.rating * 10):
        home_score = home_score + random.randint(0, 3)

    for possession in range(away.rating * 10):
        away_score = away_score + random.randint(0, 3)

    # higher score wins game
    if home_score > away_score:
        actual_winner = state.home_team
    else:
        actual_winner = state.away_team

    home_box_scores = make_box_scores(home, home_score)
    away_box_scores = make_box_scores(away, away_score)

    home_top, home_second, home_reb, home_ast = top_players(home)
    away_top, away_second, away_reb, away_ast = top_players(away)

    home_selected = [home_top, home_second, home_reb, home_ast]
    away_selected = [away_top, away_second, away_reb, away_ast]

    correct = 0
    total = 9

    content = [
        Header("Game Results"),
        Text(state.home_team),
        LineBreak(),
        Text(str(home_score)),
        LineBreak(),
        LineBreak(),
        Text(state.away_team),
        LineBreak(),
        Text(str(away_score)),
        LineBreak(),
        LineBreak(),
        Text("Winning Team: " + actual_winner),
        LineBreak(),
        LineBreak()
    ]

    content = add_box_score_to_page(content, state.home_team, home_box_scores, home_selected)
    content = add_box_score_to_page(content, state.away_team, away_box_scores, away_selected)

    content.append(Header("Prediction Check"))
    content.append(LineBreak())

    content.append(Text("Winner"))
    content.append(LineBreak())
    content.append(Text("Pick: " + state.predicted_winner))
    content.append(LineBreak())
    content.append(Text("Actual: " + actual_winner))
    content.append(LineBreak())

    if state.predicted_winner == actual_winner:
        content.append(Text("Correct"))
        content.append(LineBreak())
        content.append(LineBreak())
        correct = correct + 1
    else:
        content.append(Text("Incorrect"))
        content.append(LineBreak())
        content.append(LineBreak())

    # gets generated stats for prediction checks
    home_top_points = get_player_stat(home_box_scores, home_top, "points")
    home_second_points = get_player_stat(home_box_scores, home_second, "points")
    home_rebounds = get_player_stat(home_box_scores, home_reb, "rebounds")
    home_assists = get_player_stat(home_box_scores, home_ast, "assists")

    away_top_points = get_player_stat(away_box_scores, away_top, "points")
    away_second_points = get_player_stat(away_box_scores, away_second, "points")
    away_rebounds = get_player_stat(away_box_scores, away_reb, "rebounds")
    away_assists = get_player_stat(away_box_scores, away_ast, "assists")

    correct = add_prediction_result(content, home_top + " Points", state.home_lead_scorer_ou, home_top_points, 29.5, correct)
    correct = add_prediction_result(content, home_second + " Points", state.home_second_scorer_ou, home_second_points, 24.5, correct)
    correct = add_prediction_result(content, home_reb + " Rebounds", state.home_lead_rebounder_ou, home_rebounds, 9.5, correct)
    correct = add_prediction_result(content, home_ast + " Assists", state.home_lead_assister_ou, home_assists, 7.5, correct)

    correct = add_prediction_result(content, away_top + " Points", state.away_lead_scorer_ou, away_top_points, 29.5, correct)
    correct = add_prediction_result(content, away_second + " Points", state.away_second_scorer_ou, away_second_points, 24.5, correct)
    correct = add_prediction_result(content, away_reb + " Rebounds", state.away_lead_rebounder_ou, away_rebounds, 9.5, correct)
    correct = add_prediction_result(content, away_ast + " Assists", state.away_lead_assister_ou, away_assists, 7.5, correct)

    content.append(Header("Final Prediction Score"))
    content.append(Text(str(correct) + "/" + str(total) + " Correct"))
    content.append(LineBreak())

    content.append(Button("Play Again", pick_teams))

    return Page(state, content)

# starting state removes need for error checks and none values
start_server(State(
    "Sixers",
    "Lakers",
    "",
    "Sixers",
    "Over 29.5",
    "Over 24.5",
    "Over 9.5",
    "Over 7.5",
    "Over 29.5",
    "Over 24.5",
    "Over 9.5",
    "Over 7.5"
))

from drafter import *
from teams_data import *
set_site_information(
    author="your_email@udel.edu",
    description="""NBA game simulator with 8 of my favorite teams to make poredictions and earn points.""",
    sources=["https://www.espn.com/nba/teams"],
    planning=["Project Plab.pdf"],
    links=["https://github.com/edrisk7/cisc-project"]
)
hide_debug_information()
set_website_title("Your Website Title")
set_website_framed(False)
@dataclass
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
    return [team.name for team in TEAMS]

def find_team(name):
    for team in TEAMS:
        if team.name == name:
            return team
    return TEAMS[0]

def stat_table(team):
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
    off_players = sorted(team.members, key=lambda player: player.off_rating, reverse=True)
    def_players = sorted(team.members, key=lambda player: player.def_rating, reverse=True)

    return (
        off_players[0].name,
        off_players[1].name,
        def_players[0].name,
        off_players[0].name
    )

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("NBA Simulator"),
        Text("Pick teams, make predictions, simulate games, and earn points."),
        Button("Rules", rules),
        Button("Pick Teams", pick_teams)
    ])

@route
def rules(state: State) -> Page:
    return Page(state, [
        Header("Rules"),
        Text("1. Pick a home team and an away team."),
        Text("2. Fill out the prediction sheet before the game starts."),
        Text("3. You will predict the winner and choose Over or Under for player stat lines."),
        Text("4. The stat lines are based on the players shown on the prediction page."),
        Text("5. After predictions are saved, the game will be simulated."),
        Text("6. Team rating controls how many possession loops each team gets."),
        Text("7. Each possession gives a team 0 to 3 points."),
        Text("8. After the game, your predictions will be checked and you will earn points for correct picks."),
        Button("Pick Teams", pick_teams),
        Button("Back Home", index)
    ])

@route
def pick_teams(state: State) -> Page:
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
        Text("Winner: " + state.predicted_winner),
        Text("Your predictions are saved. Next we will add the simulation page."),
        Button("Edit Predictions", prediction_sheet),
        Button("Back Home", index)
    ])
                         
#initial conditions to avoid need for error msgs and None
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

from dataclasses import dataclass

@dataclass
class Player:
    name: str
    position: str
    off_rating: int
    def_rating: int
    ppg: float
    apg: float
    rpg: float

@dataclass
class Team:
    name: str
    conference: str
    rating: int
    members: list[Player]

sixers = Team("Sixers","East",8,[
    Player("Maxey","G",113,98,27,6,4),
    Player("Embiid","C",112,110,27,4,8),
    Player("George","F",106,104,17,4,5),
    Player("Edgecombe","G",101,99,14,3,4),
    Player("Grimes","G",99,101,13,3,4),
    Player("Oubre","F",97,100,12,2,5),
    Player("Drummond","C",88,105,6,1,8),
    Player("Lowry","G",87,97,5,4,2)
])

celtics = Team("Celtics","East",9,[
    Player("Brown","F",112,104,25,3,6),
    Player("Tatum","F",111,104,24,5,8),
    Player("White","G",106,108,17,5,4),
    Player("Pritchard","G",103,94,15,4,3),
    Player("Hauser","F",98,96,10,1,4),
    Player("Queta","C",91,103,7,1,7),
    Player("Kornet","C",90,102,6,1,5),
    Player("Scheierman","G",88,93,5,2,3)
])

pistons = Team("Pistons","East",8,[
    Player("Cunningham","G",114,101,26,8,6),
    Player("Duren","C",101,108,14,3,11),
    Player("Harris","F",102,99,15,2,6),
    Player("Thompson","F",96,110,11,3,7),
    Player("Robinson","G",99,92,11,2,3),
    Player("LeVert","G",98,96,10,4,3),
    Player("Holland","F",94,101,9,2,4),
    Player("Stewart","C",90,105,8,1,7)
])

cavs = Team("Cleveland","East",8,[
    Player("Mitchell","G",114,101,27,5,5),
    Player("Harden","G",108,96,17,8,5),
    Player("Mobley","F",106,112,19,4,9),
    Player("Allen","C",100,109,14,2,10),
    Player("Strus","G",96,98,11,3,4),
    Player("Hunter","F",98,101,12,2,4),
    Player("Ball","G",92,103,8,5,4),
    Player("Tyson","F",90,99,7,2,4)
])

spurs = Team("Spurs","West",9,[
    Player("Wemby","C",115,118,25,3,12),
    Player("Fox","G",112,99,23,7,4),
    Player("Vassell","G",104,98,16,4,4),
    Player("Harper","G",102,97,14,4,5),
    Player("Castle","G",101,103,14,4,5),
    Player("Keldon","F",99,98,13,2,5),
    Player("Champagnie","F",96,99,10,2,4),
    Player("Sochan","F",94,104,9,3,6)
])

okc = Team("OKC","West",10,[
    Player("SGA","G",118,104,34,6,5),
    Player("Jalen Williams","F",110,105,20,5,5),
    Player("Holmgren","C",106,112,17,2,8),
    Player("Dort","G",96,107,10,2,4),
    Player("Hartenstein","C",92,109,8,3,9),
    Player("Wallace","G",94,104,8,3,3),
    Player("Wiggins","F",93,98,8,2,4),
    Player("Joe","G",92,95,9,2,3)
])

lakers = Team("Lakers","West",8,[
    Player("Doncic","G",118,96,33,8,9),
    Player("LeBron","F",112,102,25,8,8),
    Player("Reaves","G",108,97,23,6,5),
    Player("Ayton","C",101,104,14,2,10),
    Player("Hachimura","F",99,97,12,1,5),
    Player("Hayes","C",90,101,7,1,5),
    Player("Vincent","G",88,97,6,2,2),
    Player("Vanderbilt","F",86,105,5,2,6)
])

wolves = Team("Timberwolves","West",8,[
    Player("Edwards","G",116,103,27,5,6),
    Player("Randle","F",106,99,19,4,7),
    Player("Gobert","C",96,113,12,1,11),
    Player("McDaniels","F",98,108,12,2,5),
    Player("Reid","C",101,101,13,2,5),
    Player("Conley","G",92,98,8,5,3),
    Player("Dosunmu","G",94,100,10,3,3),
    Player("Dillingham","G",91,92,8,3,2)
])

TEAMS = [sixers,celtics,pistons,cavs,spurs,okc,lakers,wolves]
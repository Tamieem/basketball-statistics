from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import scoreboard
from datetime import date, datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.offsetbox import OffsetImage


def get_games(game_id):
### Important Columns to note:  [4]=Quarter [6]=time left in quarter [10]= current score [11]= score margin (home team is postive)

    gameplay = playbyplayv2.PlayByPlayV2(game_id)
    pbp = gameplay.play_by_play.get_dict() ## [10] holds score, [11] holds score margin



if date.today() <= datetime.strptime("2019-04-30", "%Y-%m-%d").date():
    date = datetime.now().strftime("%Y-%m-%d")
else:
    date = "2019-04-30"
schedule = scoreboard.Scoreboard(day_offset='0', game_date=date, league_id='00').get_dict()['resultSets'][0]
## Will need to include a calendar option that will == schedule variable
# (with dropdown list of games refreshing on each on click action)

 #or sched in schedule:  ## Will need to produce a dropdown list of options of games that had happened within that day
    #print(sched)
game_id = schedule['rowSet'][0][2]
print("test")
get_games(game_id)


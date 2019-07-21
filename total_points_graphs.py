from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import scoreboard
from datetime import date, datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.offsetbox import OffsetImage

fig = plt.figure()
plt.ion()
def get_game(game_id):
### Important Columns to note:  [4]=Quarter [6]=time left in quarter [10]= current score  (AWAY_SCORE - HOME_SCORE) [11]= score margin (home team is postive)
    x_data = [[], [], [], []]
    y_data = [[], [], [], []]
    label_data = [[], [], [], []]
    gameplay = playbyplayv2.PlayByPlayV2(game_id)
    plays = gameplay.play_by_play.get_dict()['data'] ## [10] holds score, [11] holds score margin
    quarter = 0

    for play in plays:
        if play[11] is not None and play[6] != '0:00' and play[6] != '12:00':
            if quarter != int(play[4])-1:
                quarter = int(play[4]) - 1
            time = dates.date2num(datetime.strptime(play[6], '%M:%S'))
            time = (quarter * 12)+ time
            x_data[quarter].append(time)
            if play[11] == 'TIE':
                y_data[quarter].append(0)
            else:
                y_data[quarter].append(int(play[11]))
            if play[7] is None: # play[7] = Home team description
                label_data[quarter].append('' + play[9] + '\nScore: ' + play[10]) # play[9] = Away team description
            else:
                label_data[quarter].append('' + play[7] + '\nScore: ' + play[10])
    plt.plot(x_data[0], y_data[0], 'ro-')
    plt.xlim(dates.date2num(datetime.strptime('12:00', '%M:%S')), dates.date2num(datetime.strptime('00:00', '%M:%S')))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%M:%S'))
    plt.show()


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
get_game(game_id)


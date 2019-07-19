from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import boxscoreplayertrackv2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.offsetbox import OffsetImage
import urllib.request
from IPython.display import display


def create_court(ax =None, color='black', lw=2, out_lines=False):
    if ax is None:
        ax = plt.gca()

    #basketball hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill= False)

    #backboard
    backboard = Rectangle((-30, -7.5),60, -1, linewidth=lw, color=color, fill=False)

    #Paint
    outer_paint = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_paint = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    #free throw
    free_throw_top= Arc((0,142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    free_throw_bottom = Arc((0,142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    #restricted area
    restricted = Arc((0,0), 80,80, theta1=0, theta2=180, linewidth=lw, color=color,)

    #three point line
    corner_three1 = Rectangle((-220, -47.5), 0 , 140, linewidth=lw, color=color)
    corner_three2 = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0,0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    #center court
    center_outer = Arc((0, 422.5), 120, 120, theta2=0, theta1=180, linewidth=lw, color=color)
    center_inner = Arc((0, 422.5), 40, 40, theta1= 180, theta2=0, linewidth=lw, color=color)

    court = [hoop, backboard, outer_paint, inner_paint, free_throw_bottom, free_throw_top, restricted,
             corner_three1, corner_three2, three_arc, center_outer, center_inner]
    if out_lines:
        out_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court.append(out_lines)
    for item in court:
        ax.add_patch(item)

    return ax

player = shotchartdetail.ShotChartDetail(player_id=1628995, team_id=1610612752)
headers = player.shot_chart_detail.get_dict()['headers']
shots = player.shot_chart_detail.get_dict()['data']
pic_link = urllib.request.urlretrieve("https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+str(shots[0][3])+".png")
pic = plt.imread(pic_link[0])
shot_df = pd.DataFrame(shots, columns=headers)
sns.set_style("white")
sns.set_color_codes()
plt.figure(figsize=(12,11))
game_ids = shot_df.GAME_ID
for game_id in game_ids:
    game = playbyplayv2.PlayByPlayV2(game_id=game_id)
    boxscore = boxscoreplayertrackv2.BoxScorePlayerTrackV2(game_id)
    fg = boxscore.player_stats.get_dict()
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y, c='red')
plt.style.use('classic')
ax = create_court(out_lines=True)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title(""+str(shots[0][4]) + " FGM", y=1.2, fontsize=18)
ax.text(-245, 420, 'Source: stats.nba.com \nCreated by: Tamieem Jaffary', fontsize=12)
ax.set_xlim(-250, 250)
ax.set_ylim(422.5,-47.5)
img = OffsetImage(pic, zoom=.6)
img.set_offset((890,921))
ax.add_artist(img)
plt.show()

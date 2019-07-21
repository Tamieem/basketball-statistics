from nba_api.stats.endpoints import shotchartdetail
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Patch
from matplotlib.offsetbox import OffsetImage
import urllib.request
import sys

## WILL NEED TO Create  dropdown menus for each variable, primarily the first 3 and then the rest can be hidden under an
## "advanced filters" button
def main():
    player_id = "1628995"
    ## Kevin Knox, because he was the player I was originally thinking of when I first started this project...
    # pretty low FG% even for a rookie sheesh
    team_id = "1610612752" ## New York Knicks
    context_measure_simple = 'default'
    last_n_games = '0'
    league_id = '00'
    month = '0'
    opp_team = '0'
    quarter = '0'
    season_type = 'Regular Season'
    ### There are other filters to the search but they are nullable so we don't need to specify their values unless warranted
    player = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team_id,
                                             context_measure_simple=context_measure_simple, last_n_games=last_n_games,
                                             league_id=league_id, month=month, opponent_team_id=opp_team, period=quarter,
                                             season_type_all_star=season_type)
    get_Shotchart(player)


def get_Shotchart(player):
    shots = player.shot_chart_detail.get_dict()['data']
    pic_link = urllib.request.urlretrieve(
        "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+str(shots[0][3])+".png")
    pic = plt.imread(pic_link[0])
    sns.set_style("white")
    sns.set_color_codes()
    plt.figure(figsize=(12,11))
    for shot in shots:
        time = shot[21]
        year = str(time[0:4])
        date_month = str(time[4:6])
        day = str(time[6:])
        date = str('' + date_month+'/'+day+'/'+year)
        if shot[10] == 'Missed Shot':
            plt.scatter(shot[17], shot[18], c='blue', label=""+shot[11]+" vs "+shot[23] + " on " + date)
        else:
            plt.scatter(shot[17], shot[18], c='red', label=""+shot[11]+" vs "+shot[23] + " on " + date)
    plt.style.use('classic')
    ax = create_court(out_lines=True)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(""+str(shots[0][4]) + " FGA", y=1.2, fontsize=22)
    ax.text(-100, -50, '2018-2019 ' + player.parameters['SeasonType']+': ' + str(len(shots)) + ' total shots',
            fontsize=18)
    ax.text(-245, 420, 'Source: stats.nba.com \nCreated by: Tamieem Jaffary', fontsize=14)
    missed = Patch(color='blue', label='Missed Shot')
    made = Patch(color='red', label = "Made Shot")
    plt.legend(handles=[missed,made], loc='lower right')
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5,-47.5)
    plt.axis('off')
    ax.set_facecolor('#EEEEEE')
    img = OffsetImage(pic, zoom=.6)
    img.set_offset((890,921))
    ax.add_artist(img)
    plt.show()


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
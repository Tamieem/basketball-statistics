from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo, playergamelogs
from datetime import datetime
import calendar
from nba_api.stats.static import players, teams
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Patch
from matplotlib.offsetbox import OffsetImage
import urllib.request

from create_court import create_court


def get_shotchart(player, player_id):
    shots = player.shot_chart_detail.get_dict()['data']
    pic_link = urllib.request.urlretrieve(
        "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + str(player_id) + ".png")
    plt.figure(figsize=(15, 13))
    made_count = 0
    for shot in shots:
        time = shot[21]
        year = str(time[0:4])
        date_month = str(time[4:6])
        day = str(time[6:])
        date = str('' + date_month + '/' + day + '/' + year)
        if shot[10] == 'Missed Shot':
            plt.scatter(shot[17], shot[18], c='blue', label="" + shot[11] + " vs " + shot[23] + " on " + date)
        else:
            made_count += 1
            plt.scatter(shot[17], shot[18], c='red', label="" + shot[11] + " vs " + shot[23] + " on " + date)
    plt.style.use('classic')
    ax = create_court(out_lines=True)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title("" + str(shots[0][4]) + " FGA", y=1.2, fontsize=22)  # Takes 'Player's name' + 'FGA'
    fg = round((made_count / len(shots) * 100), 2)

    ax.text(-75, -70, '' + shots[0][4] + ' ' + player.parameters['ContextMeasure'], fontsize=22)
    ax.text(-225, -50, '' + text_builder(player.parameters) + ': ' + str(len(shots)) + ' total shots, ' +
            str(fg) + '% FG', fontsize=12)
    ax.text(-245, 420, 'Source: stats.nba.com \nCreated by Tamieem Jaffary', fontsize=14)
    missed = Patch(color='blue', label='Missed Shot')
    made = Patch(color='red', label="Made Shot")
    plt.legend(handles=[missed, made], loc='lower right')
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)
    plt.axis('off')
    ax.set_facecolor('#EEEEEE')
    pic = plt.imread(pic_link[0])
    img = OffsetImage(pic, zoom=.8)
    img.set_offset((15, 150))


def text_builder(parameters):
    text = ''
    if parameters['Season'] is None:
        current_season = datetime.now()
        current_year = current_season.year
        if current_season.month <= 9:
            current_year -= 1
        season = '{}-{}'.format(current_year, str(current_year + 1)[2:])
    else:
        season = parameters['Season']
    text += season
    season_type = parameters['SeasonType']
    text += ' ' + season_type + ' shots'
    if parameters['ClutchTime'] != ' ':
        clutch = ' in the ' + parameters['ClutchTime']
        text += clutch
    if parameters['Period'] != '0':
        period = ' of the'
        if parameters['Period'] == '1':
            period += ' 1st quarter'
        elif parameters['Period'] == '2':
            period += ' 2nd quarter'
        elif parameters['Period'] == '3':
            period += ' 3rd quarter'
        elif parameters['Period'] == '4':
            period += ' 4th quarter'
        text += period
    if parameters['AheadBehind'] != ' ':
        ahead_behind = ' while ' + parameters['AheadBehind']
        text += ahead_behind
    if parameters['Outcome'] != ' ':
        if parameters['Outcome'] == 'W':
            outcome = ' in a game win'
        else:
            outcome = ' in a game loss'
        text += outcome
    if parameters['LastNGames'] != '0':
        games = ' for the last ' + parameters['LastNGames'] + ' games'
        text += games
    if parameters['Month'] != '0':
        month = ' in the month of ' + calendar.month_name[int(parameters['Month'])]
        text += month
    if parameters['OpponentTeamID'] != '0':
        team = teams.find_team_name_by_id(parameters['OpponentTeamID'])
        oppteam = ' versus ' + team['abbreviation']
        text += oppteam
    return text

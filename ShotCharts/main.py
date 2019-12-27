from flask import *
import os
import random
from datetime import datetime
import calendar
from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo, playergamelogs
from nba_api.stats.static import players, teams
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Patch
from matplotlib.offsetbox import OffsetImage
import urllib.request
import io
import base64
import PIL


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    text+= ' ' + season_type + ' shots'
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
        text +=games
    if parameters['Month'] != '0':
        month = ' in the month of ' + calendar.month_name[int(parameters['Month'])]
        text += month
    if parameters['OpponentTeamID'] != '0':
        team = teams.find_team_name_by_id(parameters['OpponentTeamID'])
        oppteam = ' versus ' + team['abbreviation']
        text += oppteam
    return text


def get_Shotchart(player, player_id):
    shots = player.shot_chart_detail.get_dict()['data']
    pic_link = urllib.request.urlretrieve(
        "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+str(player_id)+".png")
    plt.figure(figsize=(15, 13))
    made_count=0
    for shot in shots:
        time = shot[21]
        year = str(time[0:4])
        date_month = str(time[4:6])
        day = str(time[6:])
        date = str('' + date_month+'/'+day+'/'+year)
        if shot[10] == 'Missed Shot':
            plt.scatter(shot[17], shot[18], c='blue', label=""+shot[11]+" vs "+shot[23] + " on " + date)
        else:
            made_count +=1
            plt.scatter(shot[17], shot[18], c='red', label=""+shot[11]+" vs "+shot[23] + " on " + date)
    plt.style.use('classic')
    ax = create_court(out_lines=True)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(""+str(shots[0][4]) + " FGA", y=1.2, fontsize=22) #Takes 'Player's name' + 'FGA'
    fg = round((made_count/len(shots)*100), 2)

    ax.text(-75, -70, '' + shots[0][4] + ' ' + player.parameters['ContextMeasure'], fontsize=22)
    ax.text(-225, -50, ''+ text_builder(player.parameters) + ': ' + str(len(shots)) + ' total shots, ' +
            str(fg) + '% FG', fontsize=12)
    ax.text(-245, 420, 'Source: stats.nba.com \nCreated by Tamieem Jaffary', fontsize=14)
    missed = Patch(color='blue', label='Missed Shot')
    made = Patch(color='red', label = "Made Shot")
    plt.legend(handles=[missed,made], loc='lower right')
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5,-47.5)
    plt.axis('off')
    ax.set_facecolor('#EEEEEE')
    pic = plt.imread(pic_link[0])
    img = OffsetImage(pic, zoom=.8)
    img.set_offset((15,150))


@app.route("/", methods=['GET', 'POST'])
def home():
    ax = create_court()
    player_id = 2544

    if request.method== 'POST':
        player_id = 1628995
        ## Kevin Knox, because he was the player I was originally thinking of when I first started this project...
        # pretty low FG% even for a rookie sheesh
        team_id = 1610612752  ## New York Knicks
        context_measure_simple = 'FGA'
        last_n_games = '0'
        league_id = '00'
        month = '0'
        opp_team_id = 0
        period = '0'
        season_type = 'Regular Season'
        ### There are other filters to the search but they are nullable so we don't need to specify their values unless warranted
        player_id = request.form['player']
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()['resultSets'][0]['rowSet']
        #sleep(2)
        season = request.form['Season']
        team_id = player_info[0][16]
        ## Team ID is not accurate for previous seasons if player has been traded
        raw_data = playergamelogs.PlayerGameLogs(player_id_nullable=player_id, get_request=False)
        raw_data.parameters['Season'] = season
        raw_data.get_request()
        data_sets = raw_data.data_sets
        team_id = data_sets[0].get_dict()['data'][0][3]
        ### Gets Team ID of player at the start of the requested season ###

        context_measure_simple = request.form['ContextMeasure']
        season_type = request.form['SeasonType']
        clutch_time_nullable = request.form['ClutchTime']
        outcome_nullable = request.form['Outcome']
        ahead_behind_nullable = request.form['While']
        last_n_games = request.form['LastNGames']
        period = request.form['Period']
        month = request.form['Month']
        opp_team_id = request.form['OppTeam']

        player = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team_id,
                                                 context_measure_simple=context_measure_simple,
                                                 last_n_games=last_n_games, league_id=league_id, month=month,
                                                 opponent_team_id=opp_team_id, period=period,
                                                 clutch_time_nullable=clutch_time_nullable,
                                                 outcome_nullable=outcome_nullable,
                                                 ahead_behind_nullable=ahead_behind_nullable,
                                                 season_type_all_star=season_type,
                                                 season_nullable=season)
        get_Shotchart(player, player_id)
    players_list = players.get_active_players()
    team_list = teams.get_teams()
    seasons = ['1998-1999',
               '1999-2000',
               '2000-2001',
               '2001-2002',
               '2002-2003',
               '2003-2004',
               '2004-2005',
               '2005-2006',
               '2006-2007',
               '2007-2008',
               '2008-2009',
               '2009-2010',
               '2010-2011',
               '2011-2012',
               '2012-2013',
               '2013-2014',
               '2014-2015',
               '2015-2016',
               '2016-2017',
               '2017-2018',
               '2018-2019',
               '2019-2020']
    context_measure = ['PTS', 'FG_PCT', 'FG3_PCT', 'PTS_FB',
                       'PTS_OFF_TOV', 'PTS_2ND_CHANCE',  'FG3M', 'FG3A', 'FGM', 'FGA']
    season_type = [ 'All Star', 'Playoffs', 'Pre Season', 'Regular Season']
    clutch_time = ['Last 5 Minutes', 'Last 4 Minutes', 'Last 3 Minutes', 'Last 2 Minutes', 'Last 1 Minute',
                    'Last 30 Seconds', 'Last 10 Seconds']
    outcome = ['W', 'L']
    ahead_behind=['Ahead or Behind', 'Ahead or Tied', 'Behind or Tied']
    period = ['1','2','3','4']
    month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    last_n_games = [str(x) for x in range(1,26)]
    params = [context_measure, season_type, clutch_time, outcome, ahead_behind, period, month, last_n_games]
    img = io.BytesIO()
    # plt.xlim(-300, 300)
    # plt.ylim(422.5,-47.5)
    plt.tick_params(labelbottom=False, labelleft=False)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('home.html', teams_list=team_list, players_list=players_list, seasons=seasons, params=params, plot_url=plot_url)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
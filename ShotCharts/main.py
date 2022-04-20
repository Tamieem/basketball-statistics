from flask import *
from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo, playergamelogs
from nba_api.stats.static import players, teams
import matplotlib.pyplot as plt
import io
import base64

from create_shotchart import get_shotchart

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
def home():
    player_id = 2544

    if request.method == 'POST':
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
        season = request.form['Season']
        team_id = player_info[0][18]
        ## Team ID is not accurate for previous seasons if player has been traded
        raw_data = playergamelogs.PlayerGameLogs(player_id_nullable=player_id, get_request=False)
        raw_data.parameters['Season'] = season
        raw_data.get_request()
        data_sets = raw_data.data_sets
        team_id = data_sets[0].get_dict()['data'][0][4]
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
        get_shotchart(player, player_id)
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
    params = get_params()
    img = io.BytesIO()
    plt.tick_params(labelbottom=False, labelleft=False)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('home.html', teams_list=team_list, players_list=players_list, seasons=seasons, params=params,
                           plot_url=plot_url)


def get_params():
    context_measure = ['PTS', 'FG_PCT', 'FG3_PCT', 'PTS_FB',
                       'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'FG3M', 'FG3A', 'FGM', 'FGA']
    season_type = ['All Star', 'Playoffs', 'Pre Season', 'Regular Season']
    clutch_time = ['Last 5 Minutes', 'Last 4 Minutes', 'Last 3 Minutes', 'Last 2 Minutes', 'Last 1 Minute',
                   'Last 30 Seconds', 'Last 10 Seconds']
    outcome = ['W', 'L']
    ahead_behind = ['Ahead or Behind', 'Ahead or Tied', 'Behind or Tied']
    period = ['1', '2', '3', '4']
    month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    last_n_games = [str(x) for x in range(1, 26)]
    return [context_measure, season_type, clutch_time, outcome, ahead_behind, period, month, last_n_games]


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()

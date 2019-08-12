from flask import *
import os
import random
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Patch
from matplotlib.offsetbox import OffsetImage
import io
import base64

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



@app.route("/", methods=['GET', 'POST'])
def home():
    ax = create_court()
    players_list = players.get_active_players()
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
               '2018-2019']
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
    plt.xlim(-300, 300)
    plt.ylim(422.5,-47.5)
    plt.tick_params(labelbottom=False, labelleft=False)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('home.html', players_list=players_list, seasons=seasons, params=params, plot_url=plot_url)


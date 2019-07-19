from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playbyplayv2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.offsetbox import OffsetImage


def get_games(game_id):
### Important Columns to note:  [4]=Quarter [6]=time left in quarter [10]= current score [11]= score margin (home team is postive)

    gameplay = playbyplayv2.PlayByPlayV2(game_id)
    gameplay.play_by_play.get_dict() ## [10] holds score, [11] holds score margin

    play_by_plays = []
    for link_set in link_sets:
        for link in link_set:
            href = link.get("href")
            if "playbyplay" in href:
                play_by_plays.append(href)

    return play_by_plays


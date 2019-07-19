from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playbyplayv2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

player = shotchartdetail.ShotChartDetail(player_id=1628995, team_id=1610612752)
headers = player.shot_chart_detail.get_dict()['headers']
shots = player.shot_chart_detail.get_dict()['data']
shot_df = pd.DataFrame(shots, columns=headers)
sns.set_style("white")
sns.set_color_codes()
plt.figure(figsize=(12,11))
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
plt.show()
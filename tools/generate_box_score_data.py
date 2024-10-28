# -*- coding: utf-8 -*-
"""
Created by Guilherme Theis

Current version = 0.0.01
"""


#Import
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.static import players
import pandas as pd
import matplotlib.pyplot as plt

player_name = "Jayson Tatum"
player_info = players.find_players_by_full_name(player_name)

if player_info:
    tatum_id = player_info[0]['id']
else:
    raise ValueError(f"Player {player_name} not found")

game_logs = playergamelogs.PlayerGameLogs(
    season_nullable='2023-24',  # Season 2023-24
    player_id_nullable=tatum_id,
    season_type_nullable='Regular Season'  # Regular Season filter
)

#df gen
game_logs_df = game_logs.get_data_frames()[0]

#filtering
game_logs_df['GAME_DATE'] = pd.to_datetime(game_logs_df['GAME_DATE'])
game_logs_df = game_logs_df[['GAME_DATE', 'PTS']]  # Use points and game date

#sort date
game_logs_df = game_logs_df.sort_values(by='GAME_DATE').reset_index(drop=True)

#get games
game_logs_df['Game_Number'] = range(1, len(game_logs_df) + 1)

#Generate Months
game_logs_df['Month'] = game_logs_df['GAME_DATE'].dt.strftime("%b '%y")

#PPG calc
game_logs_df['PPG'] = game_logs_df['PTS'].cumsum() / (game_logs_df.index + 1)

#Plot
plt.figure()

# Plot Points (PTS) as a bar plot
plt.bar(game_logs_df['GAME_DATE'], game_logs_df['PTS'], color='lightblue', label='PTS')

# Plot PPG as a line plot
plt.plot(game_logs_df['GAME_DATE'], game_logs_df['PPG'], color='red', marker='o', label='PPG')

# Set labels and title
plt.xlabel('Month', fontsize=12)
plt.ylabel('Points', fontsize=12)
plt.title('Jayson Tatum - PTS and PPG (2023-24 Season)', fontsize=14)

# Customize X-axis with only 7 ticks for the months Oct-Apr
plt.xticks(pd.to_datetime(['2023-10-01', '2023-11-01', '2023-12-01', '2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']),
           ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'], rotation=45)

# Add legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()

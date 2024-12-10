"""
File: models.py
Author: Mark Maci, markmaci@bu.edu, 12/10/2024
Description: Utility functions to assist in player data retrieval from the NBA API and related sources.
These functions do not directly render views but provide helper logic, such as fetching
a player's name and headshot image.
"""

from nba_api.stats.endpoints import commonplayerinfo
import requests
from bs4 import BeautifulSoup

def get_player_name_and_image(player_id):
    """
    Retrieve a player's display name and headshot URL using their NBA player_id.

    Args:
        player_id (int): The unique NBA player ID.

    Returns:
        (str, str): A tuple containing the player's display name and headshot image URL.
                    If no headshot is found, a placeholder image URL is returned.
    """
    # Fetch general player info from the NBA API
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
    data = info['resultSets'][0]['rowSet'][0]

    # The name at index 3 is DISPLAY_FIRST_LAST (e.g., "LeBron James")
    player_name = data[3]

    # Attempt to retrieve the player's headshot from nba.com
    url = f'https://www.nba.com/player/{player_id}'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    player_image_div = soup.find('div', {'class': 'PlayerSummary_mainInnerTeam____nFZ'})
    head_shot_url = "https://via.placeholder.com/150"  # fallback if image not found

    if player_image_div:
        img_tag = player_image_div.find('img', {'class': 'PlayerImage_image__wH_YX PlayerSummary_playerImage__sysif'})
        if img_tag:
            head_shot_url = img_tag['src']

    return player_name, head_shot_url

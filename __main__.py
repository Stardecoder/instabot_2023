"""
Created on Sat Feb 11 19:52:52 2023

@author: StarDecoder
"""

from utils_functions import read_params, connect_to_my_ig_account, map_hashtags_with_medias, collapse_hashtags_media_dict 
from auto_browsing import generate_daily_session_params,  basic_daily_auto_browsing
from stalking_functions import download_medias
import logging
logging.basicConfig(level = logging.INFO)

my_log = logging.getLogger("instabot_2023")


PARAMS_FILENAME = "params.yaml"
params = read_params(PARAMS_FILENAME)


cl = connect_to_my_ig_account(params)

if cl is not None:

    #GENERATE DAILY PARAMS F
    hashtags_to_explore, current_day, nbr_likes, nbr_comments = generate_daily_session_params(params)
    
    #MAP HASHTAG/MEDIAS TO INTERACT WITH
    hashtags_medias_dict = map_hashtags_with_medias(cl, hashtags_to_explore, params,  recent = False)
    
    medias = collapse_hashtags_media_dict(hashtags_medias_dict) 
    
    download_medias(cl, medias, store_at = "data_instabot_2023")

    #RUN DAILY AUTO BROWSING
    basic_daily_auto_browsing(current_day, cl, hashtags_medias_dict, nbr_likes, params)
    
    my_log.info("your daily session is done")
else:
    my_log.error("Sorry bra, we could not connect you to IG")
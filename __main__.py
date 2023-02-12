"""
Created on Sat Feb 11 19:52:52 2023

@author: StarDecoder
"""
from instagrapi import Client
from utils_functions import read_params, map_hashtags_with_medias 
from auto_browsing import generate_daily_session_params,  basic_daily_auto_browsing


PARAMS_FILENAME = "params.yaml"
params = read_params(PARAMS_FILENAME)


#CONNECT TO YOUR PERSONNAL INSTAGRAM ACOUNT
cl = Client()
cl.login(params['username'], params['password'])


#GENERATE DAILY PARAMS F
hashtags_to_explore, current_day, nbr_likes, nbr_comments = generate_daily_session_params(params)

#MAP HASHTAG/MEDIAS TO INTERACT WITH
hashtags_medias_dict = map_hashtags_with_medias(cl, hashtags_to_explore, params)



#RUN DAILY AUTO BROWSING
basic_daily_auto_browsing(current_day, cl, hashtags_medias_dict, nbr_likes, params)
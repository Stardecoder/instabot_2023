# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 19:52:52 2023

@author: StarDecoder
"""

import yaml
from yaml.loader import SafeLoader
import os
import logging
logging.basicConfig(level = logging.INFO)
from instagrapi import Client


my_logger = logging.getLogger("instabot_2023")


def read_params(params_filepath):
    params = None
    try:
        with open(params_filepath) as f:
            params = yaml.load(f, Loader=SafeLoader)
            
    except Exception as e:
        print(e)
        
    return params



def connect_to_my_ig_account(params):
    session_path = os.path.join("data_instabot_2023","connexion_settings.json")
    cl = Client()
    try:
        if os.path.exists(session_path):
            my_logger.info("found session file at " + session_path + " it will be loaded")
            cl.load_settings(session_path)

        #CONNECT TO YOUR PERSONNAL INSTAGRAM ACOUNT 
        my_logger.info("logging to " + params['username'] + " ...")
        if params['verification_code'] == "":
            cl.login(params['username'], params['password'])
        else:
            cl.login(params['username'], params['password'], verification_code = params['verification_code'])
            
        #/!\ seems to trigger more LoginRequired Exceptions 
        #keep connection params for future connections
        #if not os.path.exists(session_path):
        #    cl.dump_settings(session_path)
            
        my_logger.info("logged in!")
        return cl
    except Exception as e:
        my_logger.exception(e)
        return None
                
def collapse_hashtags_media_dict(hashtags_medias_dict):
    medias = []
    for k in hashtags_medias_dict.keys():
        medias.extend(hashtags_medias_dict[k])
    return medias


def map_hashtags_with_medias(client, hashtags_to_explore, params, recent = True):
    hashtags_medias_dict = dict()
    

    for h in hashtags_to_explore:
        my_logger.info('\n #mapping medias for hashtag ' + h + '...\n')
        try:
            if recent:
                hashtags_medias_dict[h] = client.hashtag_medias_recent(h, amount = params['max_posts_per_hashtag'][0])
            else:
                hashtags_medias_dict[h] = client.hashtag_medias_top(h, amount = params['max_posts_per_hashtag'][0])
        except Exception as e:
            my_logger.exception(e)
        
    return hashtags_medias_dict





"""
Client key methods
    media_like
    media_comment
    comment_like
    
    search_users
    search_hashtags

"""

"""
Media key attributes:
    comment_count
    like_count
    view_count
    caption_text
    id

"""

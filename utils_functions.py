# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 19:52:52 2023

@author: Nedjmeddine
"""

import yaml
from yaml.loader import SafeLoader


def read_params(params_filepath):
    params = None
    try:
        with open(params_filepath) as f:
            params = yaml.load(f, Loader=SafeLoader)
            
    except Exception as e:
        print(e)
        
    return params


def map_hashtags_with_medias(client, hashtags_to_explore, params):
    hashtags_medias_dict = dict()
    

    for h in hashtags_to_explore:
        print('mapping medias for hashtag ', h, '...')
        try:
            hashtags_medias_dict[h] = client.hashtag_medias_recent(h, amount = params['max_posts_per_hashtag'][0])
        except Exception as e:
            print(e)
        
    return hashtags_medias_dict

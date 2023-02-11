"""
Created on Sat Feb 11 19:52:52 2023

@author: Nedjmeddine
"""
import time
from datetime import datetime
from instagrapi import Client
import numpy as np 
import yaml
from utils_functions import read_params


PARAMS_FILENAME = "params.yaml"
params = read_params(PARAMS_FILENAME)


cl = Client()
cl.login(params['username'], params['password'])

hashtags_to_explore = params['hashtags'] 

for h in hashtags_to_explore:
    



user_id = cl.user_id_from_username("lahoubi_prod")
medias = cl.user_medias(user_id, 100)

for m in medias:
    print(m.caption_text)

cl.media_like('media_id')
cl.media_comment(m.id, 'excellent work :)')


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
top_medias = cl.hashtag_medias_top("paris", amount = 20)


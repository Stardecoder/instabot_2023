"""
Created on Sat Feb 11 19:52:52 2023

@author: Nedjmeddine
"""
import time
from datetime import datetime
from instagrapi import Client
import numpy as np 
import yaml
from utils_functions import read_params, map_hashtags_with_medias


PARAMS_FILENAME = "params.yaml"
params = read_params(PARAMS_FILENAME)

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

cl = Client()
cl.login(params['username'], params['password'])

hashtags_to_explore = params['hashtags'] 


current_day = datetime.now().day
nbr_likes = np.random.choice(np.arange(params['min_max_likes_per_day'][0],
                                       params['min_max_likes_per_day'][1]),
                             1)[0]

nbr_comments = np.random.choice(np.arange(params['min_max_comments_per_day'][0],
                                       params['min_max_comments_per_day'][1]),
                             1)[0]


hashtags_medias_dict = map_hashtags_with_medias(cl, hashtags_to_explore, params)

while (nbr_likes > 0) or (nbr_comments > 0) or (current_day != datetime.now().day):
    

    h = np.random.choice(hashtags_to_explore, 1)[0]
    posts_h = cl.hashtag_medias_recent(h, amount = params['max_posts_per_hashtag'])
    



user_id = cl.user_id_from_username("lahoubi_prod")
medias = cl.user_medias(user_id, 100)

for m in medias:
    print(m.caption_text)

cl.media_like('media_id')
cl.media_comment(m.id, 'excellent work :)')



top_medias = cl.hashtag_medias_top("paris", amount = 20)


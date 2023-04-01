"""
Created on Sun Feb 12 11:18:59 2023

@author: Nedjmeddine
"""
from datetime import datetime
import numpy as np
import time 
import logging
logging.basicConfig(level = logging.INFO)
my_log = logging.getLogger("instabot_2023")

def pick_hashtag_media_from(hashtags_medias_dict):
    h = np.random.choice(list(hashtags_medias_dict.keys()),1)[0]
    
    m_idx = np.random.choice(np.arange(0,len(hashtags_medias_dict[h])),1)[0]
    m = hashtags_medias_dict[h][m_idx]
    del hashtags_medias_dict[h][m_idx] 
    
    return h, m, hashtags_medias_dict  


def generate_patience_time_between_likes(params):
    return np.random.randint(params['min_max_time_between_two_likes'][0], params['min_max_time_between_two_likes'][1])

def generate_patience_time_between_post_downloads(params):
    return np.random.randint(params['min_max_time_between_two_post_downloads'][0], params['min_max_time_between_two_post_downloads'][1])


def generate_daily_session_params(params):

    hashtags_to_explore = params['hashtags'] 
    
    
    current_day = datetime.now().day
    nbr_likes = np.random.choice(np.arange(params['min_max_likes_per_day'][0],
                                           params['min_max_likes_per_day'][1]),
                                 1)[0]
    
    nbr_comments = np.random.choice(np.arange(params['min_max_comments_per_day'][0],
                                           params['min_max_comments_per_day'][1]),
                                 1)[0]
    
    return hashtags_to_explore, current_day, nbr_likes, nbr_comments


def wait_for_next_like(params):
    patience = generate_patience_time_between_likes(params) 
    my_log.info('Next like in ' + str(patience) +  ' seconds thanks for waiting :) ...')
    time.sleep(patience)
 
    
def wait_for_next_post_download(params):
    patience = generate_patience_time_between_post_downloads(params) 
    my_log.info('Next Post Download in ' + str(patience) + ' seconds thanks for waiting :) ...')
    time.sleep(patience)
     

def basic_daily_auto_browsing(current_day, cl, hashtags_medias_dict, nbr_likes, params):


    while current_day == datetime.now().day:
        try:
            h, m, hashtags_medias_dict  = pick_hashtag_media_from(hashtags_medias_dict)
           
            if nbr_likes > 0:
                print('about to throw a like at media with hashtag ', h)
                cl.media_like(m.id)
                
                wait_for_next_like(params)
                
                nbr_likes = nbr_likes - 1
                
            if nbr_likes <= 0:
                print('max nbr of daily likes reached, see you tomorrow bra')
                break
        except Exception as e:
            print('OUPS SOMETHING WENT WRONG \n', e)

            

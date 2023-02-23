# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 20:17:45 2023

@author: StarDecoder
"""
from datetime import datetime
import os
import json
import logging
logging.basicConfig(level = logging.INFO)

my_log = logging.getLogger("instabot_2023")

MAX_FOLLOWERS = 2000
MAX_FOLLOWINGS = 1000
MAX_POSTS_PER_PROFILE = 200

def download_medias(cl, medias, store_at = "data_instabot_2023"):
    #Photos
    for m in medias:
        if m.media_type == 1:
            cl.photo_download(m.pk, store_at)


def stalk_profile(cl, username, data_folder = "data_instabot_2023", followers = False, followings = False):
    '''
    for given username the function creates local folder with:
         - profile picture
         - json file containing relevant informations (name, bio, is_private, follower_ids, following_ids,....)
    '''
    
    stalked_profile = dict()
    my_log.info("stalking " + username + "...")
    try:
        user_info = cl.user_info_by_username(username).dict()
        stalked_profile = user_info
        user_id = user_info['pk']
        profile_dir = os.path.join(data_folder, "profiles", user_info['username'])
        profile_pic_path = os.path.join(profile_dir, user_info['username'] + "_profile_pic_" + str(datetime.now()).replace(':','-').replace('.','-'))
     
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)      
        my_log.info("downloading profile pic...")
        cl.photo_download_by_url(user_info['profile_pic_url_hd'], profile_pic_path)
        
        if followers:
            my_log.info("looking for followers...")
            followers = cl.user_followers(user_id, amount = MAX_FOLLOWERS)
            stalked_profile['follower'] = list(followers.keys())
        
        if followings:
            my_log.info("looking for followings...")
            followings = cl.user_following(user_id, amount = MAX_FOLLOWINGS)
            stalked_profile['following'] = list(followings.keys())
            
        
        json_path = os.path.join(profile_dir,'profile_infos.json')
        my_log.info("writing stalked profile infos on json file stored at: " + json_path)
        with open(json_path, 'w') as f:
            json.dump(stalked_profile, f)
    except Exception as e:
        my_log.exception(e)


def get_id_from_username(cl, username):
    try:
        return cl.user_info_by_username(username).dict()['pk']
    except Exception as e:
        my_log.exception(e)
        return None



def get_media_type(m):
    if m.media_type == 1:
        return "photo"
    if m.media_type == 1 and m.product_type == "feed":
        return "video"
    if m.media_type == 2 and m.product_type == "igtv":
        return "igtv"
    if m.media_type == 2 and m.product_type == "clips":
        return "reel"
    if m.media_type == 8: 
        return "album"
    
    
def list_posts_of_profile(cl, username, max_nbr_posts = MAX_POSTS_PER_PROFILE):        

    posts = dict()
    try:
        user_id = cl.user_info_by_username(username).dict()['pk']
        
        medias = cl.user_medias(user_id, amount = MAX_POSTS_PER_PROFILE)
        
        
        for m in medias:
        
            m_dict = m.dict()
            m_dict['post_type'] = get_media_type(m)
            posts[m.id] = m_dict
    except Exception as e:
        my_log.exception(e)
    
    return posts




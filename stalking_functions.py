"""
Created on Thu Feb 16 20:17:45 2023

@author: StarDecoder
"""
import instagrapi
from auto_browsing import wait_for_next_post_download 
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


def get_followers(cl, user_id, max_follows = MAX_FOLLOWERS):
    followers = []
    
    try:
        followers = cl.user_followers_v1(user_id, amount = MAX_FOLLOWERS)
    except instagrapi.exceptions.LoginRequired:
        followers = cl.user_followers_v1(user_id, amount = MAX_FOLLOWERS)
    except Exception as e:
        my_log.error("\n\n\n We couldn't get the list of followers ://....\n\n\n")
        my_log.exception(e)
        my_log.info("\n\n\n")
    return followers
        

def get_followings(cl, user_id, max_follows = MAX_FOLLOWERS):
    followings = []
    
    try:
        followings = cl.user_following_v1(user_id, amount = MAX_FOLLOWERS)
    except instagrapi.exceptions.LoginRequired:
        followings = cl.user_following_v1(user_id, amount = MAX_FOLLOWERS)
    except Exception as e:
        my_log.error("\n\n\n We couldn't get the list of followers ://....\n\n\n")
        my_log.exception(e)
        my_log.info("\n\n\n")
    return followings
        

def extract_user_infos(list_of_users):
    list_of_users_infos = []
    if len(list_of_users)>0:
        list_of_users_infos = [{'pk':u.pk, 'username' :u.username, 'full_name': u.full_name} for u in list_of_users]
    return list_of_users_infos

def stalk_profile(cl, username, data_folder = "data_instabot_2023", followers = False, followings = False):
    '''
    for given username the function creates local folder with:
         - profile picture
         - json file containing relevant informations (name, bio, is_private, follower_ids, following_ids,....)
    '''
    
    stalked_profile = dict()
    my_log.info("stalking " + username + "...")
    profile_dir = os.path.join(data_folder, "profiles", username)
    json_path = os.path.join(profile_dir,'profile_infos.json')
    
    try:
        user_info = cl.user_info_by_username(username).dict()
        stalked_profile = user_info
        user_id = user_info['pk']
        
        profile_pic_path = os.path.join(profile_dir, user_info['username'] + "_profile_pic_" + str(datetime.now()).replace(':','-').replace('.','-'))
     
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)      
        my_log.info("downloading profile pic...")
        cl.photo_download_by_url(user_info['profile_pic_url_hd'], profile_pic_path)
        
        if followers:
            my_log.info("\n\n\nlooking for followers...\n\n\n")
            followers = get_followers(cl, user_id, max_follows = MAX_FOLLOWERS)
            stalked_profile['followers'] = extract_user_infos(followers)
        
        if followings:
            my_log.info("\n\n\nlooking for followings...\n\n\n")
            followings = get_followings(cl, user_id, max_follows = MAX_FOLLOWINGS)
            stalked_profile['followings'] = extract_user_infos(followings)
            
        
        my_log.info("writing stalked profile infos on json file stored at: " + json_path)
        with open(json_path, 'w') as f:
            json.dump(stalked_profile, f)
        return stalked_profile
    
    except Exception as e:
        my_log.exception(e)
        with open(json_path, 'w') as f:
            json.dump(stalked_profile, f)
        return stalked_profile


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
        user_id = get_id_from_username(cl, username)
    
        medias = cl.user_medias_v1(user_id, amount = MAX_POSTS_PER_PROFILE)
        
        
        for m in medias:
        
            m_dict = m.dict()
            m_dict['post_type'] = get_media_type(m)
            posts[m.id] = m_dict
    except Exception as e:
        my_log.exception(e)
    
    return posts


def download_posts(posts, cl, username, params, folder = ""):
    '''
    download list of posts fetched by function list_posts_of_profile
    handles only photos and videos
    '''
    if folder == "":
        folder = os.path.join("data_instabot_2023", "profiles", username)
    
    for k in posts.keys():
        p = posts[k]
        try:
            if p['post_type'] == "photo":
                cl.photo_download(p['pk'], folder = folder)
                my_log.info("post photo downloaded at " +  folder)
            elif p['post_type'] =="video":
                cl.video_download(p['pk'], folder = folder)
                my_log.info("video photo downloaded at " +  folder)
            elif p['post_type'] =="album":
                cl.album_download(p['pk'], folder = folder)
                my_log.info("post album downloaded at " +  folder)
        except instagrapi.exceptions.LoginRequired:
            my_log.error("\n\n\n oups we got caught by Instagram it's better to stop mate \n\n\n")
            return 
        except Exception as e:
            my_log.exception(e)
        
        wait_for_next_post_download(params)
            


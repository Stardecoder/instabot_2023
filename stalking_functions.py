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


def download_medias(cl, medias, store_at = "data_instabot_2023"):
    #Photos
    for m in medias:
        if m.media_type == 1:
            cl.photo_download(m.pk, store_at)


def stalk_profile(cl, username, data_folder = "data_instabot_2023"):
    '''
    for given username the function creates local folder with profile picture
    and relevant informations (name, bio, is_private,....) in json file named profile_infos.json
    '''
    try:
        user_info = cl.user_info_by_username(username).dict()
     
        profile_dir = os.path.join(data_folder, "profiles", user_info['username'])
        profile_pic_path = os.path.join(profile_dir, user_info['username'] + "_profile_pic_" + str(datetime.now()).replace(':','-').replace('.','-'))
     
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)      
            
        cl.photo_download_by_url(user_info['profile_pic_url_hd'], profile_pic_path)
        
        with open(os.path.join(profile_dir,'profile_infos.json'), 'w') as f:
            json.dump(user_info, f)
    except Exception as e:
        my_log.exception(e)









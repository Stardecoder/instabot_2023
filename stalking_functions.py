# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 20:17:45 2023

@author: StarDecoder
"""


from utils_functions import read_params, connect_to_my_ig_account, map_hashtags_with_medias, collapse_hashtags_media_dict 
from auto_browsing import generate_daily_session_params,  basic_daily_auto_browsing

import logging
logging.basicConfig(level = logging.INFO)

my_log = logging.getLogger("instabot_2023")


PARAMS_FILENAME = "params.yaml"
params = read_params(PARAMS_FILENAME)


cl = connect_to_my_ig_account(params)


#user_info = cl.user_id_from_username("avicii")

#cl.user_info_by_username('adw0rd').dict()


def download_medias(cl, medias, store_at = "data_instabot_2023"):
    #Photos
    for m in medias:
        if m.media_type == 1:
            cl.photo_download(m.pk, store_at)

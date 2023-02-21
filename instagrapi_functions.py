# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 09:00:40 2023

@author: StarDecoder

* List the most important functionalities of INSTAGRAPI
"""

from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)
cl.dump_settings('data_instabot_2023/connexion_settings.json')
cl.load_settings('data_instabot_2023/connexion_settings.json')
cl.login(USERNAME, PASSWORD)

h = 'parismodel'
hashtag = cl.hashtag_info(h)
hashtag.dict()
medias = cl.hashtag_medias_top(h)
medias = cl.hashtag_medias_recent(h)

"""
Media types:

    Photo - When media_type=1
    Video - When media_type=2 and product_type=feed
    IGTV - When media_type=2 and product_type=igtv
    Reel - When media_type=2 and product_type=clips
    Album - When media_type=8
"""


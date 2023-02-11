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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 22:43:25 2018

@author: margaux
"""
"""
Peut-on établir un lien entre la densité de médecins par spécialité  et par 
territoire et la pratique du dépassement d'honoraires ? Est-ce  dans les 
territoires où la densité est la plus forte que les médecins  pratiquent 
le moins les dépassement d'honoraires ? Est ce que la densité de certains 
médecins / praticiens est corrélé à la densité de population pour certaines 
classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
import re
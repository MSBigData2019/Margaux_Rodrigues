#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:51:35 2018

@author: margaux
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from queue import Queue
from threading import Thread

def get_main_contrib_crawl(url):
    
    res = requests.get(url)
    html_doc =  res.text
    soup = BeautifulSoup(html_doc, "lxml")
    elt = soup.find("tbody")
    rankings = elt.findAll("th", {'scope' : 'row'})
    
    usernames = [] 
    names = []
    rankings = []
    
    for truc in elt.findAll('tr'):
        user_info = truc.findNext('td').text.split()
        usernames.append(user_info[0])
        if (len(user_info) > 1):
            if len(user_info) > 2:
                username = user_info[1][1:] + ' ' + user_info[2][:-1]
            else:
                username = user_info[1][1:]
        else:
            username = ''
        names.append(username) 
        rankings.append(truc.findNext('th').text[1:])
    
    d = {'Username': usernames, 'Name' : names}
    df = pd.DataFrame(data = d, index = rankings)
    return df
        
def get_total_stars_for_user(user, tk, nbre_repos):
    pages_to_visit = (nbre_repos // 100) + 1
    stars = 0
    for i in range(pages_to_visit):
        url = 'https://api.github.com/users/' + user + '/repos?page='+ str(i) + 'per_page=100'
        head = {'Authorization': 'token {}'.format(tk[0].strip())}
        get_repo = requests.get(url, headers=head)
        repo_dict = json.loads(get_repo.content) #return un dico de repos
        for repo in repo_dict:
            stars += repo['stargazers_count']
    return stars

def get_count_of_repos_for_user(user, tk):
    url = 'https://api.github.com/users/' + user
    head = {'Authorization': 'token {}'.format(tk[0].strip())}
    get_repo = requests.get(url, headers=head)
    user_dict = json.loads(get_repo.content) #return un dico de repos
    repos_count = user_dict['public_repos']
    return repos_count
    
def means_stars_per_user(user, tk):
    repos_count = get_count_of_repos_for_user(user, tk)
    stars = get_total_stars_for_user(user, tk, repos_count)
    if repos_count != 0:
        return [stars, repos_count, stars / repos_count]
    else: return [stars, repos_count, 0] 

def main():
    # Crawling
    url = 'https://gist.github.com/paulmillr/2657075'
    tk_file = '../tk.txt'
    with open (tk_file) as f:
        tk = f.readlines()
    # get_main_contrib_crawl(url)
    # using API
    # objectif récupérer pour les top contributeurs le nombre moyen de stars de leurs repos
    # puis les classer 

    user_list = get_main_contrib_crawl(url) # returns a pd DF with Username
    #stragazers_count
    stars_list = []
    count_list = []
    mean_list = []
    for user in user_list.Username:
        stars_means = means_stars_per_user(user, tk)
        stars_list.append(stars_means[0])
        count_list.append(stars_means[1])
        mean_list.append(stars_means[2])
    
    user_list['Total_stars'] = stars_list
    user_list['Number_repos'] = count_list
    user_list['Mean_stars'] = mean_list
    print(user_list.sort_values(by = 'Mean_stars', ascending = False))
    
if __name__ == '__main__':
    main()

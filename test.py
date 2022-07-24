# coding=utf-8
from bs4 import BeautifulSoup
import pandas as pd
import requests
from random import random
from time import sleep
import csv
import math

def extract(page):
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    url = f'https://fr.indeed.com/jobs?q=data+scientist&limit=50&start={page}'
    r = requests.get(url, header)                                                   #accède à l'url de la page demandée
    soup = BeautifulSoup(r.content, 'html.parser')                                  #récupère le contenu de la page 
    return soup

'''
fonction permettant de retrouver la div dans le code html 
contenant le nombre de page et le nombre de jobs affichés
'''
nb_page = [] 
def nb_pages(soup):
    div = soup.find(id = 'searchCountPages').text.strip()                           #récupération de la div contenant le nombre de page et le nb total de jobs
    nb_page.append(div)                                                             #ajout à la liste 
    return

'''
fonction convertissant les listes en chaînes de caractères 
'''
def listToString(list):                                                             
    str1 = " "                                                                      #séparateur
    return (str1.join(list))                                                        #"joint" tous les mots ayant été séparés par le séparateur


joblist = []                                                                        #liste vide qui va contenir les titres et urls

def transform(soup):
    divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')                   #trouve toutes les "cartes" des jobs 
    for item in divs:                                                               #pour chaque carte
        atag = item.h2.a                                                            
        title = item.find('a').text.strip()                                         #récupère le titre
        job_url = 'https://fr.indeed.com' + atag.get('href')                        #récupère l'url dans le titre

        job = {                                                                     #dictionnaire (titre, url)
        'title': title,
        'url': job_url
        }
        joblist.append(job)                                                         #ajout de chaque (titre,url) à la liste 
    return

def sleep_for_random_interval():                                                    #fonction permettant de mettre un temps d'attente aléatoire
    seconds = random() * 10
    sleep(seconds)

i = 0                                                                               #initialisation du compteur qui va parcourir le nombre de pages
a = extract(0)                                                                      #on stocke dans a le contenu html de la 1ère page afin de récupérer la div du nombre de pages
sleep_for_random_interval() 
print(a)                                                                            #vérifie qu'on affiche bien la page html et qu'on se fait pas bloquer par le captcha
nb_pages(a)                                                                         #permet de stocker dans la liste nb_page la div du nombre de pages
convertedStr = listToString(nb_page)                                                #conversion liste en chaîne de caractères
split_string = convertedStr.split()                                                 #séparation de tous les mots du string dans une liste
page = math.trunc(int(split_string[3])/50)                                          #nombre maximal de pages arrondi à l'entier inférieur 
print(page)
for j in range(0,1000,50):                                                          #boucle parcourant un nombre de page au pif, pris exprès bien plus grand que ce que l'on est censé obtenir
    while i < page :                                                                #tant que i est inférieur au nombre de page, on récupère les infos des pages
        sleep_for_random_interval()                                                 #temps d'attente aléatoire
        print(f'getting page, {j}')
        c = extract(j)                                                              #récupération de l'url de la page
        sleep_for_random_interval() 
        transform(c)                                                                #dans la page, récupération de tous les titres et url 
        i += 1                                                                      #incrémente compteur de la page
        j+=50                                                                       #incrémente compteur start dans l'url de la page afin de ne pas récupérer 2 fois la même page

df = pd.DataFrame(joblist)                                                          #création d'un dataframe contenant la liste
print(df.head())
df.to_csv('indeed_url_dataScientist.csv')                                                         #conversion du dataframe en fichier csv

description = []                                                                    #création d'une liste vide qui va contenir les descriptions des jobs
for url in df.iloc[0:, 1]:                                                          #boucle parcourant la colonne url du fichier jobs.csv 
    print('recovery url : {}'.format(url))
    response = requests.get(url)                                                    #accède à chaque url du dataframe
    try : 
        soup = BeautifulSoup(response.content, 'html.parser')                           #récupère le contenu de chaque url en html
        sleep_for_random_interval()
        divs = soup.find('div', class_ = 'jobsearch-jobDescriptionText').text.strip()   #trouve la description de chaque job 
        description.append(divs)                                                        #ajout à la liste vide
    except :  
        print("exception raised")
df2 = pd.DataFrame(description)                                                     #création d'un nouveau dataframe contenant toutes les descriptions
print(df2.head())
df2.to_csv('indeed_desc_dataScientist.csv')  

#pb : scrape jusqu'à l'url 567 puis pb de captcha
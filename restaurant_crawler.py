'''
Author: Wu Wanqi
'''

#To get the information about restaurants and store in csv file 
#To get the restaurant images
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import re
import cv2 as cv
import numpy as np
import os
import csv
import requests


browser = webdriver.Chrome()
restaurant_names=[]
restaurant_scores=[]
restaurant_price_lunch=[]
restaurant_price_dinner=[]
restaurant_distance=[]
restaurant_tags=[]
restaurant_address=[]
temp_names=[]
temp_scores=[]
temp_checks=[]
temp_lunch=[]
temp_dinner=[]
temp_distance_tag=[]
temp_distance=[]
temp_tags=[]
temp_addresses=[]
temp_src=[]
temp_images=[]
temp_imageNames=[]
downloaded=[]

a=0
b=0

#Dic={}
#Dic['a']='string1'
#Dic['a'].append('string2')
#print(Dic)

for i in range(1,12):
    browser.get('https://tabelog.com/tokyo/C13104/C36271/rstLst/%s/?svd=20190702&svt=1900&svps=2'%(str(i))) 
    stop=i
    time.sleep(5) 
    bs = BeautifulSoup(browser.page_source, "html.parser")
    scores=bs.find_all('span','c-rating__val c-rating__val--strong list-rst__rating-val')
    titles = bs.find_all('a', 'list-rst__rst-name-target cpy-rst-name')
    checkbit=bs.find_all('em','list-rst__rvw-count-num cpy-review-count')
    prices_lunch=bs.find_all('span','c-rating__val list-rst__budget-val cpy-lunch-budget-val')
    prices_dinner=bs.find_all('span','c-rating__val list-rst__budget-val cpy-dinner-budget-val')
    distance_tags=bs.find_all('span','list-rst__area-genre cpy-area-genre')
    addresses=bs.find_all('p','list-rst__address cpy-address')
    srcs=bs.find_all('img','js-thumbnail-img js-cassette-img js-analytics')
    #srcs_nophoto=bs.find_all('img','js-cassette-img cpy-main-image')

    for score in scores:
        temp_scores.append(score.string)
    for title in titles:
        temp_names.append(title.string)
    for check in checkbit:
        temp_checks.append(check.string)
    for price_lunch in prices_lunch:
        temp_lunch.append(price_lunch.string)
    for price_dinner in prices_dinner:
        temp_dinner.append(price_dinner.string)
    for distance_tag in distance_tags:
        temp_distance_tag.append(distance_tag.string)
    for address in addresses:
        temp_addresses.append(address.string)

    sum=0
    for src in srcs:
        print(src['alt'])
        temp_imageNames.append(src['alt'])
        print(src['data-original'])
        temp_images.append(src['data-original'])
        sum+=1
    print(sum)

    #for src_nophoto in srcs_nophoto:
        #temp_imageNames.append(src_nophoto['alt'])
        #temp_images.append(src_nophoto['data-original'])


    for k in range(len(temp_distance_tag)):
        string1=temp_distance_tag[k].split('/',1)[0]
        string1=string1.strip()
        string2=temp_distance_tag[k].split('/',1)[1]
        string2=string2.strip()
        temp_distance.append(string1)
        temp_tags.append(string2)

    #print(temp_distance)
    #print(temp_tags)



    #print(temp_scores)
    #print(temp_names)
    #print(temp_checks)
    #print(temp_lunch)
    #print(temp_dinner)
    #print(temp_distance_tag)
    print()

    for j in range(20):
        if(stop==11 and j==14):
            break
        if(temp_checks[j]!=' - ' and temp_names[a]!='彩食酒房 瑠飯' and temp_names[a]!='トゥイードル コーヒー' and temp_names[a]!='辻定商店'):
            restaurant_names.append(temp_names[a])
            restaurant_distance.append(temp_distance[a])
            restaurant_tags.append(temp_tags[a])
            restaurant_scores.append(temp_scores[b])
            restaurant_price_lunch.append(temp_lunch[a])
            restaurant_price_dinner.append(temp_dinner[a])
            restaurant_address.append(temp_addresses[a])
            a+=1
            b+=1
        else:
            a+=1

    temp_scores.clear()
    temp_names.clear()
    temp_checks.clear()
    temp_lunch.clear()
    temp_dinner.clear()
    temp_distance_tag.clear()
    temp_distance.clear()
    temp_tags.clear()
    temp_addresses.clear()

    a=0
    b=0

for i in range(len(restaurant_names)):
    print(restaurant_names[i])

with open('restaurant.csv','w',encoding='GB18030',newline='') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['No.','name','address','score','tags','distance','price:lunch','price:dinner'])  
    for i in range(len(restaurant_names)):
        writer.writerow([i+1,restaurant_names[i],restaurant_address[i],restaurant_scores[i],restaurant_tags[i],restaurant_distance[i],restaurant_price_lunch[i],restaurant_price_dinner[i]])

#scores = bs.find_all(class_='c-rating__val c-rating__val--strong list-rst__rating-val')

#print(len(restaurant_names))
#print(len(scores))

k=0
det=0
for i in range(len(restaurant_names)):
    k=0
    for j in range(len(temp_imageNames)):
        if(temp_imageNames[j]==restaurant_names[i]):
            tempstring=str(temp_imageNames[j]).replace(' ','')
            temp_imageNames[j]=tempstring
            path='D:/third/python_class/final/images/'+str(temp_imageNames[j])
            if not os.path.isdir(path):
                os.mkdir(path)
            os.chdir(path)
            r=requests.get(temp_images[j])
            k+=1
            t=os.path.join(path,str(k)+'.jpg')
            fw=open(t,'wb')
            fw.write(r.content)
            downloaded.append(temp_images[j])
            fw.close()
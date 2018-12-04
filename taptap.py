# _*_ coding: utf-8 _*_

import requests
from bs4 import BeautifulSoup

# 解析游戏详情页，获取名字、发行商、评论、版本等
def game_detail(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res,'lxml')
    tag = soup.find('div',class_="show-main-header ")
    name = tag.find('div',class_="main-header-text").h1.text.strip()
    publisher = tag.find('span',itemprop="name").text
    ratingvalue = tag.find('span',itemprop="ratingValue").text
    softwareversion = soup.find('span',itemprop="softwareVersion").text
    #contents = soup.find('div',class_="item-text-body").text
    print(name,publisher,ratingvalue,softwareversion)

# 获取游戏评论
def game_contents(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res,'lxml')
    all_contents_url = soup.find('a',class_="pull-right").get("href")
    new_res = requests.get(all_contents_url).text
    new_soup = BeautifulSoup(new_res,'lxml')
    tags = new_soup.find_all('li',class_="taptap-review-item collapse in")
    for tag in tags:
        user_name = tag.find('span',class_="taptap-user").a.text
        time = tag.find('span',data-toggle="tooltip").get("title data-original-title")
        device = tag.find('span',class_="text-footer-device").text
        contents = tag.find('div',class_="item-text-body").text
        print("%s------使用%s-------%s"  %(user_name,device,time))






url = "https://www.taptap.com/top/download"
res = requests.get(url).text
soup = BeautifulSoup(res,"lxml")
games_info = soup.find_all('div',class_="taptap-top-card")
for game_info in games_info:
    url = game_info.find('div',class_="top-card-middle").a.get("href")
    print("==================================================")
    game_detail(url)
    #name = BeautifulSoup(game_info,"lxml")
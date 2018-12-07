# _*_ coding: utf-8 _*_

import re
import json
import requests
from bs4 import BeautifulSoup

# 解析游戏详情页，获取名字、发行商、评论、版本等
def get_game_detail(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res,'lxml')
    tag = soup.find('div',class_="show-main-header ")
    name = tag.find('div',class_="main-header-text").h1.text.strip()
    publisher = tag.find('span',itemprop="name").text
    ratingvalue = tag.find('span',itemprop="ratingValue").text
    softwareversion = soup.find('span',itemprop="softwareVersion").text
    #contents = soup.find('div',class_="item-text-body").text
    print(name,publisher,ratingvalue,softwareversion)
    if soup.find('div',class_="taptap-review-title section-title").find('a',class_="pull-right"): # 有多页评论
        next_url = soup.find('div',class_="taptap-review-title section-title").find('a',class_="pull-right").get('href')
        review_urls = get_review_pages(next_url)

        for review_url in review_urls:
            print(review_url)
            get_game_contents(review_url)

# 获取游戏评论
def get_game_contents(url):
    res = requests.get(url)
    print(res.url)
    soup = BeautifulSoup(res.text,'lxml')
    #all_contents_url = soup.find('a',class_="pull-right").get("href")
    #new_res = requests.get(all_contents_url).text
    #new_soup = BeautifulSoup(new_res,'lxml')
    tags = soup.find_all('li',class_="taptap-review-item collapse in")
    for tag in tags:
        user_name = tag.find('span',class_="taptap-user").a.text
        time = tag.find('span',attrs={"data-toggle": "tooltip"}).get("title")
        if tag.find('span',class_="text-footer-device"):
            device = tag.find('span',class_="text-footer-device").text
        else:
            device = 'pc'
        contents = tag.find('div',class_="item-text-body").text
        print("%s------使用%s-------%s"  %(user_name,device,time))
        print(contents)
        for sub_tag in tag.find_all('li',class_=re.compile("taptap-comment-item ")):
            sub_user = sub_tag.get("data-user")
            sub_contents = sub_tag.find('div',class_="item-text-body").text
            print("*****************************来自【%s】的回复************************" %sub_user)
            print(sub_contents)
        if tag.find('div',class_="taptap-comments-buttons") and tag.find('div',class_="taptap-comments-buttons").section:
            url_tag = tag.find('div',class_="taptap-comments-buttons").section.find_all('a',rel="nofollow")
            get_sub_contents(url_tag)

# 获取回复评论第2页及后的评论
def get_sub_contents(tags):
    start_page = 2
    end_page = tags[-2].text
    url = tags[0].get('href').split("page=")[0]
    #print(url)
    urls = [url + "page=" + str(i) for i in range(start_page,int(end_page)+1)]
    for url in urls:
        res = requests.get(url).text
        js = json.loads(res, encoding='utf-8')
        soup = BeautifulSoup(js['data']['html'], 'lxml')
        for tag in soup.find_all('li', class_=re.compile("taptap-comment-item ")):
            sub_user = tag.get("data-user")
            sub_contents = tag.find('div', class_="item-text-body").text
            print("*****************************来自【%s】的回复************************" % sub_user)
            print(sub_contents)

def get_review_pages(url):
    res = requests.get(url).text
    soup = BeautifulSoup(res,'lxml')
    tags = soup.find('section',class_="taptap-button-more").find_all('a',rel="nofollow")
    start_page = 1
    end_page = tags[-2].text
    url = tags[0].get('href').split("page=")[0]
    urls = [url + "page=" + str(i) + "#review-list" for i in range(start_page,int(end_page)+1)]
    return urls



url = "https://www.taptap.com/top/download"
res = requests.get(url).text
soup = BeautifulSoup(res,"lxml")
games_info = soup.find_all('div',class_="taptap-top-card")
for game_info in games_info:
    url = game_info.find('div',class_="top-card-middle").a.get("href")
    print("================================================================================")
    get_game_detail(url)
    get_game_contents(url)

import requests
from bs4 import BeautifulSoup
from datetime import date
import ujson
import os
import pickle
import re


def get_current_date():
    current_date = date.today()
    return current_date


def download_image(file_path, url):
    folder_path = 'generate/washington_post/' + get_current_date().strftime("%Y-%m-%d")
    response = requests.get(url)
    if response.status_code == 200:
        with open(folder_path + file_path, 'wb') as file:
            file.write(response.content)
        print("图片下载成功, url=" + url)
    else:
        print("图片下载失败！" + url)


def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def scrap_url(url, header, cookie, param):
    return requests.get(url, params=param, cookies=cookie, headers=header)
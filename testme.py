#coding=utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from test_email import send_alert
import logging


def get_Jzenplaylist():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
                  /66.0.3359.181 Safari/537.36'
    headers = {'User-Agent': user_agent}
    payload = {'id':'322938519'} #我喜欢的音乐歌单
    playlist_page = requests.get("http://music.163.com/playlist", params=payload, headers=headers)
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    #print('Successfully grabbed:', hour, ':', minute)
    logging.info('Successfully grabbed: %(h)d:%(m)d'%{'h':hour,'m':minute})
    bs = BeautifulSoup(playlist_page.content,'lxml')
    playlist_block = bs.find('ul',{'class':'f-hide'})
    playlist = []
    for ta in playlist_block:
        name = ta.a.get_text()
        playlist.append(name)
    return playlist


def compare_list(last_list,now_list):
    '''
    return:
    response : <list> new-added songs
    status : <number> the playlist changes or not
    '''
    response = {}
    status = 0
    last_list = set(last_list)
    now_list = set(now_list)
    added_song = list(now_list - last_list)
    deleted_song = list(last_list - now_list)

    if len(added_song) != 0:
        if len(deleted_song) != 0:
            status = 3 #既有新增歌曲又有减少歌曲
        else:
            status = 2 #仅有新增歌曲没有减少歌曲
    elif len(deleted_song) != 0:
        status = 1     #没有新增歌曲但有减少歌曲

    response['A'] = added_song
    response['D'] = deleted_song

    # for i in range(len(now_list)):
    #     if now_list[i] == last_list[0]:
    #         if i == 0:
    #             response = []
    #         else:
    #             response.extend([now_list[k] for k in range(i)])
    #             status = 1
    #         break

    return response, status


def content_translation(response,status):
    content = ''
    content_head = ['你喜欢的歌曲新增了:','你喜欢的歌曲减少了:']
    content_song = [','.join(response['A']),','.join(response['D'])]
    content_all = [content_head[i] + content_song[i] for i in range(2)]
    if status == 3:
        content = content_all[0]+'\n'+content_all[1]
    elif status == 2:
        content = content_all[0]
    elif status == 1:
        content = content_all[1]
    return content


def run_task():
    global last_list
    now_list = get_Jzenplaylist()
    response, status = compare_list(last_list, now_list)
    last_list = now_list
    if status != 0:
        subject = '你喜欢的歌曲发生变化啦!'
        content = content_translation(response,status)
        send_alert(subject, content)
    return 0


def timer_run(sched_time):
    flag = 0
    while True:
        now = datetime.datetime.now()
        if (now.minute == sched_time.minute) & (flag == 0):
            run_task()
            flag = 1
        else:
            if flag == 1:
                sched_time = sched_time + datetime.timedelta(minutes=1)
                flag = 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        filename='log.txt',
                        filemode='w',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


    last_list = get_Jzenplaylist()
    sched_time = datetime.datetime.now()+datetime.timedelta(seconds=20)
    timer_run(sched_time)







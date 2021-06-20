from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json
import time
import numpy as np

star = {"白羊座":"aries","金牛座":"taurus","双子座":"gemini",
        "巨蟹座":"cancer","狮子座":"leo","处女座":"virgo",
        "天秤座":"libra","天蝎座":"scorpio","射手座":"sagittarius",
        "摩羯座":"capricorn","水瓶座":"aquarius","双鱼座":"pisces"}

plugin_name = 'star'

@on_command('运势')
async def luck(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    st = session.state.get('message') or session.current_arg
    if st == "":
        return
    if st[-1]!= '座':
        st += '座'
    if st not in star.keys():
       await session.send('没有'+st+'这个星座哦！')
    localtime = time.localtime(time.time())
    year = str(localtime.tm_year)
    mon = str(localtime.tm_mon)
    day = str(localtime.tm_mday)
    url = "http://www.xzw.com/fortune/" + star[st] + "/"
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    soup = BeautifulSoup(html)
    html2 = soup.find('div', class_='c_cont')
    html2 = str(html2)
    soup = BeautifulSoup(html2)
    text = ""
    text = year+'.'+mon+'.'+day+st+"的运势:\r\n"
    text = year+'.'+mon+'.'+day+st+"的运势:\r\n"
    text = text + '【整体运势】' + str(soup.find_all('span')[0])[6:-27] + '\r\n'
    text = text + '【爱情运势】' + str(soup.find_all('span')[1])[6:-7] + '\r\n'
    text = text + '【事业学业】' + str(soup.find_all('span')[2])[6:-7] + '\r\n'
    text = text + '【财富运势】' + str(soup.find_all('span')[3])[6:-7] + '\r\n'
    text = text + '【健康运势】' + str(soup.find_all('span')[4])[6:-7] + '\r\n'
    await session.send(text)

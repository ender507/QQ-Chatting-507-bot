from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json
import time

star = {"白羊座":"aries","金牛座":"taurus","双子座":"gemini",
        "巨蟹座":"cancer","狮子座":"leo","处女座":"virgo",
        "天秤座":"libra","天蝎座":"scorpio","射手座":"sagittarius",
        "摩羯座":"capricorn","水瓶座":"aquarius","双鱼座":"pisces"}


luck = on_command('运势')
@luck.handle()
async def _(bot: Bot, event: Event, state: T_State):
    st = str(event.get_message()).strip()
    if st == "":
        return
    if st[-1]!= '座':
        st += '座'
    if st not in star.keys():
       await luck.send('没有'+st+'这个星座哦！')
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
    await luck.send(text)

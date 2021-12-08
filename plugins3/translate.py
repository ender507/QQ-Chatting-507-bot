from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event

import urllib.request
import urllib.parse
import json
import random
import numpy as np

def tslt(contest, from_lang, to_lang):
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    head={}
    head['User_Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    data={}
    data['i']=contest
    data['from']= from_lang
    data['to']= to_lang
    data['smartresult']='dict'
    data['client']='fanyideskweb'
    data['salt']='15656811332752'
    data['sign']='51763d2d84d4ce9e2c32e3af6fcda1c0'
    data['ts']='1565681133275'
    data['bv']='48b19e5b92693b3779082041b5e5429b'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']='FY_BY_CLICKBUTTION'
    data=urllib.parse.urlencode(data).encode('utf-8')
    response = urllib.request.Request(url,data,head)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    return str(json.loads(html)['translateResult'][0][0]['tgt'])


translate = on_command('翻译')
@translate.handle()
async def _(bot: Bot, event: Event, state: T_State):
    content = str(event.get_message()).strip()
    content.replace(':','')
    content.replace('：','')
    if "507" in content:
        await translate.send('不许迫害507！')
        return
    if "dick" in content or "suck" in content:
        reply = ["不要让507bot翻译奇怪的东西呀", "如果你再让507bot翻译奇怪东西的话，507bot可要生气了",\
                 "你要翻译的是什么怪东西","净网bot507要出警啦！"]
        await translate.send(reply[random.randint(0,3)])
        return
    res = tslt(content, "AUTO", "AUTO")
    if "牛牛" in res or "牛子" in res or "女体" in res or "射精" in res or "精液" in res or "阴经" in res or "阴道" in res:
        reply = ["不要让507bot翻译奇怪的东西呀", "如果你再让507bot翻译奇怪东西的话，507bot可要生气了",\
                 "你要翻译的是什么怪东西","净网bot507要出警啦！"]
        await translate.send(reply[random.randint(0,3)])
    else:
        await translate.send('翻译结果：' + res)

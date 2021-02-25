from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import urllib.request
import urllib.parse
import json
import random
BLACK_LIST = ['1292719501']

def tslt(contest):
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    head={}
    head['User_Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    data={}
    data['i']=contest
    data['from']= 'AUTO'
    data['to']= 'AUTO'
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


@on_command('翻译')
async def translate(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    content = str(session.current_arg_text.strip())
    content.replace(':','')
    content.replace('：','')
    if "507" in content:
        await session.send('不许迫害507！')
        return
    if "dick" in content or "suck" in content:
        reply = ["不要让507bot翻译奇怪的东西呀", "如果你再让507bot翻译奇怪东西的话，507bot可要生气了",\
                 "你要翻译的是什么怪东西","净网bot507要出警啦！"]
        await session.send(reply[random.randint(0,3)])
        return
    res = tslt(content)
    if "牛牛" in res or "牛子" in res or "女体" in res or "射精" in res or "精液" in res:
        reply = ["不要让507bot翻译奇怪的东西呀", "如果你再让507bot翻译奇怪东西的话，507bot可要生气了",\
                 "你要翻译的是什么怪东西","净网bot507要出警啦！"]
        await session.send(reply[random.randint(0,3)])
    else:
        await session.send('翻译结果：' + res)

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
import urllib.request
import urllib.parse
import string
import json

music = on_command("音乐")

@music.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["music"] = args


@music.got("music", prompt="请输入歌名")
async def _(bot: Bot, event: Event, state: T_State):
    url='https://v1.hitokoto.cn/nm/search/'+state["music"]+'?type=SONG&offset=0&limit=1'
    url = urllib.parse.quote(url, safe=string.printable)
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    sid = str(json.loads(html)["result"]["songs"][0]["id"])
    
    await music.send(Message('[CQ:music,type=163,id='+sid+']'))

music2 = on_command("qq音乐")

@music2.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["music"] = args


@music2.got("music", prompt="请输入歌名")
async def _(bot: Bot, event: Event, state: T_State):
    url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=1&w='+state["music"]
    url = urllib.parse.quote(url, safe=string.printable)
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    sid = str(json.loads(html[9:-1])['data']["song"]['list'][0]['songid'])
    await music.send(Message('[CQ:music,type=qq,id='+sid+']'))

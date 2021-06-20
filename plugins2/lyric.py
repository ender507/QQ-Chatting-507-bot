from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import urllib.request
import urllib.parse
import json
import numpy as np


plugin_name = 'lyric'


def lrc(contest):
    url='http://music.163.com/api/search/pc'
    head={}
    head['User_Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    data={}
    data['s']=contest
    data['offset']=0
    data['limit']=1
    data['type']=1
    data=urllib.parse.urlencode(data).encode('utf-8')
    response = urllib.request.Request(url,data,head)
    #response.add_header('User_Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')

    sid = str(json.loads(html)["result"]["songs"][0]["id"])
    url='http://music.163.com/api/song/media?id=' + sid
    response = urllib.request.Request(url,data,head)
    #response.add_header('User_Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    return json.loads(html)["lyric"]

@on_command('歌词')
async def lyric(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    content = str(session.current_arg_text.strip())
    content = lrc(content)
    flag = False
    ans = ""
    for i in range(len(content)):
        if content[i] is '[':
            flag = True
        elif content[i] is ']':
            flag = False
        elif content[i] == '\n'and i+1 != len(content)and content[i+1] == '\n':
            continue
        elif flag is False:
            ans += content[i]
    if len(ans)>800:
        ans = ans[:800]
        await session.send('歌词太长了')
    await session.send(ans)

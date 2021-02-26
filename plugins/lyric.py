from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import urllib.request
import urllib.parse
import json

AVAILABLE = True
BLACK_LIST = []

@on_command('lyric启用', permission=SUPERUSER)
async def lyricSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('lyric已启用！507bot想听大家唱歌了')

@on_command('lyric禁用', permission=SUPERUSER)
async def lyricShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('lyric禁用了...是不是你们唱的太难听了？')

@on_command('lyric黑名单', permission=SUPERUSER)
async def lyricBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在lyric黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的lyric功能已禁用')

@on_command('lyric出狱', permission=SUPERUSER)
async def lyricBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在lyric黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的lyric功能已启用')

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
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global AVAILABLE
    if not AVAILABLE:
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
    await session.send(ans)

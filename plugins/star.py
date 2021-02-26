from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import urllib.request
import urllib.parse
import json
import time

star = {"白羊座":"aries","金牛座":"taurus","双子座":"gemini",
        "巨蟹座":"cancer","狮子座":"leo","处女座":"virgo",
        "天秤座":"libra","天蝎座":"scorpio","射手座":"sagittarius",
        "摩羯座":"capricorn","水瓶座":"aquarius","双鱼座":"pisces"}

AVAILABLE = True
BLACK_LIST = []

@on_command('star启用', permission=SUPERUSER)
async def starSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('star已启用！507bot给宁算命了')

@on_command('star禁用', permission=SUPERUSER)
async def starShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('star禁用了...有这么不准吗？')

@on_command('star黑名单', permission=SUPERUSER)
async def starBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在star黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的star功能已禁用')

@on_command('star出狱', permission=SUPERUSER)
async def starBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在star黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的star功能已启用')

@on_command('运势')
async def luck(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global AVAILABLE
    if not AVAILABLE:
        return
    st = session.state.get('message') or session.current_arg
    if st == "":
        return 
    if st not in star.keys():
       await session.send('没有'+st+'这个星座哦！')
    localtime = time.localtime(time.time())
    year = str(localtime.tm_year)
    mon = str(localtime.tm_mon)
    day = str(localtime.tm_mday)
    url = "https://app.data.qq.com/?umod=astro"+\
    "&act=astro&jsonp=1&func=TodatTpl&t=3&a="+str(star[st])+"&y=2015&m="+mon+"&d="+day
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('unicode_escape')
    html = html[9:-2].replace('\r\n','').replace('\n','')
    res = year+'.'+mon+'.'+day+st+"的运势:\n"
    res = res + json.loads(html)["fortune"][0]["content"]
    await session.send(res)

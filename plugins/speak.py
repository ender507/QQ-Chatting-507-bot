from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import requests
import json

AVAILABLE = True
BLACK_LIST = []

@on_command('speak启用', permission=SUPERUSER)
async def teachSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('speak已启用！该整活了')

@on_command('speak禁用', permission=SUPERUSER)
async def teachShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('speak禁用了...都怪群友们整怪东西')

@on_command('speak黑名单', permission=SUPERUSER)
async def teachBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在speak黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的speak功能已禁用')

@on_command('speak出狱', permission=SUPERUSER)
async def teachBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在speak黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的speak功能已启用')

@on_command('说话')
async def learn(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global AVAILABLE
    if not AVAILABLE:
        return
    mes = str(session.state.get('message') or session.current_arg)
    await session.send('[CQ:tts,text='+mes+']')

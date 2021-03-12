from plugins.time_normalizer.TimeNormalizer import TimeNormalizer # 引入包
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import json

AVAILABLE = True

BLACK_LIST = []

@on_command('time启用', permission=SUPERUSER)
async def timeSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('time已启用')

@on_command('time禁用', permission=SUPERUSER)
async def timeShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('time禁用了...')

@on_command('time黑名单', permission=SUPERUSER)
async def timeBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在time黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的time功能已禁用')

@on_command('time出狱', permission=SUPERUSER)
async def timeBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    if uid not in BLACK_LIST:
        await session.send('这个人不在time黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的time功能已启用')

@on_command('时间')
async def time(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    mes = session.state.get('message') or session.current_arg
    mes = str(mes).replace('礼拜','星期')
    tn = TimeNormalizer()
    res = tn.parse(target=mes)
    await session.send(json.loads(res)['timestamp'])

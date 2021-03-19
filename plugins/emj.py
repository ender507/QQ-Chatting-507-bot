from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
from plugins.emojiDef import *
import sys

AVAILABLE = True
BLACK_LIST = ['1292719501',1292719501]

@on_command('emoji启用', permission=SUPERUSER)
async def _(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('emoji已启用，差不多得了')

@on_command('emoji禁用', permission=SUPERUSER)
async def _(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('emoji禁用了...那是真的牛批')

@on_command('emoji黑名单', permission=SUPERUSER)
async def _(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在emoji黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的lyric功能已禁用')

@on_command('emoji出狱', permission=SUPERUSER)
async def _(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在emoji黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的emoji功能已启用')


@on_command('抽象')
async def _(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        await session.send('你懂个锤子的抽象 爬')
        return
    global AVAILABLE
    if not AVAILABLE:
        return
    content = str(session.current_arg_text.strip())
    if '507' in content or '五零七' in content:
        await session.send('你懂个锤子的抽象 爬')
        return
    ans = u""
    for eachChar in content:
        if eachChar not in pinyin.keys():
            ans += eachChar
            continue
        ch = pinyin[eachChar]
        if ch not in emoji.keys():
            ans += eachChar
            continue
        emj = str(emoji[ch])
        ans += emj
    await session.send(ans)

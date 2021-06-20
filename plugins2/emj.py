from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
from plugins.emojiDef import *
import sys
import numpy as np


plugin_name = 'emoji'

@on_command('抽象')
async def _(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
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

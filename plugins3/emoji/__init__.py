from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event

from .emojiDef import *
import sys
import numpy as np


emoji = on_command('抽象')

@emoji.handle()
async def _(bot: Bot, event: Event, state: T_State):
    content = str(event.get_message()).strip()
    if '507' in content or '五零七' in content:
        await emoji.send('你懂个锤子的抽象 爬')
        return
    ans = u""
    for eachChar in content:
        if eachChar not in pinyin.keys():
            ans += eachChar
            continue
        ch = pinyin[eachChar]
        if ch not in emoji_dict.keys():
            ans += eachChar
            continue
        emj = str(emoji_dict[ch])
        ans += emj
    await emoji.send(ans)

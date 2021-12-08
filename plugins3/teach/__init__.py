from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event

import requests
import json
import numpy as np


teach = on_command('学习')
@teach.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip()
    if len(mes) != 2:
        await session.send('不符合格式要求！请在消息和回复之间用空格隔开')
        return
    reply = mes[1]
    mes = mes[0]
    await teach.send('明白了！在有群友说“'+mes+'”时我应该回复“'+reply+'”')
    await teach.send('上述内容会交由507审核，通过后507bot就能实装啦！')
    with open('.\\learn_log.txt','a') as f:
        f.write(mes+' '+reply+'\n')
        

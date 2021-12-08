from aiocqhttp.message import escape
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
from loguru import logger
import random
import numpy as np

from . import itpk_api


nlp = on_command('nlp', aliases=set(('NLP',)))

@nlp.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg:
        state['msg'] = msg



@nlp.got("msg",prompt="请输入任意消息")
async def NLP(bot: Bot, event: Event, state: T_State):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = state['msg']
    reply = await itpk_api.call_NLP_api(bot, event,message)
    if reply:
        # 如果调用机器人成功，得到了回复，则转义之后发送给用户
        await nlp.send(reply)



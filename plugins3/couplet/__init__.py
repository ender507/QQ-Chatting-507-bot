from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
from .data_source import call_api
import numpy as np

"""
couplet插件使用的API为「王斌给您对对联」(https://ai.binwang.me/couplet/) 通过抓包取得的[非公开]API
因此**请不要频繁调用**，对服务器产生影响
如果有条件，可以自行搭建对对联后端 [wb14123/seq2seq-couplet](https://github.com/wb14123/seq2seq-couplet)
若有侵权，请联系开发者删除
"""

couplet = on_command('couplet', aliases=set(('对联', '对对联')))

@couplet.handle()
async def _(bot: Bot, event: Event, state: T_State):
    arg = str(event.get_message()).strip()
    if arg:
        if len(arg) <= 15:
            state['input_couplet'] = arg
        else:
            await couplet.send('上联太长了！重新输入吧')
        return

@couplet.got("input_couplet",prompt="请输入上联：")
async def couplet(bot: Bot, event: Event, state: T_State):
    input_couplet = state["input_couplet"]
    output_couplet = await call_api(bot, event,input_couplet)
    if output_couplet:
        await bot.send(event,f"上联:「{input_couplet}」\n下联:「{output_couplet}」")




from . import id2qq
# id2qq包含一个名为qq的字典，查询方式为:qq['用户名'] = qq号
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event



poke = on_command('poke', aliases=set(('戳','戳一戳')))

@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip()  
    if mes not in id2qq.qq.keys():
        await poke.send('没有查询到名为【'+mes+'】的账号')
    else:
        await poke.send(Message('[CQ:poke,qq='+str(id2qq.qq[mes])+']'))

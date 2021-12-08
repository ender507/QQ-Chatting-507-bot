from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
import random

roll = on_command('roll')
@roll.handle()
async def _(bot: Bot, event: Event, state: T_State):
    content = str(event.get_message()).strip()
    if content.isdigit():
        num = int(content)
        await roll.send('roll点结果：'+str(random.randint(1,num)))

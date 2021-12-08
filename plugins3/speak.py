from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event

speak = on_command("说话")

@speak.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["content"] = args


@speak.got("content", prompt="请输入你想让507bot说的话")
async def _(bot: Bot, event: Event, state: T_State):
    content = state["content"]
    if len(content)>100:
        content = '消息太长了，五零七bot不想说'
    await speak.send(Message('[CQ:tts,text='+content+']'))


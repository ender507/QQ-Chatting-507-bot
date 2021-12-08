'''管理员功能'''
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
from nonebot.permission import SUPERUSER
import os
import shutil
import numpy as np
    

admin_menu = on_command('管理员菜单', permission=SUPERUSER)
@admin_menu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = "\
圆括号内表示要输入的内容\r\n\
【管理员菜单】呼出本菜单\r\n\
【自爆】关闭bot\r\n\
【说】复读和发送CQ码\
"
    await admin_menu.send(mes)


# 直接退出从而关闭程序
explosion = on_command('自爆', permission=SUPERUSER)
@explosion.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await explosion.send('啊我死了')
    await explosion.send(Message('[CQ:record,file=zibao.amr]'))
    exit(0)



# 复读，如"说 你好"会回复"你好"
# 可以接CQ码，如"说 [CQ:image,file=xxx]"
say = on_command('说', permission=SUPERUSER)
@say.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip()
    # 反向转义
    mes = mes.replace('&#44;',',')
    mes = mes.replace('&amp;','&')
    mes = mes.replace('&#91;','[')
    mes = mes.replace('&#93;',']')
    await say.send(Message(mes))


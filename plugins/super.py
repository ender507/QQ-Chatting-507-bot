from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import os
import shutil

@on_command('重启')
async def reboot(session: CommandSession):
    # os.system('start cmd /k "run.bat"')
    await session.send('507bot不会自己重启，因为507不会写代码')
    

@on_command('自爆', permission=SUPERUSER)
async def explosion(session: CommandSession):
    await session.send('啊我死了')
    exit(0)


@on_command('tashikani', permission=SUPERUSER)
async def tashikani(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if '1419626179' not in uid:
        return
    await session.send('就是就是！')


@on_natural_language(keywords={'自爆'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'explosion')


@on_natural_language(keywords={'是不是'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'tashikani')

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
    await session.send('就是就是！')


@on_command('禁用', permission=SUPERUSER)
async def close(session: CommandSession):
    file = session.state.get('message') or session.current_arg
    file =  str(file) + '.py'
    if file=='super.py':
        await session.send('管理模块不能禁用')
    elif os.path.exists('plugins\\'+file):  
        os.remove('plugins\\'+file)
        await session.send(file+'模块禁用成功,下次重启后生效')
    else:
        await session.send('功能模块不存在或未启用')

@on_command('启用', permission=SUPERUSER)
async def open(session: CommandSession):
    file = session.state.get('message') or session.current_arg
    file = str(file) + '.py'
    if os.path.exists('plugins\\'+file):  
        await session.send('功能模块已启用')
    else:
        if os.path.exists('plugins\\backup\\'+file):
            shutil.copy('plugins\\backup\\'+file, "awesome\\plugins\\")
            await session.send(file+'功能模块已启用,下次重启后生效')
        else:
            await session.send('功能模块不存在')


@on_natural_language(keywords={'自爆'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'explosion')


@on_natural_language(keywords={'是不是'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'tashikani')

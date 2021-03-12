from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import random

AVAILABLE = True
BLACK_LIST = []

@on_command('record启用', permission=SUPERUSER)
async def recordSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('record已启用！lulu的粉丝该提纯了')

@on_command('record禁用', permission=SUPERUSER)
async def recordShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('record禁用了，现在我们都是anti了')

@on_command('record黑名单', permission=SUPERUSER)
async def recordBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在record黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的star功能已禁用')

@on_command('record出狱', permission=SUPERUSER)
async def recordBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在record黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的record功能已启用')




@on_command('六六六')
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=666.amr]')

@on_command('az', aliases=('啊这'))
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=az.amr]')

@on_command('谢谢')
async def _(session: CommandSession):

    return
    
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=xiexie.amr]')

@on_command('菜')
async def _(session: CommandSession):

    return
    
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=cai.amr]')

@on_command('来点鬼叫', aliases=('来点怪叫'))
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=guaijiao'+str(random.randint(1,10))+'.amr]')

@on_command('来点鬼歌', aliases=('来点怪歌'))
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=g'+str(random.randint(1,10))+'.amr]')

@on_command('怎么办')
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=zenmeban'+str(random.randint(1,2))+'.amr]')

@on_command('绝了')
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=juele.amr]')

@on_command('别走')
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=biezou.amr]')

@on_command('nice', aliases=('奈斯'))
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=nice.amr]')

@on_command('求饶')
async def _(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:record,file=qiurao.amr]')

@on_command('这波')
async def zhebo(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    if random.randint(0,2) == 1:
        await session.send('[CQ:record,file=zhebo.amr]')

@on_natural_language(keywords={'这波'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '这波')

@on_natural_language(keywords={'别走'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '别走')

@on_natural_language(keywords={'怎么办'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '怎么办')

@on_natural_language(keywords={'谢'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '谢谢')

@on_natural_language(keywords={'菜'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '菜')

@on_natural_language(keywords={'六六六','666'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '六六六')

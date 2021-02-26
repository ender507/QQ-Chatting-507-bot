from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *

AVAILABLE = True
BLACK_LIST = []

@on_command('teach启用', permission=SUPERUSER)
async def teachSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('teach已启用！507bot想要学习')

@on_command('teach禁用', permission=SUPERUSER)
async def teachShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('teach禁用了...都怪群友们教怪东西')

@on_command('teach黑名单', permission=SUPERUSER)
async def teachBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在teach黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的teach功能已禁用')

@on_command('teach出狱', permission=SUPERUSER)
async def teachBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在teach黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的teach功能已启用')

@on_command('学习')
async def learn(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global AVAILABLE
    if not AVAILABLE:
        return
    mes = str(session.state.get('message') or session.current_arg).split()
    if len(mes) != 2:
        await session.send('不符合格式要求！请在消息和回复之间用空格隔开')
        return
    reply = mes[1]
    mes = mes[0]
    await session.send('明白了！在有群友说“'+mes+'”时我应该回复“'+reply+'”')
    await session.send('上述内容会交由507审核，通过后507bot就能实装啦！')
    with open('plugins\\learn_log.txt','a') as f:
        f.write(mes+' '+reply+'\n')
    

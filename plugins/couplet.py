from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_text
from nonebot.command.argfilter.validators import fit_size
from nonebot.permission import *
from plugins.couplet_src.data_source import call_api

"""
couplet插件使用的API为「王斌给您对对联」(https://ai.binwang.me/couplet/) 通过抓包取得的[非公开]API
因此**请不要频繁调用**，对服务器产生影响
如果有条件，可以自行搭建对对联后端 [wb14123/seq2seq-couplet](https://github.com/wb14123/seq2seq-couplet)
若有侵权，请联系开发者删除
"""
AVAILABLE = True
BLACK_LIST = []

__plugin_name__ = 'couplet(对对联)'
__plugin_usage__ = r"""
神经网络自动对对联
不支持繁体字和特殊符号，断句请用全角逗号分隔
【本插件使用的API为「王斌给您对对联」(https://ai.binwang.me/couplet/) 通过抓包取得的[非公开]API】
【因此请不要频繁调用，对服务器产生影响】
Command(s):
 - /couplet [上联]
""".strip()

@on_command('couplet启用', permission=SUPERUSER)
async def coupletSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('couplet已启用！来和507bot对对联吧')

@on_command('couplet禁用', permission=SUPERUSER)
async def coupletShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('couplet禁用了...507bot的对联对得这么差吗？')

@on_command('couplet黑名单', permission=SUPERUSER)
async def coupletBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在couplet黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的couplet功能已禁用')

@on_command('couplet出狱', permission=SUPERUSER)
async def coupletBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在couplet黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的couplet功能已启用')

@on_command('couplet', aliases=('对联', '对对联'))
async def couplet(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global AVAILABLE
    if not AVAILABLE:
        return
    input_couplet = session.get('input_couplet', prompt="请输入对联上联",
                                arg_filters=[
                                    handle_cancellation(session),
                                    extract_text,
                                    fit_size(max_length=20, message="上联太长了！重新输入吧")
                                ])
    output_couplet = await call_api(session, input_couplet)

    if output_couplet:
        await session.send(f"上联:「{input_couplet}」\n下联:「{output_couplet}」")

@couplet.args_parser
async def _(session: CommandSession):
    arg = session.current_arg.strip()

    if session.is_first_run:
        if arg:
            if len(arg) <= 15:
                session.state['input_couplet'] = arg
            else:
                await session.send('上联太长了！重新输入吧')
        return

    if not arg:
        session.pause('请输入对联上联')

    session.state[session.current_key] = arg

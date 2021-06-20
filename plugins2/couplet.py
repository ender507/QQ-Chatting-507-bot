from nonebot import on_command, CommandSession
from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_text
from nonebot.command.argfilter.validators import fit_size
from nonebot.permission import *
from plugins.couplet_src.data_source import call_api
import numpy as np

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

plugin_name = 'couplet'


@on_command('couplet', aliases=('对联', '对对联'))
async def couplet(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
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
